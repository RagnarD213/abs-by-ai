<?php
/**
 * Local-preview content for WordPress Playground (sixpackabs/playground/blueprint.json,
 * started by the `sixpackabs-playground` entry in .claude/launch.json).
 *
 * Creates stand-ins for the real pages the design links to, copies three real
 * articles from the live site's public REST API (to exercise the ported article
 * template: CTA card, end-of-post form, comments), then runs the REAL sync once
 * against absbyai.com's live feeds. Never run this anywhere but Playground.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
$host = (string) wp_parse_url( home_url(), PHP_URL_HOST );
if ( ! in_array( $host, array( '127.0.0.1', 'localhost' ), true ) ) {
	exit( 'seed.php only runs in a local Playground' );
}

function spa_seed_page( $title, $slug, $content, $parent = 0, $template = '' ) {
	$path     = $parent ? get_post_field( 'post_name', $parent ) . '/' . $slug : $slug;
	$existing = get_page_by_path( $path );
	if ( $existing ) {
		return $existing->ID;
	}
	$id = wp_insert_post( array(
		'post_type'    => 'page',
		'post_status'  => 'publish',
		'post_title'   => $title,
		'post_name'    => $slug,
		'post_content' => $content,
		'post_parent'  => $parent,
	) );
	if ( $template ) {
		update_post_meta( $id, '_wp_page_template', $template );
	}
	return $id;
}

function spa_seed_p( $text ) {
	return "<!-- wp:paragraph -->\n<p>" . esc_html( $text ) . "</p>\n<!-- /wp:paragraph -->";
}

$pages = spa_seed_page( 'Pages', 'pages', spa_seed_p( 'Pages.' ) );
spa_seed_page( 'About Us', 'about-us', spa_seed_p( 'Local stand-in for Dan’s story page.' ), $pages );
spa_seed_page( 'Abs Calculator', 'abs-calculator', spa_seed_p( 'Local stand-in for the Abs Calculator page.' ), 0, 'page-no-title' );
spa_seed_page( 'Contact Us', 'contact-us', spa_seed_p( 'Local stand-in for the Contact page.' ) );
spa_seed_page( 'Partner With Us', 'partner-with-us', spa_seed_p( 'Local stand-in for the Collab page.' ) );
spa_seed_page(
	'Blog',
	'blog',
	'<!-- wp:query {"queryId":1,"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":false}} --><div class="wp-block-query"><!-- wp:post-template --><!-- wp:post-title {"isLink":true} /--><!-- wp:post-date /--><!-- /wp:post-template --></div><!-- /wp:query -->'
);

$res = wp_remote_get( 'https://sixpackabs.com/wp-json/wp/v2/posts?per_page=3&_fields=title,slug,content,date_gmt', array( 'timeout' => 30 ) );
if ( ! is_wp_error( $res ) && 200 === (int) wp_remote_retrieve_response_code( $res ) ) {
	$cat = term_exists( 'ab-workouts', 'category' );
	if ( ! $cat ) {
		$cat = wp_insert_term( 'Ab Workouts', 'category', array( 'slug' => 'ab-workouts' ) );
	}
	foreach ( (array) json_decode( wp_remote_retrieve_body( $res ), true ) as $post ) {
		if ( get_page_by_path( $post['slug'], OBJECT, 'post' ) ) {
			continue;
		}
		$id = wp_insert_post( array(
			'post_type'     => 'post',
			'post_status'   => 'publish',
			'post_title'    => wp_strip_all_tags( html_entity_decode( $post['title']['rendered'] ) ),
			'post_name'     => $post['slug'],
			'post_content'  => $post['content']['rendered'],
			'post_date_gmt' => str_replace( 'T', ' ', $post['date_gmt'] ),
			'post_category' => array( (int) $cat['term_id'] ),
		) );
		wp_insert_comment( array( 'comment_post_ID' => $id, 'comment_author' => 'Local test', 'comment_content' => 'Local test comment.', 'comment_approved' => 1 ) );
	}
} else {
	error_log( 'seed: could not fetch live articles: ' . ( is_wp_error( $res ) ? $res->get_error_message() : wp_remote_retrieve_response_code( $res ) ) );
}

update_option( 'show_on_front', 'posts' );
flush_rewrite_rules();
error_log( 'seed sync: ' . wp_json_encode( spa_sync_run() ) );
