<?php
/**
 * Content model.
 *
 * - `spa_video`: one public page per YouTube video at /videos/<slug>/. The
 *   post type archive /videos/ lists long-form only; /shorts/ lists Shorts.
 * - `spa_video_type`: `long` or `short`. The hourly sync sets it from the
 *   duration (Short = 180 s or less) unless Dan picks an override in the
 *   "YouTube sync" box on the edit screen.
 * - Meta the sync writes: `_spa_youtube_id`, `_spa_duration`,
 *   `_spa_published_at`, `_spa_thumb_url`, `_spa_portrait_url`,
 *   `_spa_type_override`, `_spa_imported_hash` (see inc/sync.php for how the
 *   hash protects Dan's edits to the notes).
 */

defined( 'ABSPATH' ) || exit;

const SPA_SHORT_MAX_SECONDS = 180;

add_action( 'init', 'spa_register_content_model' );

function spa_register_content_model() {
	register_post_type( 'spa_video', array(
		'labels'        => array(
			'name'               => 'Videos',
			'singular_name'      => 'Video',
			'menu_name'          => 'Videos',
			'all_items'          => 'All videos',
			'add_new_item'       => 'Add video',
			'edit_item'          => 'Edit video',
			'view_item'          => 'View video',
			'search_items'       => 'Search videos',
			'not_found'          => 'No videos found',
			'not_found_in_trash' => 'No videos in the trash',
		),
		'public'        => true,
		'has_archive'   => 'videos',
		'rewrite'       => array( 'slug' => 'videos', 'with_front' => false ),
		'show_in_rest'  => true,
		'supports'      => array( 'title', 'editor', 'excerpt', 'thumbnail', 'custom-fields' ),
		'menu_icon'     => 'dashicons-video-alt3',
		'menu_position' => 5,
	) );

	// No /type/<term>/ URLs: the two archives live at /videos/ and /shorts/
	// (rewrite rule below, term links filtered to match).
	register_taxonomy( 'spa_video_type', 'spa_video', array(
		'labels'            => array( 'name' => 'Video types', 'singular_name' => 'Video type' ),
		'public'            => true,
		'hierarchical'      => false,
		'show_in_rest'      => true,
		'show_admin_column' => true,
		'show_in_menu'      => false,
		'meta_box_cb'       => false,
		'rewrite'           => false,
		'query_var'         => 'spa_video_type',
	) );

	$meta = array(
		'_spa_youtube_id'    => 'string',
		'_spa_duration'      => 'integer',
		'_spa_published_at'  => 'string',
		'_spa_thumb_url'     => 'string',
		'_spa_portrait_url'  => 'string',
		'_spa_type_override' => 'string',
		'_spa_imported_hash' => 'string',
	);
	foreach ( $meta as $key => $type ) {
		register_post_meta( 'spa_video', $key, array(
			'type'          => $type,
			'single'        => true,
			'show_in_rest'  => true,
			'auth_callback' => function () {
				return current_user_can( 'edit_posts' );
			},
		) );
	}

	add_rewrite_rule( '^shorts/?$', 'index.php?spa_video_type=short', 'top' );
	add_rewrite_rule( '^shorts/page/([0-9]{1,})/?$', 'index.php?spa_video_type=short&paged=$matches[1]', 'top' );
}

function spa_ensure_video_terms() {
	foreach ( array( 'long' => 'Free videos', 'short' => 'Shorts' ) as $slug => $name ) {
		$term = get_term_by( 'slug', $slug, 'spa_video_type' );
		if ( ! $term ) {
			wp_insert_term( $name, 'spa_video_type', array( 'slug' => $slug ) );
		} elseif ( $term->name !== $name ) {
			wp_update_term( $term->term_id, 'spa_video_type', array( 'name' => $name ) );
		}
	}
}

// Browser-tab titles for the two archives (core and Yoast): "Free videos" / "Shorts".
function spa_archive_title() {
	if ( is_tax( 'spa_video_type', 'short' ) ) {
		return 'Shorts';
	}
	if ( is_post_type_archive( 'spa_video' ) || is_tax( 'spa_video_type', 'long' ) ) {
		return 'Free videos';
	}
	return '';
}
add_filter( 'document_title_parts', function ( $parts ) {
	$t = spa_archive_title();
	if ( $t ) {
		$parts['title'] = $t;
	}
	return $parts;
} );
add_filter( 'wpseo_title', function ( $title ) {
	$t = spa_archive_title();
	return $t ? $t . ' – ' . get_bloginfo( 'name' ) : $title;
} );

// Term links point at the two real archives.
add_filter( 'term_link', function ( $url, $term, $taxonomy ) {
	if ( 'spa_video_type' !== $taxonomy ) {
		return $url;
	}
	return 'short' === $term->slug ? home_url( '/shorts/' ) : home_url( '/videos/' );
}, 10, 3 );

// /videos/ = long-form only, 12 per page; /shorts/ = Shorts, 18 per page.
add_action( 'pre_get_posts', function ( WP_Query $q ) {
	if ( is_admin() || ! $q->is_main_query() ) {
		return;
	}
	if ( $q->is_tax( 'spa_video_type' ) ) {
		$q->set( 'post_type', 'spa_video' );
		$q->set( 'posts_per_page', 'short' === $q->get( 'spa_video_type' ) ? 18 : 12 );
		return;
	}
	if ( $q->is_post_type_archive( 'spa_video' ) ) {
		$q->set( 'tax_query', array( array( 'taxonomy' => 'spa_video_type', 'field' => 'slug', 'terms' => 'long' ) ) );
		$q->set( 'posts_per_page', 12 );
	}
} );

/** The effective type of a video post: its term, else derived from duration. */
function spa_video_type( $post_id ) {
	$terms = wp_get_object_terms( $post_id, 'spa_video_type', array( 'fields' => 'slugs' ) );
	if ( ! is_wp_error( $terms ) && ! empty( $terms ) ) {
		return in_array( 'short', $terms, true ) ? 'short' : 'long';
	}
	return (int) get_post_meta( $post_id, '_spa_duration', true ) <= SPA_SHORT_MAX_SECONDS ? 'short' : 'long';
}

/* ------------------------------------------------------------------------
 * Edit screen: the "YouTube sync" box (type override + sync status).
 * --------------------------------------------------------------------- */

add_action( 'add_meta_boxes_spa_video', function () {
	add_meta_box( 'spa_video_sync', 'YouTube sync', 'spa_video_meta_box', 'spa_video', 'side', 'high' );
} );

function spa_video_meta_box( WP_Post $post ) {
	$yt       = (string) get_post_meta( $post->ID, '_spa_youtube_id', true );
	$override = (string) get_post_meta( $post->ID, '_spa_type_override', true );
	$duration = (int) get_post_meta( $post->ID, '_spa_duration', true );
	$edited   = $yt && md5( $post->post_content ) !== get_post_meta( $post->ID, '_spa_imported_hash', true );
	wp_nonce_field( 'spa_video_meta', 'spa_video_meta_nonce' );
	?>
	<p>
		<label for="spa_youtube_id"><strong>YouTube video id</strong></label><br>
		<input type="text" id="spa_youtube_id" name="spa_youtube_id" value="<?php echo esc_attr( $yt ); ?>" maxlength="11" style="width:100%" <?php echo $yt ? 'readonly' : ''; ?>>
		<?php if ( $yt ) : ?>
			<a href="<?php echo esc_url( 'https://www.youtube.com/watch?v=' . $yt ); ?>" target="_blank" rel="noopener">Open on YouTube</a>
			<?php if ( $duration ) : ?> · <?php echo esc_html( spa_format_duration( $duration ) ); ?><?php endif; ?>
		<?php endif; ?>
	</p>
	<p>
		<label for="spa_type_override"><strong>Show as</strong></label><br>
		<select id="spa_type_override" name="spa_type_override" style="width:100%">
			<option value="" <?php selected( $override, '' ); ?>>Automatic (Short if 3:00 or less)</option>
			<option value="long" <?php selected( $override, 'long' ); ?>>Long-form video</option>
			<option value="short" <?php selected( $override, 'short' ); ?>>Short</option>
		</select>
	</p>
	<p style="color:#646970">
		<?php if ( $edited ) : ?>
			You have edited the notes, so the hourly sync no longer changes this video's text. Title, thumbnail and date still follow YouTube.
		<?php else : ?>
			The notes come from the YouTube description and follow it until you edit them here.
		<?php endif; ?>
	</p>
	<?php
	spa_sync_status_line();
}

add_action( 'save_post_spa_video', function ( $post_id ) {
	if ( ! isset( $_POST['spa_video_meta_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['spa_video_meta_nonce'] ) ), 'spa_video_meta' ) ) {
		return;
	}
	if ( ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) || ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	$yt = isset( $_POST['spa_youtube_id'] ) ? preg_replace( '/[^A-Za-z0-9_-]/', '', wp_unslash( $_POST['spa_youtube_id'] ) ) : '';
	if ( 11 === strlen( $yt ) && ! get_post_meta( $post_id, '_spa_youtube_id', true ) ) {
		update_post_meta( $post_id, '_spa_youtube_id', $yt );
	}

	$override = isset( $_POST['spa_type_override'] ) ? sanitize_key( wp_unslash( $_POST['spa_type_override'] ) ) : '';
	if ( ! in_array( $override, array( '', 'long', 'short' ), true ) ) {
		$override = '';
	}
	update_post_meta( $post_id, '_spa_type_override', $override );

	if ( $override ) {
		wp_set_object_terms( $post_id, $override, 'spa_video_type' );
	} elseif ( get_post_meta( $post_id, '_spa_duration', true ) ) {
		$auto = (int) get_post_meta( $post_id, '_spa_duration', true ) <= SPA_SHORT_MAX_SECONDS ? 'short' : 'long';
		wp_set_object_terms( $post_id, $auto, 'spa_video_type' );
	}
} );

// Videos list: a duration column beside the type column.
add_filter( 'manage_spa_video_posts_columns', function ( $cols ) {
	$cols['spa_duration'] = 'Length';
	return $cols;
} );
add_action( 'manage_spa_video_posts_custom_column', function ( $col, $post_id ) {
	if ( 'spa_duration' === $col ) {
		$d = (int) get_post_meta( $post_id, '_spa_duration', true );
		echo $d ? esc_html( spa_format_duration( $d ) ) : '—';
	}
}, 10, 2 );
