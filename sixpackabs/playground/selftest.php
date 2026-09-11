<?php
/**
 * Self-test for the sixpackabs-child sync + edit-screen logic, run inside a
 * throwaway WordPress Playground with fixture feeds (no network, no real site):
 *
 *   npx -y @wp-playground/cli@3.1.53 php \
 *     --mount-dir sixpackabs/theme/sixpackabs-child /wordpress/wp-content/themes/sixpackabs-child \
 *     --mount-dir sixpackabs/playground /spa-playground \
 *     --blueprint=sixpackabs/playground/selftest-blueprint.json /spa-playground/selftest.php
 *
 * Prints one line per check and "SELFTEST PASS n/n" or "SELFTEST FAIL".
 */

require '/wordpress/wp-load.php';

$checks = 0;
$fails  = 0;
function spa_t( $name, $ok, $detail = '' ) {
	global $checks, $fails;
	$checks++;
	if ( ! $ok ) {
		$fails++;
	}
	echo ( $ok ? '  ok   ' : '  FAIL ' ) . $name . ( $ok || '' === $detail ? '' : ' — ' . $detail ) . "\n";
}

if ( 'sixpackabs-child' !== get_stylesheet() || ! function_exists( 'spa_upsert_video' ) ) {
	echo "SELFTEST FAIL — theme not active\n";
	exit( 1 );
}
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/template.php';
spa_register_content_model();
spa_ensure_video_terms();

// Fixture feeds served through pre_http_request — nothing leaves the machine.
$GLOBALS['spa_fixture'] = array( 'channel' => array(), 'instagram' => array() );
add_filter( 'pre_http_request', function ( $pre, $args, $url ) {
	foreach ( array( 'channel', 'instagram' ) as $name ) {
		if ( SPA_FEED_BASE . '/' . $name . '.json' === $url ) {
			return array( 'headers' => array(), 'body' => wp_json_encode( $GLOBALS['spa_fixture'][ $name ] ), 'response' => array( 'code' => 200, 'message' => 'OK' ), 'cookies' => array(), 'filename' => null );
		}
	}
	return new WP_Error( 'selftest_offline', 'selftest blocks ' . $url );
}, 10, 3 );

function spa_fx( $id, $secs, $desc, $title = null, $published = '2026-09-06T14:00:00Z' ) {
	return array(
		'id' => $id, 'title' => $title ? $title : "Title $id", 'description' => $desc, 'publishedAt' => $published,
		'durationSeconds' => $secs, 'type' => $secs <= 180 ? 'short' : 'long', 'embeddable' => true,
		'thumbnails' => array( 'maxres' => '', 'high' => '', 'portrait' => '', 'version' => null ),
	);
}
function spa_post_for( $yt ) {
	return spa_find_video( $yt );
}
function spa_terms_of( $post_id ) {
	return wp_get_object_terms( $post_id, 'spa_video_type', array( 'fields' => 'slugs' ) );
}

echo "sixpackabs-child selftest\n";
wp_set_current_user( 0 ); // the sync runs from cron: no user, kses active

// --- terms
$short_term = get_term_by( 'slug', 'short', 'spa_video_type' );
spa_t( 'type terms exist with archive names', $short_term && 'Shorts' === $short_term->name && get_term_by( 'slug', 'long', 'spa_video_type' ) );

// --- description → blocks
$blocks = spa_description_to_blocks( "First line.\nSecond line.\n\nSee https://absbyai.com/?a=1&b=2. #abs" );
spa_t( 'description: two paragraph blocks', 2 === substr_count( $blocks, '<!-- wp:paragraph -->' ) );
spa_t( 'description: single newline → <br>', false !== strpos( $blocks, 'First line.<br>' ) );
spa_t( 'description: URL linked nofollow, trailing period kept outside', false !== strpos( $blocks, 'rel="nofollow noopener">https://absbyai.com/?a=1&amp;b=2</a>. #abs' ) );
spa_t( 'description: empty stays empty', '' === spa_description_to_blocks( '   ' ) );
spa_t( 'excerpt: first paragraph, URLs removed', 'Watch this. It works.' === spa_description_excerpt( "Watch this. https://x.co It works.\n\nMore." ) );

// --- create / unchanged / update
$A = 'AAAAAAAAAAA';
$B = 'BBBBBBBBBBB';
$C = 'CCCCCCCCCCC';
spa_t( 'create long video', 'created' === spa_upsert_video( spa_fx( $A, 800, "Intro A.\n\nMore A." ) ) );
$pa = spa_post_for( $A );
spa_t( 'created as published, dated like YouTube', $pa && 'publish' === $pa->post_status && '2026-09-06 14:00:00' === $pa->post_date_gmt );
spa_t( 'created with long term + meta', array( 'long' ) === spa_terms_of( $pa->ID ) && 800 === (int) get_post_meta( $pa->ID, '_spa_duration', true ) );
spa_t( 'import hash recorded', md5( $pa->post_content ) === get_post_meta( $pa->ID, '_spa_imported_hash', true ) );
$rerun = spa_upsert_video( spa_fx( $A, 800, "Intro A.\n\nMore A." ) );
spa_t( 're-run with same data is unchanged', 'unchanged' === $rerun, $rerun . ' because: ' . implode( ', ', (array) ( $GLOBALS['spa_upsert_reasons'] ?? array() ) ) );
spa_t( 'new description updates untouched notes', 'updated' === spa_upsert_video( spa_fx( $A, 800, "Intro A v2.\n\nMore A." ) ) && false !== strpos( spa_post_for( $A )->post_content, 'Intro A v2.' ) );
spa_t( 'excerpt follows untouched', 'Intro A v2.' === spa_post_for( $A )->post_excerpt );

// --- Dan edits the notes: the sync must never overwrite them
wp_update_post( array( 'ID' => $pa->ID, 'post_content' => '<!-- wp:paragraph --><p>Dan wrote these notes.</p><!-- /wp:paragraph -->' ) );
spa_upsert_video( spa_fx( $A, 800, "Intro A v3 from YouTube.\n\nMore A.", 'New YouTube title' ) );
$pa = spa_post_for( $A );
spa_t( "Dan's edited notes survive a new description", false !== strpos( $pa->post_content, 'Dan wrote these notes.' ) && false === strpos( $pa->post_content, 'v3' ) );
spa_t( 'title still follows YouTube; slug (URL) unchanged', 'New YouTube title' === $pa->post_title && 'title-aaaaaaaaaaa' === $pa->post_name );
spa_t( 'untouched excerpt still follows YouTube', 'Intro A v3 from YouTube.' === $pa->post_excerpt );

// --- type rules
spa_upsert_video( spa_fx( $B, 180, 'Short B.' ) );
spa_upsert_video( spa_fx( $C, 181, 'Long C.' ) );
spa_t( '180 s = short, 181 s = long', array( 'short' ) === spa_terms_of( spa_post_for( $B )->ID ) && array( 'long' ) === spa_terms_of( spa_post_for( $C )->ID ) );
update_post_meta( spa_post_for( $C )->ID, '_spa_type_override', 'short' );
wp_set_object_terms( spa_post_for( $C )->ID, 'short', 'spa_video_type' );
spa_upsert_video( spa_fx( $C, 181, 'Long C.' ) );
spa_t( 'type override survives the sync', array( 'short' ) === spa_terms_of( spa_post_for( $C )->ID ) );

// --- a full sync run: leaving the feed → draft; returning → publish; Dan's own drafts stay drafts
$GLOBALS['spa_fixture']['channel'] = array( 'channel' => array( 'subscriberCount' => 3030, 'videoCount' => 3 ), 'videos' => array( spa_fx( $A, 800, 'x' ), spa_fx( $B, 180, 'Short B.' ), spa_fx( $C, 181, 'Long C.' ) ) );
spa_sync_videos();
$GLOBALS['spa_fixture']['channel']['videos'] = array( spa_fx( $A, 800, 'x' ), spa_fx( $B, 180, 'Short B.' ) );
$r = spa_sync_videos();
spa_t( 'video that left the feed is drafted, not deleted', 'draft' === spa_post_for( $C )->post_status && 1 === $r['drafted'] );
$GLOBALS['spa_fixture']['channel']['videos'][] = spa_fx( $C, 181, 'Long C.' );
$r = spa_sync_videos();
spa_t( 'it comes back when public again', 'publish' === spa_post_for( $C )->post_status && 1 === $r['restored'] );
wp_update_post( array( 'ID' => spa_post_for( $B )->ID, 'post_status' => 'draft' ) );
spa_sync_videos();
spa_t( 'a video Dan drafted himself stays drafted', 'draft' === spa_post_for( $B )->post_status );
wp_trash_post( spa_post_for( $B )->ID );
$before = wp_count_posts( 'spa_video' );
spa_sync_videos();
$after = wp_count_posts( 'spa_video' );
spa_t( 'a trashed video is not re-created', (int) $before->publish === (int) $after->publish && 'trash' === spa_post_for( $B )->post_status );
$GLOBALS['spa_fixture']['channel']['videos'] = array();
$r = spa_sync_videos();
spa_t( 'an empty feed unpublishes nothing', 0 === $r['drafted'] && 'publish' === spa_post_for( $A )->post_status );
spa_t( 'subscriber count stored for the Subscribe box', 3030 === spa_channel()['subscriberCount'] );

// --- Instagram: only instagram.com permalinks are kept
$GLOBALS['spa_fixture']['instagram'] = array( 'images' => array(
	array( 'id' => '111', 'permalink' => 'https://evil.example/p/1/', 'imageUrl' => '', 'alt' => 'x' ),
	array( 'id' => '222', 'permalink' => 'https://www.instagram.com/p/2/', 'imageUrl' => '', 'alt' => 'y' ),
) );
$ig = spa_sync_instagram();
spa_t( 'instagram: foreign permalink rejected, missing image skipped', 0 === $ig['kept'] && 2 === $ig['feed'] );

// --- edit screen: meta box renders and the override saves
wp_set_current_user( 1 );
ob_start();
spa_video_meta_box( spa_post_for( $A ) );
$box = ob_get_clean();
spa_t( 'meta box renders override select + edited-notes notice + Sync now', false !== strpos( $box, 'name="spa_type_override"' ) && false !== strpos( $box, 'You have edited the notes' ) && false !== strpos( $box, 'Sync now' ) );
$_POST = array( 'spa_video_meta_nonce' => wp_create_nonce( 'spa_video_meta' ), 'spa_type_override' => 'short', 'spa_youtube_id' => '' );
do_action( 'save_post_spa_video', spa_post_for( $A )->ID, spa_post_for( $A ), true );
spa_t( 'saving the box sets the override and the term', 'short' === get_post_meta( spa_post_for( $A )->ID, '_spa_type_override', true ) && array( 'short' ) === spa_terms_of( spa_post_for( $A )->ID ) );
$_POST['spa_type_override'] = '';
do_action( 'save_post_spa_video', spa_post_for( $A )->ID, spa_post_for( $A ), true );
spa_t( 'clearing the override returns to automatic (800 s → long)', array( 'long' ) === spa_terms_of( spa_post_for( $A )->ID ) );
$_POST = array();

// --- empty states
spa_t( 'instagram grid renders nothing without images', '' === spa_render_instagram_grid() );
spa_t( 'featured video renders for the newest long-form', false !== strpos( spa_render_featured_video(), 'spa-featured' ) );

echo ( $fails ? "SELFTEST FAIL $fails/$checks\n" : "SELFTEST PASS $checks/$checks\n" );
