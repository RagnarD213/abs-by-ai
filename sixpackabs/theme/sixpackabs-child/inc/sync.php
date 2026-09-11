<?php
/**
 * The hourly sync: absbyai.com feeds → WordPress.
 *
 * absbyai.com/api/sixpackabs/channel.json lists the channel's PUBLIC videos
 * (the public-only filter lives there, in scripts/sixpackabs/feed.js, with
 * tests). For each one this upserts a `spa_video` post keyed by
 * `_spa_youtube_id`:
 *
 *   create  published, dated like YouTube, notes = the description as blocks,
 *           excerpt = its first paragraph, featured image = the maxres
 *           thumbnail downloaded into the media library (+ the vertical
 *           thumbnail for Shorts).
 *   update  title, date, duration, thumbnails and type follow YouTube. The notes
 *           and excerpt follow YouTube ONLY while md5(stored text) still equals
 *           the hash recorded at import — the moment Dan edits them in
 *           WordPress the text is his and the sync never touches it again.
 *   gone    a video that leaves the feed (made private/unlisted/deleted) goes to
 *           draft — never deleted — and comes back if it returns. A video Dan
 *           drafted or trashed himself stays that way.
 *
 * instagram.json lists @danrosefit's 6 latest photo posts; each image is
 * downloaded once (the Graph CDN URLs expire) and the set is kept in the
 * `spa_instagram` option.
 *
 * Runs: WP-Cron hourly (`spa_sync`), `wp spa sync`, or Videos → "Sync now".
 */

defined( 'ABSPATH' ) || exit;

if ( ! defined( 'SPA_FEED_BASE' ) ) {
	define( 'SPA_FEED_BASE', 'https://absbyai.com/api/sixpackabs' );
}

add_action( 'spa_sync', 'spa_sync_run' );

add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'spa_sync' ) ) {
		wp_schedule_event( time() + 60, 'hourly', 'spa_sync' );
	}
} );

// Switching away from this theme stops the job (it comes back on re-activation).
add_action( 'switch_theme', function () {
	wp_clear_scheduled_hook( 'spa_sync' );
} );

function spa_sync_run() {
	if ( get_transient( 'spa_sync_lock' ) ) {
		return array( 'skipped' => 'another sync is running' );
	}
	set_transient( 'spa_sync_lock', time(), 15 * MINUTE_IN_SECONDS );
	if ( function_exists( 'set_time_limit' ) ) {
		@set_time_limit( 600 ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
	}
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';

	$report = array( 'at' => gmdate( 'c' ) );
	try {
		$report['videos']    = spa_sync_videos();
		$report['instagram'] = spa_sync_instagram();
	} finally {
		delete_transient( 'spa_sync_lock' );
	}
	update_option( 'spa_sync_last', $report, false );
	error_log( 'spa_sync ' . wp_json_encode( $report ) ); // phpcs:ignore WordPress.PHP.DevelopmentFunctions
	return $report;
}

function spa_fetch_feed( $name ) {
	$res = wp_remote_get( SPA_FEED_BASE . '/' . $name . '.json', array( 'timeout' => 30, 'headers' => array( 'Accept' => 'application/json' ) ) );
	if ( is_wp_error( $res ) ) {
		return $res;
	}
	$code = (int) wp_remote_retrieve_response_code( $res );
	if ( 200 !== $code ) {
		return new WP_Error( 'spa_feed_http', "$name.json returned HTTP $code" );
	}
	$data = json_decode( wp_remote_retrieve_body( $res ), true );
	return is_array( $data ) ? $data : new WP_Error( 'spa_feed_json', "$name.json is not valid JSON" );
}

/* ------------------------------------------------------------------------
 * Videos
 * --------------------------------------------------------------------- */

function spa_sync_videos() {
	$feed = spa_fetch_feed( 'channel' );
	if ( is_wp_error( $feed ) ) {
		return array( 'error' => $feed->get_error_message() );
	}
	spa_ensure_video_terms();
	if ( ! empty( $feed['channel'] ) && is_array( $feed['channel'] ) ) {
		update_option( 'spa_channel', array(
			'subscriberCount' => isset( $feed['channel']['subscriberCount'] ) ? (int) $feed['channel']['subscriberCount'] : null,
			'videoCount'      => isset( $feed['channel']['videoCount'] ) ? (int) $feed['channel']['videoCount'] : null,
		), false );
	}

	$videos = isset( $feed['videos'] ) && is_array( $feed['videos'] ) ? $feed['videos'] : array();
	$counts = array( 'feed' => count( $videos ), 'created' => 0, 'updated' => 0, 'unchanged' => 0, 'restored' => 0, 'drafted' => 0, 'errors' => array() );
	if ( ! empty( $feed['stale'] ) ) {
		$counts['stale_feed'] = true;
	}

	$seen = array();
	foreach ( $videos as $v ) {
		$yt = isset( $v['id'] ) ? preg_replace( '/[^A-Za-z0-9_-]/', '', (string) $v['id'] ) : '';
		if ( 11 !== strlen( $yt ) || empty( $v['publishedAt'] ) ) {
			continue;
		}
		$v['id']     = $yt;
		$seen[ $yt ] = true;
		$result      = spa_upsert_video( $v );
		if ( is_wp_error( $result ) ) {
			$counts['errors'][] = $yt . ': ' . $result->get_error_message();
		} else {
			$counts[ $result ]++;
		}
	}

	// Unpublish what left the feed. An empty or suspiciously short feed (under
	// half of what is published) never unpublishes anything.
	$published = spa_published_videos_by_youtube_id();
	$missing   = array_diff_key( $published, $seen );
	if ( $missing ) {
		if ( $seen && count( $seen ) >= 0.5 * count( $published ) ) {
			foreach ( $missing as $post_id ) {
				wp_update_post( array( 'ID' => $post_id, 'post_status' => 'draft' ) );
				update_post_meta( $post_id, '_spa_auto_drafted', 1 );
				$counts['drafted']++;
			}
		} else {
			$counts['errors'][] = 'feed looked short; left ' . count( $missing ) . ' missing videos published';
		}
	}
	return $counts;
}

function spa_upsert_video( array $v ) {
	$yt            = $v['id'];
	$duration      = isset( $v['durationSeconds'] ) ? (int) $v['durationSeconds'] : 0;
	$type          = ( isset( $v['type'] ) && in_array( $v['type'], array( 'long', 'short' ), true ) ) ? $v['type'] : ( $duration <= SPA_SHORT_MAX_SECONDS ? 'short' : 'long' );
	$published_gmt = gmdate( 'Y-m-d H:i:s', strtotime( $v['publishedAt'] ) );
	$title         = wp_strip_all_tags( (string) ( $v['title'] ?? '' ) );
	$description   = (string) ( $v['description'] ?? '' );
	$source_hash   = md5( $description );
	$thumbs        = isset( $v['thumbnails'] ) && is_array( $v['thumbnails'] ) ? $v['thumbnails'] : array();
	$meta          = array(
		'_spa_youtube_id'   => $yt,
		'_spa_duration'     => $duration,
		// Stored as plain UTC 'Y-m-d H:i:s' (like post_date_gmt): some database layers
		// rewrite ISO-8601 strings, which made every hourly run look like a change.
		'_spa_published_at' => $published_gmt,
		'_spa_thumb_url'    => esc_url_raw( (string) ( $thumbs['maxres'] ?? '' ) ),
		'_spa_portrait_url' => esc_url_raw( (string) ( $thumbs['portrait'] ?? '' ) ),
		'_spa_embeddable'   => empty( $v['embeddable'] ) ? 0 : 1,
	);

	$existing = spa_find_video( $yt );

	if ( ! $existing ) {
		$post_id = wp_insert_post( wp_slash( array(
			'post_type'      => 'spa_video',
			'post_status'    => 'publish',
			'post_title'     => $title,
			'post_name'      => sanitize_title( $title ),
			'post_content'   => spa_description_to_blocks( $description ),
			'post_excerpt'   => spa_description_excerpt( $description ),
			'post_date'      => get_date_from_gmt( $published_gmt ),
			'post_date_gmt'  => $published_gmt,
			'post_author'    => spa_sync_author_id(),
			'comment_status' => 'closed',
			'ping_status'    => 'closed',
		) ), true );
		if ( is_wp_error( $post_id ) ) {
			return $post_id;
		}
		foreach ( $meta as $k => $val ) {
			update_post_meta( $post_id, $k, $val );
		}
		update_post_meta( $post_id, '_spa_source_hash', $source_hash );
		spa_record_imported_text( $post_id, true, true );
		wp_set_object_terms( $post_id, $type, 'spa_video_type' );
		spa_sync_thumbnails( $post_id, $v );
		return 'created';
	}

	if ( 'trash' === $existing->post_status ) {
		return 'unchanged'; // Dan deleted it on purpose.
	}

	$post_id  = $existing->ID;
	$changed  = false;
	$restored = false;
	$update   = array( 'ID' => $post_id );
	$reasons  = array(); // what differed — kept for the self-test and debugging

	if ( wp_specialchars_decode( $existing->post_title, ENT_QUOTES ) !== $title ) {
		$update['post_title'] = $title; // the slug (URL) never changes
		$reasons[]            = 'title';
	}
	if ( $existing->post_date_gmt !== $published_gmt ) {
		$update['post_date']     = get_date_from_gmt( $published_gmt );
		$update['post_date_gmt'] = $published_gmt;
		$reasons[]               = 'date';
	}

	$wrote_content = false;
	$wrote_excerpt = false;
	if ( get_post_meta( $post_id, '_spa_source_hash', true ) !== $source_hash ) {
		if ( spa_text_untouched( $existing, 'content' ) ) {
			$update['post_content'] = spa_description_to_blocks( $description );
			$wrote_content          = true;
			$reasons[]              = 'notes';
		}
		if ( spa_text_untouched( $existing, 'excerpt' ) ) {
			$update['post_excerpt'] = spa_description_excerpt( $description );
			$wrote_excerpt          = true;
			$reasons[]              = 'excerpt';
		}
	}

	if ( 'draft' === $existing->post_status && get_post_meta( $post_id, '_spa_auto_drafted', true ) ) {
		$update['post_status'] = 'publish';
		$restored              = true;
		$reasons[]             = 'restored';
	}

	if ( count( $update ) > 1 ) {
		$r = wp_update_post( wp_slash( $update ), true );
		if ( is_wp_error( $r ) ) {
			return $r;
		}
		$changed = true;
		if ( $restored ) {
			delete_post_meta( $post_id, '_spa_auto_drafted' );
		}
		if ( $wrote_content || $wrote_excerpt ) {
			spa_record_imported_text( $post_id, $wrote_content, $wrote_excerpt );
		}
	}
	if ( get_post_meta( $post_id, '_spa_source_hash', true ) !== $source_hash ) {
		update_post_meta( $post_id, '_spa_source_hash', $source_hash );
	}

	foreach ( $meta as $k => $val ) {
		if ( (string) get_post_meta( $post_id, $k, true ) !== (string) $val ) {
			update_post_meta( $post_id, $k, $val );
			$changed   = true;
			$reasons[] = $k;
		}
	}

	if ( ! get_post_meta( $post_id, '_spa_type_override', true ) ) {
		$current = wp_get_object_terms( $post_id, 'spa_video_type', array( 'fields' => 'slugs' ) );
		if ( is_wp_error( $current ) || array( $type ) !== array_values( $current ) ) {
			wp_set_object_terms( $post_id, $type, 'spa_video_type' );
			$changed   = true;
			$reasons[] = 'type';
		}
	}

	if ( spa_sync_thumbnails( $post_id, $v ) ) {
		$changed   = true;
		$reasons[] = 'thumbnail';
	}

	$GLOBALS['spa_upsert_reasons'] = $reasons;
	if ( $restored ) {
		return 'restored';
	}
	return $changed ? 'updated' : 'unchanged';
}

/** True while the stored notes/excerpt are still exactly what the sync wrote. */
function spa_text_untouched( WP_Post $post, $field ) {
	if ( 'excerpt' === $field ) {
		return md5( $post->post_excerpt ) === get_post_meta( $post->ID, '_spa_imported_excerpt_hash', true );
	}
	return md5( $post->post_content ) === get_post_meta( $post->ID, '_spa_imported_hash', true );
}

/** Hash what WordPress actually stored (kses may normalise the markup). */
function spa_record_imported_text( $post_id, $content, $excerpt ) {
	clean_post_cache( $post_id );
	$p = get_post( $post_id );
	if ( $content ) {
		update_post_meta( $post_id, '_spa_imported_hash', md5( $p->post_content ) );
	}
	if ( $excerpt ) {
		update_post_meta( $post_id, '_spa_imported_excerpt_hash', md5( $p->post_excerpt ) );
	}
}

function spa_find_video( $yt ) {
	$ids = get_posts( array(
		'post_type'        => 'spa_video',
		'post_status'      => array( 'publish', 'draft', 'pending', 'private', 'future', 'trash' ),
		'meta_key'         => '_spa_youtube_id', // phpcs:ignore WordPress.DB.SlowDBQuery
		'meta_value'       => $yt, // phpcs:ignore WordPress.DB.SlowDBQuery
		'posts_per_page'   => 1,
		'fields'           => 'ids',
		'no_found_rows'    => true,
		'suppress_filters' => true,
	) );
	return $ids ? get_post( $ids[0] ) : null;
}

function spa_published_videos_by_youtube_id() {
	$ids = get_posts( array(
		'post_type'        => 'spa_video',
		'post_status'      => 'publish',
		'posts_per_page'   => -1,
		'fields'           => 'ids',
		'no_found_rows'    => true,
		'suppress_filters' => true,
	) );
	$out = array();
	foreach ( $ids as $id ) {
		$yt = get_post_meta( $id, '_spa_youtube_id', true );
		if ( $yt ) {
			$out[ $yt ] = $id;
		}
	}
	return $out;
}

function spa_sync_author_id() {
	$ids = get_users( array( 'role' => 'administrator', 'number' => 1, 'orderby' => 'ID', 'order' => 'ASC', 'fields' => 'ID' ) );
	return $ids ? (int) $ids[0] : 0;
}

/**
 * YouTube description → paragraph blocks: blank lines split paragraphs, single
 * newlines become <br>, URLs become nofollow links, hashtags stay as text.
 */
function spa_description_to_blocks( $description ) {
	$text = trim( str_replace( array( "\r\n", "\r" ), "\n", (string) $description ) );
	if ( '' === $text ) {
		return '';
	}
	$blocks = array();
	foreach ( preg_split( "/\n\s*\n+/", $text ) as $para ) {
		$para = trim( $para );
		if ( '' === $para ) {
			continue;
		}
		$html = preg_replace_callback( '~https?://[^\s<]+~i', function ( $m ) {
			$raw  = rtrim( $m[0], '.,;:!?)' );
			$tail = substr( $m[0], strlen( $raw ) );
			$href = esc_url( wp_specialchars_decode( $raw, ENT_QUOTES ) );
			return '<a href="' . $href . '" rel="nofollow noopener">' . $raw . '</a>' . $tail;
		}, esc_html( $para ) );
		$html     = nl2br( $html, false );
		$blocks[] = "<!-- wp:paragraph -->\n<p>" . $html . "</p>\n<!-- /wp:paragraph -->";
	}
	return implode( "\n\n", $blocks );
}

/** The first paragraph of a description, URLs removed, at most ~300 characters. */
function spa_description_excerpt( $description ) {
	$text  = trim( str_replace( array( "\r\n", "\r" ), "\n", (string) $description ) );
	$first = trim( (string) preg_split( "/\n\s*\n+/", $text )[0] );
	$first = trim( preg_replace( '/\s+/', ' ', preg_replace( '~https?://\S+~i', '', $first ) ) );
	if ( mb_strlen( $first ) > 300 ) {
		$first = rtrim( preg_replace( '/\s+\S*$/u', '', mb_substr( $first, 0, 297 ) ), ' ,;:' ) . '…';
	}
	return $first;
}

/**
 * Download the maxres thumbnail as the featured image (again when YouTube's
 * ETag changes — Dan swapping a thumbnail), plus the vertical one for Shorts
 * that have it. Returns true when anything changed.
 */
function spa_sync_thumbnails( $post_id, array $v ) {
	$thumbs  = isset( $v['thumbnails'] ) && is_array( $v['thumbnails'] ) ? $v['thumbnails'] : array();
	$version = (string) ( $thumbs['version'] ?? '' );
	$title   = wp_strip_all_tags( (string) ( $v['title'] ?? '' ) );
	$changed = false;

	$have = (int) get_post_thumbnail_id( $post_id );
	if ( ! empty( $thumbs['maxres'] ) && ( ! $have || ( $version && $version !== (string) get_post_meta( $post_id, '_spa_thumb_version', true ) ) ) ) {
		$att = spa_sideload( $thumbs['maxres'], 'yt-' . $v['id'] . '.jpg', $post_id, $title );
		if ( ! is_wp_error( $att ) ) {
			set_post_thumbnail( $post_id, $att );
			update_post_meta( $post_id, '_spa_thumb_version', $version );
			$changed = true;
		}
	}

	// YouTube's vertical thumbnail is NOT downloaded: it is a frame from the video
	// (mid-sentence, burned captions). Shorts show Dan's cover art cropped to 9:16
	// instead — his call, 2026-09-11. See spa_video_img().
	$have = (int) get_post_thumbnail_id( $post_id );
	if ( $have ) {
		spa_ensure_short_crop( $have );
	}
	return $changed;
}

/**
 * Make sure an attachment has the 9:16 'spa-short' rendition. Image sizes are only
 * built at upload time, so thumbnails downloaded before the size existed need one
 * pass of regeneration. Runs once per attachment (the guard meta stops retries on
 * a host whose image editor cannot make it).
 */
function spa_ensure_short_crop( $att_id ) {
	$meta = wp_get_attachment_metadata( $att_id );
	if ( ! is_array( $meta ) || isset( $meta['sizes']['spa-short'] ) ) {
		return;
	}
	if ( get_post_meta( $att_id, '_spa_short_crop_tried', true ) ) {
		return;
	}
	update_post_meta( $att_id, '_spa_short_crop_tried', 1 );
	$file = get_attached_file( $att_id );
	if ( ! $file || ! file_exists( $file ) ) {
		return;
	}
	$fresh = wp_generate_attachment_metadata( $att_id, $file );
	if ( is_array( $fresh ) && isset( $fresh['sizes']['spa-short'] ) ) {
		wp_update_attachment_metadata( $att_id, $fresh );
	}
}

function spa_sideload( $url, $filename, $parent_id, $description ) {
	$tmp = download_url( $url, 60 );
	if ( is_wp_error( $tmp ) ) {
		return $tmp;
	}
	$att = media_handle_sideload( array( 'name' => sanitize_file_name( $filename ), 'tmp_name' => $tmp ), $parent_id, $description );
	if ( is_wp_error( $att ) ) {
		@unlink( $tmp ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
		return $att;
	}
	update_post_meta( $att, '_spa_sync_owned', 1 );
	return $att;
}

/* ------------------------------------------------------------------------
 * Instagram
 * --------------------------------------------------------------------- */

function spa_sync_instagram() {
	$feed = spa_fetch_feed( 'instagram' );
	if ( is_wp_error( $feed ) ) {
		return array( 'error' => $feed->get_error_message() );
	}
	$items  = isset( $feed['images'] ) && is_array( $feed['images'] ) ? array_slice( $feed['images'], 0, 6 ) : array();
	$stored = array();
	foreach ( (array) get_option( 'spa_instagram', array() ) as $s ) {
		if ( ! empty( $s['id'] ) ) {
			$stored[ $s['id'] ] = $s;
		}
	}

	$out    = array();
	$new    = 0;
	$errors = array();
	foreach ( $items as $it ) {
		$ig        = preg_replace( '/\D/', '', (string) ( $it['id'] ?? '' ) );
		$permalink = esc_url_raw( (string) ( $it['permalink'] ?? '' ) );
		if ( ! $ig || 'www.instagram.com' !== wp_parse_url( $permalink, PHP_URL_HOST ) ) {
			continue;
		}
		$alt = sanitize_text_field( (string) ( $it['alt'] ?? '' ) );
		$att = isset( $stored[ $ig ] ) && get_post( (int) $stored[ $ig ]['attachment_id'] ) ? (int) $stored[ $ig ]['attachment_id'] : spa_find_ig_attachment( $ig );
		if ( ! $att ) {
			if ( empty( $it['imageUrl'] ) ) {
				continue;
			}
			$att = spa_sideload( $it['imageUrl'], 'ig-' . $ig . '.jpg', 0, $alt );
			if ( is_wp_error( $att ) ) {
				$errors[] = $ig . ': ' . $att->get_error_message();
				continue;
			}
			update_post_meta( $att, '_spa_ig_media_id', $ig );
			update_post_meta( $att, '_wp_attachment_image_alt', $alt );
			$new++;
		}
		$out[] = array(
			'id'            => $ig,
			'permalink'     => $permalink,
			'attachment_id' => $att,
			'timestamp'     => sanitize_text_field( (string) ( $it['timestamp'] ?? '' ) ),
			'alt'           => $alt,
		);
	}
	if ( $out ) {
		update_option( 'spa_instagram', $out, false );
	}
	return array( 'feed' => count( $items ), 'kept' => count( $out ), 'new' => $new, 'errors' => $errors );
}

function spa_find_ig_attachment( $ig ) {
	$ids = get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'inherit',
		'meta_key'       => '_spa_ig_media_id', // phpcs:ignore WordPress.DB.SlowDBQuery
		'meta_value'     => $ig, // phpcs:ignore WordPress.DB.SlowDBQuery
		'posts_per_page' => 1,
		'fields'         => 'ids',
		'no_found_rows'  => true,
	) );
	return $ids ? (int) $ids[0] : 0;
}

/* ------------------------------------------------------------------------
 * Running it by hand: WP-CLI, the "Sync now" button, the status line.
 * --------------------------------------------------------------------- */

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::add_command( 'spa sync', function () {
		$report = spa_sync_run();
		WP_CLI::line( wp_json_encode( $report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES ) );
		WP_CLI::success( 'spa sync finished' );
	} );
}

add_action( 'admin_post_spa_sync', function () {
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( 'Not allowed.', 403 );
	}
	check_admin_referer( 'spa_sync' );
	spa_sync_run();
	wp_safe_redirect( add_query_arg( 'spa_synced', 1, admin_url( 'edit.php?post_type=spa_video' ) ) );
	exit;
} );

function spa_sync_now_url() {
	return wp_nonce_url( admin_url( 'admin-post.php?action=spa_sync' ), 'spa_sync' );
}

function spa_sync_status_line() {
	$last = get_option( 'spa_sync_last' );
	echo '<p style="color:#646970">';
	if ( is_array( $last ) && ! empty( $last['at'] ) ) {
		$v = $last['videos'] ?? array();
		echo esc_html( sprintf(
			'Last sync %s ago: %s videos in the feed, %d new, %d updated.',
			human_time_diff( strtotime( $last['at'] ) ),
			isset( $v['feed'] ) ? (int) $v['feed'] : '?',
			(int) ( $v['created'] ?? 0 ),
			(int) ( $v['updated'] ?? 0 )
		) );
		if ( ! empty( $v['error'] ) || ! empty( $v['errors'] ) ) {
			echo ' <strong>' . esc_html( 'Problem: ' . ( $v['error'] ?? implode( '; ', (array) $v['errors'] ) ) ) . '</strong>';
		}
	} else {
		echo 'Not synced yet.';
	}
	if ( current_user_can( 'manage_options' ) ) {
		echo ' <a href="' . esc_url( spa_sync_now_url() ) . '">Sync now</a>';
	}
	echo '</p>';
}

add_action( 'admin_notices', function () {
	$screen = function_exists( 'get_current_screen' ) ? get_current_screen() : null;
	if ( ! $screen || 'edit-spa_video' !== $screen->id ) {
		return;
	}
	echo '<div class="notice notice-info">';
	if ( isset( $_GET['spa_synced'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
		echo '<p><strong>Synced with YouTube and Instagram.</strong></p>';
	}
	echo '<p>These pages are created automatically from the public videos on the Abs by AI YouTube channel, every hour. Edit a video\'s notes here and the sync leaves its text alone from then on.</p>';
	spa_sync_status_line();
	echo '</div>';
} );
