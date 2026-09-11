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

// Favicon from the design bundle — only when no Site Icon is set in Settings
// (the live site has one already; WordPress prints that itself).
add_action( 'wp_head', function () {
	if ( has_site_icon() ) {
		return;
	}
	printf( '<link rel="icon" href="%1$s" sizes="192x192">' . "\n" . '<link rel="apple-touch-icon" href="%1$s">' . "\n", esc_url( spa_img_uri( 'sixpackabs-icon-192.png' ) ) );
}, 5 );

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
