<?php
/**
 * <head> additions: PostHog (moved here from the July header part — same
 * project key and host), the SixPackAbs favicon, and on each video page the
 * VideoObject JSON-LD + og:video tags. Yoast keeps title, description,
 * canonical and the rest of Open Graph.
 */

defined( 'ABSPATH' ) || exit;

add_action( 'wp_head', function () {
	?>
<script>
!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
posthog.init('phc_s3ZXKWHRFQVqK6pYRBRBKtc2ex7LL78CFMHtCfENEQrU', {
  api_host: 'https://us.posthog.com',
  person_profiles: 'identified_only'
});
</script>
	<?php
}, 1 );

// Site icon = the gold-on-black SixPackAbs.com symbol (brand layer, Dan 2026-11-05).
// The theme files win over whatever image is stored in Settings → Site Icon, so the
// icon ships and rolls back with the theme. get_site_icon_url() also feeds
// /favicon.ico, the Apple touch icon and the msapplication tile.
add_filter( 'get_site_icon_url', function ( $url, $size ) {
	$size = (int) $size;
	if ( $size <= 32 ) {
		$file = 'sixpackabs-icon-32.png';
	} elseif ( $size <= 180 ) {
		$file = 'sixpackabs-icon-180.png';
	} elseif ( $size <= 192 ) {
		$file = 'sixpackabs-icon-192.png';
	} else {
		$file = 'sixpackabs-icon-512.png';
	}
	return spa_img_uri( $file );
}, 99, 2 );

add_filter( 'site_icon_meta_tags', function () {
	return array(
		sprintf( '<link rel="icon" href="%s" sizes="any">', esc_url( spa_img_uri( 'favicon.ico' ) ) ),
		sprintf( '<link rel="icon" href="%s" sizes="32x32" type="image/png">', esc_url( spa_img_uri( 'sixpackabs-icon-32.png' ) ) ),
		sprintf( '<link rel="icon" href="%s" sizes="192x192" type="image/png">', esc_url( spa_img_uri( 'sixpackabs-icon-192.png' ) ) ),
		sprintf( '<link rel="icon" href="%s" sizes="512x512" type="image/png">', esc_url( spa_img_uri( 'sixpackabs-icon-512.png' ) ) ),
		sprintf( '<link rel="apple-touch-icon" href="%s">', esc_url( spa_img_uri( 'sixpackabs-icon-180.png' ) ) ),
		sprintf( '<meta name="msapplication-TileImage" content="%s">', esc_url( spa_img_uri( 'sixpackabs-icon-512.png' ) ) ),
	);
}, 99 );

// No Site Icon saved (Playground, a fresh staging copy): WordPress prints nothing,
// so print the same tags here.
add_action( 'wp_head', function () {
	if ( has_site_icon() ) {
		return;
	}
	echo implode( "\n", apply_filters( 'site_icon_meta_tags', array() ) ) . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput
}, 5 );

// Default Open Graph image (Twitter falls back to it) for any page without one of its own (Yoast).
add_action( 'wpseo_add_opengraph_additional_images', function ( $images ) {
	if ( is_object( $images ) && method_exists( $images, 'has_images' ) && ! $images->has_images() ) {
		$images->add_image( array(
			'url'    => spa_img_uri( 'sixpackabs-og-1200x630.jpg' ),
			'width'  => 1200,
			'height' => 630,
			'type'   => 'image/jpeg',
		) );
	}
} );

// Video pages: structured data and og:video.
add_action( 'wp_head', function () {
	if ( ! is_singular( 'spa_video' ) ) {
		return;
	}
	$post = get_queried_object();
	$yt   = (string) get_post_meta( $post->ID, '_spa_youtube_id', true );
	if ( ! $yt ) {
		return;
	}
	$thumb = get_the_post_thumbnail_url( $post, 'full' );
	if ( ! $thumb ) {
		$thumb = (string) get_post_meta( $post->ID, '_spa_thumb_url', true );
	}
	$description = has_excerpt( $post ) ? get_the_excerpt( $post ) : wp_trim_words( wp_strip_all_tags( $post->post_content ), 40 );
	$embed       = 'https://www.youtube.com/embed/' . rawurlencode( $yt );
	$data        = array(
		'@context'     => 'https://schema.org',
		'@type'        => 'VideoObject',
		'name'         => wp_specialchars_decode( get_the_title( $post ), ENT_QUOTES ),
		'description'  => wp_specialchars_decode( $description, ENT_QUOTES ),
		'thumbnailUrl' => array_values( array_filter( array( $thumb ) ) ),
		'uploadDate'   => get_post_time( 'c', true, $post ),
		'embedUrl'     => $embed,
		'contentUrl'   => 'https://www.youtube.com/watch?v=' . rawurlencode( $yt ),
	);
	$duration = (int) get_post_meta( $post->ID, '_spa_duration', true );
	if ( $duration ) {
		$data['duration'] = spa_iso_duration( $duration );
	}
	echo '<script type="application/ld+json">' . wp_json_encode( $data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
	printf( '<meta property="og:video" content="%1$s">' . "\n", esc_url( $embed ) );
	printf( '<meta property="og:video:secure_url" content="%1$s">' . "\n", esc_url( $embed ) );
	echo '<meta property="og:video:type" content="text/html">' . "\n";
	$short = 'short' === spa_video_type( $post->ID );
	printf( '<meta property="og:video:width" content="%d">' . "\n", $short ? 1080 : 1280 );
	printf( '<meta property="og:video:height" content="%d">' . "\n", $short ? 1920 : 720 );
}, 20 );

// Video pages: Yoast prints no meta description for spa_video by default. Use the
// excerpt (a hand-written summary once an article is in place, else the first line
// of the YouTube description) unless one is set in the Yoast box.
add_filter( 'wpseo_metadesc', function ( $description ) {
	if ( $description || ! is_singular( 'spa_video' ) ) {
		return $description;
	}
	$post = get_queried_object();
	return has_excerpt( $post ) ? wp_strip_all_tags( get_the_excerpt( $post ) ) : $description;
} );
