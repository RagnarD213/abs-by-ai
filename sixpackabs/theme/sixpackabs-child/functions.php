<?php
/**
 * SixPackAbs Child — bootstrap.
 *
 * Video-first sixpackabs.com on top of Twenty Twenty-Five:
 *   inc/render.php         shared markup helpers (cards, thumbnails, links, durations)
 *   inc/content-model.php  `spa_video` post type (/videos/<slug>/), long/short type, /shorts/ route, meta box
 *   inc/sync.php           hourly import from absbyai.com/api/sixpackabs/{channel,instagram}.json
 *   inc/blocks.php         the server-rendered blocks the templates are built from (blocks/<name>/block.json)
 *   inc/head.php           PostHog, favicon, VideoObject JSON-LD, og:video
 *
 * Deploy + rollback: sixpackabs/README.md in the Abs By AI repo.
 */

defined( 'ABSPATH' ) || exit;

define( 'SPA_THEME_VERSION', '1.0.0' );
define( 'SPA_DIR', get_stylesheet_directory() );
define( 'SPA_URI', get_stylesheet_directory_uri() );

require SPA_DIR . '/inc/render.php';
require SPA_DIR . '/inc/content-model.php';
require SPA_DIR . '/inc/sync.php';
require SPA_DIR . '/inc/blocks.php';
require SPA_DIR . '/inc/head.php';

/** Cache-busting version for a theme asset: theme version + file mtime. */
function spa_asset_version( $relative ) {
	$path = SPA_DIR . '/' . ltrim( $relative, '/' );
	return SPA_THEME_VERSION . '.' . ( file_exists( $path ) ? filemtime( $path ) : '0' );
}

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'spa-site', SPA_URI . '/assets/css/site.css', array(), spa_asset_version( 'assets/css/site.css' ) );
	wp_enqueue_script(
		'spa-site',
		SPA_URI . '/assets/js/site.js',
		array(),
		spa_asset_version( 'assets/js/site.js' ),
		array( 'strategy' => 'defer', 'in_footer' => true )
	);
} );

add_action( 'enqueue_block_editor_assets', function () {
	wp_enqueue_script(
		'spa-editor',
		SPA_URI . '/assets/js/editor.js',
		array( 'wp-blocks', 'wp-element', 'wp-server-side-render' ),
		spa_asset_version( 'assets/js/editor.js' ),
		true
	);
} );

add_action( 'after_setup_theme', function () {
	// The same stylesheet inside the editor, so the server-rendered blocks preview as they ship.
	add_editor_style( 'assets/css/site.css' );

	// Shorts cards are 9:16 but Dan's cover art is 16:9, so the card shows only the
	// middle third of the width. Asking for the full cover wastes two thirds of the
	// pixels and still renders soft (a 768 px file leaves 243 px doing a 358 px job).
	// This size is cropped to the card's shape server-side: every pixel is visible,
	// sharp on 2x and 3x screens, and lighter than the full cover. 405x720 is exactly
	// 9:16 and the tallest crop a 1280x720 cover can give without upscaling.
	add_image_size( 'spa-short', 405, 720, true );
} );

// The covers are 1280x720, so a 9:16 crop tops out at 405x720 — there is no more
// detail in the file. WordPress.com's image CDN still offers 2x and 3x variants of
// it, which are upscales: on a 3x phone the browser would fetch 179 KB instead of
// 68 KB and see exactly the same picture. Cap this size at its true resolution.
add_filter( 'wp_calculate_image_srcset', function ( $sources, $size_array ) {
	if ( ! is_array( $sources ) || ! is_array( $size_array ) ) {
		return $sources;
	}
	if ( 405 !== (int) ( $size_array[0] ?? 0 ) || 720 !== (int) ( $size_array[1] ?? 0 ) ) {
		return $sources;
	}
	foreach ( array_keys( $sources ) as $width ) {
		if ( (int) $width > 405 ) {
			unset( $sources[ $width ] );
		}
	}
	return $sources;
}, 999, 2 );

// First activation (and every re-activation): register the model, make sure both
// type terms exist, rebuild the rewrite rules so /videos/ and /shorts/ resolve,
// and queue the first sync a minute out.
add_action( 'after_switch_theme', function () {
	spa_register_content_model();
	spa_ensure_video_terms();
	flush_rewrite_rules();
	if ( ! wp_next_scheduled( 'spa_sync' ) ) {
		wp_schedule_event( time() + 60, 'hourly', 'spa_sync' );
	}
} );
