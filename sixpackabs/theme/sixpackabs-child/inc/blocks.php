<?php
/**
 * The server-rendered blocks the templates are assembled from. Each has a
 * blocks/<name>/block.json (so it can be inserted and previewed in the editor
 * via assets/js/editor.js) and a spa_render_<name>() callback below. No build
 * step. Every pixel value lives in assets/css/site.css; the spec is
 * Docs/sixpackabs-redesign/DESIGN_HANDOFF.md (#2a mobile / #2b desktop).
 *
 * Empty states: a section whose data is missing returns '' — the headline,
 * bio and newsletter always render, video/Instagram sections disappear.
 */

defined( 'ABSPATH' ) || exit;

const SPA_BLOCKS = array(
	'site-header', 'site-footer', 'featured-video', 'video-list', 'shorts-rail', 'instagram-grid',
	'bio', 'newsletter', 'subscribe-button', 'subscribe-cta', 'video-hero', 'video-grid', 'more-videos',
);

add_action( 'init', function () {
	foreach ( SPA_BLOCKS as $name ) {
		register_block_type( SPA_DIR . '/blocks/' . $name, array( 'render_callback' => 'spa_render_' . str_replace( '-', '_', $name ) ) );
	}
} );

function spa_nav_items() {
	return array(
		array( 'label' => 'Videos', 'url' => spa_url( 'videos' ) ),
		array( 'label' => 'Shorts', 'url' => spa_url( 'shorts' ) ),
		array( 'label' => 'About Dan', 'url' => spa_url( 'about' ) ),
		array( 'label' => 'Abs Calculator', 'url' => spa_url( 'calculator' ) ),
		array( 'label' => 'Collab', 'url' => spa_url( 'collab' ) ),
	);
}

function spa_logo( $height_class, $loading = 'eager' ) {
	return sprintf(
		// fetchpriority="auto" stops WordPress promoting the logo; the featured thumbnail is the LCP image.
		'<a class="spa-logo %1$s" href="%2$s" aria-label="SixPackAbs.com home"><img src="%3$s" alt="SixPackAbs.com" width="1189" height="147" loading="%4$s" fetchpriority="auto" decoding="async"></a>',
		esc_attr( $height_class ),
		esc_url( home_url( '/' ) ),
		esc_url( spa_img_uri( 'sixpackabs-logo.webp' ) ),
		esc_attr( $loading )
	);
}

/* ------------------------------------------------------------------ header */

function spa_render_site_header() {
	$nav = spa_nav_items();
	ob_start();
	?>
<div class="spa-header">
	<div class="spa-wrap spa-header__inner">
		<?php echo spa_logo( 'spa-logo--header' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
		<nav class="spa-nav" aria-label="Main">
			<?php foreach ( $nav as $item ) : ?>
				<a href="<?php echo esc_url( $item['url'] ); ?>"><?php echo esc_html( $item['label'] ); ?></a>
			<?php endforeach; ?>
		</nav>
		<div class="spa-header__actions">
			<?php echo spa_app_link( 'header', 'Try the AI App', 'spa-btn spa-btn--outline spa-header__app' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			<?php echo spa_subscribe_button( 'header', 'spa-header__sub' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			<button type="button" class="spa-burger" aria-expanded="false" aria-controls="spa-menu" aria-label="Open menu"><span></span><span></span><span></span></button>
		</div>
	</div>
</div>
<div class="spa-menu" id="spa-menu" role="dialog" aria-modal="true" aria-label="Menu" hidden>
	<div class="spa-menu__backdrop" data-spa-menu-close></div>
	<div class="spa-menu__panel">
		<div class="spa-menu__top">
			<?php echo spa_logo( 'spa-logo--header', 'lazy' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			<button type="button" class="spa-menu__close" data-spa-menu-close aria-label="Close menu"><span aria-hidden="true"></span></button>
		</div>
		<nav class="spa-menu__nav" aria-label="Menu">
			<?php foreach ( $nav as $item ) : ?>
				<a href="<?php echo esc_url( $item['url'] ); ?>"><?php echo esc_html( $item['label'] ); ?></a>
			<?php endforeach; ?>
		</nav>
		<div class="spa-menu__actions">
			<?php echo spa_app_link( 'menu', 'Try the AI App', 'spa-btn spa-btn--outline spa-btn--block' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			<?php echo spa_subscribe_button( 'menu', 'spa-btn--block' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
		</div>
	</div>
</div>
	<?php
	return ob_get_clean();
}

/* ------------------------------------------------------------------ footer */

function spa_render_site_footer() {
	$yt  = '<a href="' . esc_url( spa_url( 'youtube' ) ) . '" target="_blank" rel="noopener"' . spa_track( 'youtube_watch', 'footer' ) . '>YouTube</a>';
	$ig  = '<a href="' . esc_url( spa_url( 'instagram' ) ) . '" target="_blank" rel="noopener"' . spa_track( 'instagram', 'footer' ) . '>Instagram</a>';
	$app = spa_app_link( 'footer', 'Try the AI App', '' );
	$cal = '<a href="' . esc_url( spa_url( 'calculator' ) ) . '">Abs Calculator</a>';
	$con = '<a href="' . esc_url( spa_url( 'contact' ) ) . '">Contact / Collab</a>';
	$arc = '<a href="' . esc_url( spa_url( 'archive' ) ) . '">Article archive</a>';
	$dis = '<a href="' . esc_url( spa_url( 'disclaimer' ) ) . '">Disclaimer</a>';
	return '<div class="spa-footer"><div class="spa-wrap spa-footer__inner">'
		. '<nav class="spa-footer__m" aria-label="Footer">' . $yt . $ig . $app . $cal . $con . $arc . '</nav>'
		. '<nav class="spa-footer__d" aria-label="Footer"><div class="spa-footer__group">' . $yt . $ig . $con . $app . '</div><div class="spa-footer__group">' . $arc . $cal . $dis . '</div></nav>'
		. '<p class="spa-footer__copy">© ' . esc_html( wp_date( 'Y' ) ) . ' SixPackAbs.com · Georgetown, TX</p>'
		. '</div></div>';
}

/* ------------------------------------------------------------------ homepage */

function spa_render_featured_video() {
	$posts = spa_get_videos( 'long', 1 );
	if ( ! $posts ) {
		return '';
	}
	$p = $posts[0];
	return sprintf(
		'<a class="spa-featured" href="%1$s"><span class="spa-thumb spa-thumb--featured">%2$s<span class="spa-play spa-play--red spa-play--lg" aria-hidden="true"></span>%3$s</span><span class="spa-featured__text"><span class="spa-eyebrow">Latest video</span><h2 class="spa-featured__title">%4$s</h2><span class="spa-featured__excerpt">%5$s</span><span class="spa-cue">Watch + read the notes →</span></span></a>',
		esc_url( get_permalink( $p ) ),
		spa_video_img( $p->ID, 'landscape', '(min-width: 1280px) 724px, (min-width: 1024px) calc(100vw - 556px), calc(100vw - 62px)', true ),
		spa_duration_pill( $p->ID, 'spa-pill spa-pill--lg' ),
		esc_html( get_the_title( $p ) ),
		esc_html( wp_strip_all_tags( get_the_excerpt( $p ) ) )
	);
}

function spa_render_video_list( $attrs ) {
	$type    = ( isset( $attrs['type'] ) && 'short' === $attrs['type'] ) ? 'short' : 'long';
	$count   = isset( $attrs['count'] ) ? max( 1, (int) $attrs['count'] ) : 5;
	$offset  = isset( $attrs['offset'] ) ? max( 0, (int) $attrs['offset'] ) : 1;
	$heading = isset( $attrs['heading'] ) && '' !== $attrs['heading'] ? $attrs['heading'] : 'More free videos';
	$posts   = spa_get_videos( $type, $count, $offset );
	if ( ! $posts ) {
		return '';
	}
	$archive = spa_url( 'short' === $type ? 'shorts' : 'videos' );
	return '<aside class="spa-rail" aria-labelledby="spa-rail-h">'
		. spa_section_head( $heading, 'spa-rail-h', $archive, 'All →' )
		. '<div class="spa-rail__rows">' . implode( '', array_map( 'spa_row_card', $posts ) ) . '</div>'
		. '<a class="spa-btn spa-btn--outline spa-btn--block spa-rail__all" href="' . esc_url( $archive ) . '">Watch all videos</a>'
		. '</aside>';
}

function spa_render_shorts_rail( $attrs ) {
	$count = isset( $attrs['count'] ) ? max( 1, (int) $attrs['count'] ) : 6;
	$posts = spa_get_videos( 'short', $count );
	if ( ! $posts ) {
		return '';
	}
	$cards = '';
	foreach ( $posts as $p ) {
		$cards .= spa_short_card( $p, '(min-width: 1280px) 179px, (min-width: 1024px) calc((100vw - 208px) / 6), (min-width: 768px) 25vw, 124px' );
	}
	return '<section class="spa-band spa-shorts" aria-labelledby="spa-shorts-h"><div class="spa-wrap spa-shorts__inner">'
		. spa_section_head( 'Shorts', 'spa-shorts-h', spa_url( 'shorts' ), 'All<span class="spa-d-only"> shorts</span> →' )
		. '<div class="spa-shorts__rail">' . $cards . '<span class="spa-shorts__end" aria-hidden="true"></span></div>'
		. '</div></section>';
}

function spa_render_instagram_grid() {
	$items = get_option( 'spa_instagram', array() );
	if ( ! is_array( $items ) || ! $items ) {
		return '';
	}
	$cells = '';
	foreach ( array_slice( $items, 0, 6 ) as $it ) {
		$img = wp_get_attachment_image( (int) $it['attachment_id'], 'medium_large', false, array(
			'class'    => 'spa-ig__img',
			'alt'      => $it['alt'] ? $it['alt'] : 'Dan Rose on Instagram',
			'sizes'    => '(min-width: 1280px) 184px, (min-width: 1024px) calc((100vw - 178px) / 6), calc((100vw - 48px) / 3)',
			'loading'  => 'lazy',
			'decoding' => 'async',
		) );
		if ( ! $img ) {
			continue;
		}
		$cells .= '<a class="spa-ig__cell" href="' . esc_url( $it['permalink'] ) . '" target="_blank" rel="noopener"' . spa_track( 'instagram', 'grid' ) . '>' . $img . '</a>';
	}
	if ( ! $cells ) {
		return '';
	}
	return '<section class="spa-sec spa-ig" aria-labelledby="spa-ig-h"><div class="spa-wrap spa-ig__inner">'
		. '<div class="spa-sec__head"><h2 class="spa-h2" id="spa-ig-h">On Instagram</h2><a class="spa-all" href="' . esc_url( spa_url( 'instagram' ) ) . '" target="_blank" rel="noopener"' . spa_track( 'instagram', 'grid' ) . '>@danrosefit →</a></div>'
		. '<div class="spa-ig__grid">' . $cells . '</div>'
		. '</div></section>';
}

function spa_render_bio() {
	return '<section class="spa-bio" aria-labelledby="spa-bio-h"><div class="spa-wrap spa-bio__inner">'
		. sprintf(
			'<img class="spa-bio__photo" src="%1$s" srcset="%2$s 480w, %1$s 720w" sizes="(min-width: 1024px) 460px, (min-width: 768px) 300px, 100vw" width="720" height="864" alt="Dan Rose" loading="lazy" decoding="async">',
			esc_url( spa_img_uri( 'dan-founder.jpg' ) ),
			esc_url( spa_img_uri( 'dan-founder-480.jpg' ) )
		)
		. '<div class="spa-bio__text">'
		. '<h2 class="spa-bio__h" id="spa-bio-h">Meet SixPackAbs.com CEO Daniel Rose</h2>'
		. '<p class="spa-bio__p">Hi, I\'m Dan. I\'m one of the original founders of Six Pack Shortcuts and SixPackAbs.com, and I\'m back with a new YouTube channel. Subscribe to the channel to get new videos every week from me showing you how to lose your belly fat and get six pack abs.</p>'
		. '<div class="spa-bio__btns">'
		. spa_app_link( 'bio', 'Try Abs by AI free', 'spa-btn spa-btn--ink' )
		. '<a class="spa-btn spa-btn--outline" href="' . esc_url( spa_url( 'about' ) ) . '">Read my story</a>'
		. '</div></div></div></section>';
}

function spa_render_newsletter( $attrs ) {
	$placement = isset( $attrs['placement'] ) ? sanitize_key( $attrs['placement'] ) : 'home';
	$uid       = wp_unique_id( 'spa-news-' );
	return '<section class="spa-news" aria-labelledby="' . esc_attr( $uid ) . '-h"><div class="spa-wrap spa-news__wrap"><div class="spa-news__box">'
		. '<div class="spa-news__copy"><h2 class="spa-news__h" id="' . esc_attr( $uid ) . '-h">New video, new notes. One email each.</h2>'
		. '<p class="spa-news__sub">Get every new video plus the written breakdown.</p></div>'
		. '<div class="spa-news__formwrap">'
		. '<form class="spa-news__form" data-endpoint="https://absbyai.com/api/subscribe" data-placement="' . esc_attr( $placement ) . '" novalidate>'
		. '<label class="screen-reader-text" for="' . esc_attr( $uid ) . '-email">Email address</label>'
		. '<input class="spa-news__input" id="' . esc_attr( $uid ) . '-email" type="email" name="email" placeholder="you@email.com" autocomplete="email" inputmode="email" required aria-describedby="' . esc_attr( $uid ) . '-msg">'
		. '<button class="spa-news__btn" type="submit">Join</button>'
		. '</form>'
		. '<p class="spa-news__msg" id="' . esc_attr( $uid ) . '-msg" role="status" aria-live="polite"></p>'
		. '</div></div></div></section>';
}

/* ------------------------------------------------------------------ shared CTAs */

function spa_render_subscribe_button( $attrs ) {
	return spa_subscribe_button( isset( $attrs['placement'] ) ? sanitize_key( $attrs['placement'] ) : 'card' );
}

function spa_render_subscribe_cta( $attrs ) {
	$placement = isset( $attrs['placement'] ) ? sanitize_key( $attrs['placement'] ) : 'video_page';
	$subs      = spa_channel()['subscriberCount'];
	return '<section class="spa-subcta"><div class="spa-wrap"><div class="spa-subcta__box">'
		. '<div class="spa-subcta__text"><p class="spa-subcta__h">New videos every week from Dan</p>'
		. '<p class="spa-subcta__sub">Abs by AI on YouTube' . ( $subs ? ' · ' . esc_html( number_format_i18n( $subs ) ) . ' subscribers' : '' ) . '</p></div>'
		. spa_subscribe_button( $placement, 'spa-subcta__btn' )
		. '</div></div></section>';
}

/* ------------------------------------------------------------------ video pages */

function spa_render_video_hero() {
	$post = get_queried_object();
	if ( ! $post instanceof WP_Post || 'spa_video' !== $post->post_type ) {
		return '';
	}
	$yt       = (string) get_post_meta( $post->ID, '_spa_youtube_id', true );
	$type     = spa_video_type( $post->ID );
	$duration = (int) get_post_meta( $post->ID, '_spa_duration', true );
	$title    = get_the_title( $post );
	$eyebrow  = esc_html( get_the_date( 'M j, Y', $post ) ) . ( $duration ? ' · ' . esc_html( spa_format_duration( $duration ) ) : '' );
	$img      = spa_video_img( $post->ID, 'short' === $type ? 'portrait' : 'landscape', 'short' === $type ? '(min-width: 768px) 360px, 100vw' : '(min-width: 1024px) 896px, 100vw', true );
	$inner    = $img . '<span class="spa-play spa-play--red spa-play--lg" aria-hidden="true"></span>';

	if ( $yt && '0' !== (string) get_post_meta( $post->ID, '_spa_embeddable', true ) ) {
		$player = sprintf(
			'<button type="button" class="spa-player__facade" data-yt="%1$s" data-type="%2$s" data-title="%3$s" aria-label="%4$s">%5$s</button>',
			esc_attr( $yt ), esc_attr( $type ), esc_attr( wp_strip_all_tags( $title ) ), esc_attr( 'Play video: ' . wp_strip_all_tags( $title ) ), $inner
		);
	} else {
		$player = sprintf(
			'<a class="spa-player__facade" href="%1$s" target="_blank" rel="noopener"%2$s aria-label="%3$s">%4$s</a>',
			esc_url( 'https://www.youtube.com/watch?v=' . $yt ), spa_track( 'youtube_watch', 'video_page' ), esc_attr( 'Watch on YouTube: ' . wp_strip_all_tags( $title ) ), $inner
		);
	}

	return '<header class="spa-vhero spa-vhero--' . esc_attr( $type ) . '"><div class="spa-wrap spa-vhero__inner">'
		. '<p class="spa-eyebrow spa-vhero__eyebrow"><a href="' . esc_url( spa_url( 'short' === $type ? 'shorts' : 'videos' ) ) . '">' . ( 'short' === $type ? 'Short' : 'Free video' ) . '</a> · ' . $eyebrow . '</p>'
		. '<h1 class="spa-vhero__h1">' . esc_html( $title ) . '</h1>'
		. '<div class="spa-player spa-player--' . esc_attr( $type ) . '">' . $player . '</div>'
		. ( $yt ? '<p class="spa-vhero__links"><a href="' . esc_url( 'https://www.youtube.com/watch?v=' . $yt ) . '" target="_blank" rel="noopener"' . spa_track( 'youtube_watch', 'video_page' ) . '>Watch on YouTube</a></p>' : '' )
		. '</div></header>';
}

function spa_render_more_videos( $attrs ) {
	$post = get_queried_object();
	if ( ! $post instanceof WP_Post || 'spa_video' !== $post->post_type ) {
		return '';
	}
	$type  = spa_video_type( $post->ID );
	$count = isset( $attrs['count'] ) ? max( 1, (int) $attrs['count'] ) : 4;
	$posts = spa_get_videos( $type, $count, 0, array( $post->ID ) );
	if ( 'short' === $type && ! $posts ) {
		$type  = 'long';
		$posts = spa_get_videos( 'long', $count );
	}
	if ( ! $posts ) {
		return '';
	}
	$cards = '';
	foreach ( $posts as $p ) {
		$cards .= 'short' === $type ? spa_short_card( $p, '(min-width: 1024px) 220px, (min-width: 768px) 25vw, 45vw' ) : spa_row_card( $p );
	}
	return '<section class="spa-sec spa-more spa-more--' . esc_attr( $type ) . '" aria-labelledby="spa-more-h"><div class="spa-wrap">'
		. spa_section_head( 'short' === $type ? 'More shorts' : 'More free videos', 'spa-more-h', spa_url( 'short' === $type ? 'shorts' : 'videos' ), 'All →' )
		. '<div class="spa-more__grid">' . $cards . '</div>'
		. '</div></section>';
}

function spa_render_video_grid() {
	global $wp_query;
	$is_short = is_tax( 'spa_video_type', 'short' );
	$title    = $is_short ? 'Shorts' : 'Free videos';
	$switch   = $is_short
		? '<a class="spa-all" href="' . esc_url( spa_url( 'videos' ) ) . '">Long-form videos →</a>'
		: '<a class="spa-all" href="' . esc_url( spa_url( 'shorts' ) ) . '">Shorts →</a>';

	$cards = '';
	foreach ( (array) $wp_query->posts as $p ) {
		$cards .= $is_short ? spa_short_card( $p, '(min-width: 1024px) 200px, (min-width: 768px) 25vw, 45vw' ) : spa_grid_card( $p );
	}

	$out = '<section class="spa-archive spa-archive--' . ( $is_short ? 'short' : 'long' ) . '"><div class="spa-wrap">'
		. '<div class="spa-archive__head"><h1 class="spa-archive__h1">' . esc_html( $title ) . '</h1>' . $switch . '</div>';
	if ( $cards ) {
		$out  .= '<div class="spa-grid spa-grid--' . ( $is_short ? 'short' : 'long' ) . '">' . $cards . '</div>';
		$pages = paginate_links( array(
			'total'     => (int) $wp_query->max_num_pages,
			'current'   => max( 1, (int) get_query_var( 'paged' ) ),
			'prev_text' => '← Newer',
			'next_text' => 'Older →',
			'type'      => 'plain',
		) );
		if ( $pages ) {
			$out .= '<nav class="spa-pager" aria-label="More pages">' . $pages . '</nav>';
		}
	} else {
		$out .= '<p class="spa-archive__empty">New videos are on the way. Meanwhile, <a href="' . esc_url( spa_url( 'youtube' ) ) . '" target="_blank" rel="noopener"' . spa_track( 'youtube_watch', 'archive' ) . '>watch the channel on YouTube</a>.</p>';
	}
	return $out . '</div></section>';
}
