/**
 * Editor previews for the theme's server-rendered blocks: each one renders
 * through ServerSideRender, exactly as it ships. No build step.
 */
( function ( blocks, element, ServerSideRender ) {
	var names = [
		'site-header', 'site-footer', 'featured-video', 'video-list', 'shorts-rail', 'instagram-grid',
		'bio', 'newsletter', 'subscribe-button', 'subscribe-cta', 'video-hero', 'video-grid', 'more-videos'
	];
	names.forEach( function ( slug ) {
		var name = 'spa/' + slug;
		if ( blocks.getBlockType( name ) && blocks.getBlockType( name ).edit ) {
			return;
		}
		blocks.registerBlockType( name, {
			edit: function ( props ) {
				return element.createElement( ServerSideRender, { block: name, attributes: props.attributes } );
			},
			save: function () {
				return null;
			}
		} );
	} );
} )( window.wp.blocks, window.wp.element, window.wp.serverSideRender );
