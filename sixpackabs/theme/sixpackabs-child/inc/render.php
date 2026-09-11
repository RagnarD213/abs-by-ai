<?php
/**
 * Shared markup helpers for the blocks in inc/blocks.php: canonical links,
 * outbound-click tracking attributes, durations, video queries, thumbnails
 * and the card markup every video section reuses.
 */

defined( 'ABSPATH' ) || exit;

function spa_img_uri( $file ) {
	return SPA_URI . '/assets/img/' . $file;
}

/**
 * Every destination the design links to. App links go to the SixPackAbs-skinned
 * app with the UTM pattern already in use; `$campaign` = header|bio|footer|menu.
 */
function spa_url( $key, $campaign = '' ) {
	switch ( $key ) {
		case 'subscribe':
			return 'https://www.youtube.com/@absbyai?sub_confirmation=1';
		case 'youtube':
			return 'https://www.youtube.com/@absbyai';
		case 'instagram':
			return 'https://www.instagram.com/danrosefit/';
		case 'app':
			return 'https://try.sixpackabs.com/?utm_source=sixpackabs&utm_medium=homepage&utm_campaign=' . rawurlencode( $campaign ? $campaign : 'header' );
		case 'videos':
			return home_url( '/videos/' );
		case 'shorts':
			return home_url( '/shorts/' );
		case 'about':
			return home_url( '/pages/about-us/' );
		case 'calculator':
			return home_url( '/abs-calculator/' );
		case 'collab':
			return home_url( '/partner-with-us/' );
		case 'contact':
			return home_url( '/contact-us/' );
		case 'archive':
			return home_url( '/blog/' );
		case 'disclaimer':
			return 'https://absbyai.com/disclaimer';
	}
	return home_url( '/' );
}

/** data-* attributes site.js turns into a PostHog `outbound_click`. */
function spa_track( $target, $placement ) {
	return sprintf( ' data-spa-target="%s" data-spa-placement="%s"', esc_attr( $target ), esc_attr( $placement ) );
}

function spa_subscribe_button( $placement, $class = '' ) {
	return sprintf(
		'<a class="spa-btn spa-btn--red %1$s" href="%2$s" target="_blank" rel="noopener"%3$s><span class="spa-tri" aria-hidden="true"></span>Subscribe</a>',
		esc_attr( $class ),
		esc_url( spa_url( 'subscribe' ) ),
		spa_track( 'youtube_subscribe', $placement )
	);
}

function spa_app_link( $placement, $label, $class ) {
	return sprintf(
		'<a class="%1$s" href="%2$s"%3$s>%4$s</a>',
		esc_attr( $class ),
		esc_url( spa_url( 'app', $placement ) ),
		spa_track( 'try_app', $placement ),
		esc_html( $label )
	);
}

function spa_format_duration( $seconds ) {
	$s = max( 0, (int) $seconds );
	$h = intdiv( $s, 3600 );
	$m = intdiv( $s % 3600, 60 );
	$r = $s % 60;
	return $h ? sprintf( '%d:%02d:%02d', $h, $m, $r ) : sprintf( '%d:%02d', $m, $r );
}

function spa_iso_duration( $seconds ) {
	$s = max( 0, (int) $seconds );
	$h = intdiv( $s, 3600 );
	$m = intdiv( $s % 3600, 60 );
	$r = $s % 60;
	return 'PT' . ( $h ? $h . 'H' : '' ) . ( $m ? $m . 'M' : '' ) . ( ( $r || ( ! $h && ! $m ) ) ? $r . 'S' : '' );
}

/** Newest published videos of one type. */
function spa_get_videos( $type, $count, $offset = 0, $exclude = array() ) {
	$q = new WP_Query( array(
		'post_type'           => 'spa_video',
		'post_status'         => 'publish',
		'posts_per_page'      => (int) $count,
		'offset'              => (int) $offset,
		'post__not_in'        => array_map( 'intval', (array) $exclude ),
		'orderby'             => 'date',
		'order'               => 'DESC',
		'no_found_rows'       => true,
		'ignore_sticky_posts' => true,
		'tax_query'           => array( array( 'taxonomy' => 'spa_video_type', 'field' => 'slug', 'terms' => $type ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
	) );
	return $q->posts;
}

/**
 * Thumbnail <img>. Always Dan's own cover art (the YouTube custom thumbnail,
 * stored as the featured image); `$shape` only picks the `sizes` hint. Shorts
 * used to use YouTube's vertical thumbnail, but that is a frame grabbed from the
 * video — mid-sentence, with burned captions — so Dan's cover is used for those
 * too and cropped to the 9:16 card (his call, 2026-09-11). Alt is empty: every
 * card shows the title as text inside the same link.
 */
function spa_video_img( $post_id, $shape, $sizes, $eager = false ) {
	$att = (int) get_post_thumbnail_id( $post_id );
	$attrs = array(
		'class'    => 'spa-thumb__img',
		'alt'      => '',
		'sizes'    => $sizes,
		'loading'  => $eager ? 'eager' : 'lazy',
		'decoding' => 'async',
	);
	if ( $eager ) {
		$attrs['fetchpriority'] = 'high';
	}
	if ( $att ) {
		return wp_get_attachment_image( $att, 'full', false, $attrs );
	}
	// Not downloaded yet (the first sync is still running): YouTube's own copy.
	$url = get_post_meta( $post_id, '_spa_thumb_url', true );
	if ( ! $url ) {
		return '';
	}
	return sprintf(
		'<img class="spa-thumb__img" src="%1$s" alt="" loading="%2$s" decoding="async"%3$s>',
		esc_url( $url ),
		$eager ? 'eager' : 'lazy',
		$eager ? ' fetchpriority="high"' : ''
	);
}

function spa_duration_pill( $post_id, $class = 'spa-pill' ) {
	$d = (int) get_post_meta( $post_id, '_spa_duration', true );
	if ( ! $d ) {
		return '';
	}
	return '<span class="' . esc_attr( $class ) . '"><span class="screen-reader-text">Length </span>' . esc_html( spa_format_duration( $d ) ) . '</span>';
}

function spa_section_head( $title, $id, $link_url, $link_html, $level = 2 ) {
	return sprintf(
		'<div class="spa-sec__head"><h%1$d class="spa-h2" id="%2$s">%3$s</h%1$d><a class="spa-all" href="%4$s">%5$s</a></div>',
		(int) $level,
		esc_attr( $id ),
		esc_html( $title ),
		esc_url( $link_url ),
		$link_html
	);
}

/** Long-form row: 16:9 thumbnail left, title (+ date on desktop) right. */
function spa_row_card( WP_Post $p ) {
	return sprintf(
		'<a class="spa-row" href="%1$s"><span class="spa-thumb spa-thumb--row">%2$s%3$s</span><span class="spa-row__text"><span class="spa-row__title">%4$s</span><span class="spa-row__date">%5$s</span></span></a>',
		esc_url( get_permalink( $p ) ),
		spa_video_img( $p->ID, 'landscape', '(min-width: 1024px) 150px, 140px' ),
		spa_duration_pill( $p->ID, 'spa-pill spa-pill--sm' ),
		esc_html( get_the_title( $p ) ),
		esc_html( get_the_date( 'M j, Y', $p ) )
	);
}

/** Short card: 9:16 thumbnail with a dim play circle, title under it. */
function spa_short_card( WP_Post $p, $sizes = '(min-width: 1024px) 180px, 124px' ) {
	return sprintf(
		'<a class="spa-short" href="%1$s"><span class="spa-thumb spa-thumb--short">%2$s<span class="spa-play spa-play--dim" aria-hidden="true"></span></span><span class="spa-short__title">%3$s</span></a>',
		esc_url( get_permalink( $p ) ),
		spa_video_img( $p->ID, 'portrait', $sizes ),
		esc_html( get_the_title( $p ) )
	);
}

/** Archive card for long-form: big 16:9 thumbnail, title, date · length. */
function spa_grid_card( WP_Post $p ) {
	$d = (int) get_post_meta( $p->ID, '_spa_duration', true );
	return sprintf(
		'<a class="spa-card" href="%1$s"><span class="spa-thumb spa-thumb--card">%2$s<span class="spa-play spa-play--red spa-play--md" aria-hidden="true"></span>%3$s</span><span class="spa-card__text"><span class="spa-card__title">%4$s</span><span class="spa-card__meta">%5$s</span></span></a>',
		esc_url( get_permalink( $p ) ),
		spa_video_img( $p->ID, 'landscape', '(min-width: 1024px) 360px, (min-width: 768px) 50vw, 100vw' ),
		spa_duration_pill( $p->ID ),
		esc_html( get_the_title( $p ) ),
		esc_html( get_the_date( 'M j, Y', $p ) . ( $d ? ' · ' . spa_format_duration( $d ) : '' ) )
	);
}

/** Channel numbers the sync stored (subscriber count for the Subscribe CTA). */
function spa_channel() {
	$c = get_option( 'spa_channel' );
	return is_array( $c ) ? $c : array( 'subscriberCount' => null, 'videoCount' => null );
}
