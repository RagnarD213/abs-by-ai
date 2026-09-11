/**
 * SixPackAbs Child — front-end behaviour. No dependencies, loaded deferred.
 *  - PostHog `outbound_click` {target, placement} on every [data-spa-target] link
 *  - mobile menu: 200 ms ease-out, focus trapped, Escape and backdrop close
 *  - video page: click-to-play — the youtube-nocookie iframe is created on the
 *    click, never on load (+ PostHog `video_page_play`)
 *  - newsletter: validation on blur, disabled submit in flight, inline
 *    success/error inside the dark block, no reload; posts to absbyai.com
 *    /api/subscribe with source "sixpackabs" — the same subscriber list and
 *    Resend welcome sequence as every other form (MailerLite retired 2026-07-17)
 */
( function () {
	'use strict';

	function capture( event, props, beacon ) {
		try {
			if ( window.posthog && typeof window.posthog.capture === 'function' ) {
				window.posthog.capture( event, props, beacon ? { transport: 'sendBeacon' } : undefined );
			}
		} catch ( e ) { /* analytics never breaks the page */ }
	}

	/* ---------------------------------------------------------- outbound clicks */

	document.addEventListener( 'click', function ( e ) {
		var a = e.target.closest ? e.target.closest( '[data-spa-target]' ) : null;
		if ( ! a ) {
			return;
		}
		capture( 'outbound_click', {
			target: a.getAttribute( 'data-spa-target' ),
			placement: a.getAttribute( 'data-spa-placement' ) || 'unknown',
			href: a.href || ''
		}, true );
	} );

	/* ---------------------------------------------------------- mobile menu */

	var menu = document.getElementById( 'spa-menu' );
	var burger = document.querySelector( '.spa-burger' );
	if ( menu && burger ) {
		var panel = menu.querySelector( '.spa-menu__panel' );
		var closeButton = menu.querySelector( '.spa-menu__close' );
		var reduce = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
		var lastFocus = null;
		var closeTimer = null;

		var focusables = function () {
			return Array.prototype.filter.call( panel.querySelectorAll( 'a[href], button:not([disabled])' ), function ( el ) {
				return el.offsetParent !== null;
			} );
		};
		var open = function () {
			clearTimeout( closeTimer );
			lastFocus = document.activeElement;
			menu.hidden = false;
			document.documentElement.classList.add( 'spa-menu-open' );
			burger.setAttribute( 'aria-expanded', 'true' );
			void menu.offsetWidth; // start the transition from the closed state
			menu.classList.add( 'is-open' );
			( closeButton || focusables()[ 0 ] ).focus();
		};
		var close = function () {
			if ( menu.hidden ) {
				return;
			}
			menu.classList.remove( 'is-open' );
			burger.setAttribute( 'aria-expanded', 'false' );
			document.documentElement.classList.remove( 'spa-menu-open' );
			closeTimer = setTimeout( function () { menu.hidden = true; }, reduce ? 0 : 200 );
			if ( lastFocus && lastFocus.focus ) {
				lastFocus.focus();
			}
		};

		burger.addEventListener( 'click', open );
		menu.addEventListener( 'click', function ( e ) {
			if ( e.target.closest( '[data-spa-menu-close]' ) ) {
				close();
			}
		} );
		document.addEventListener( 'keydown', function ( e ) {
			if ( menu.hidden ) {
				return;
			}
			if ( e.key === 'Escape' ) {
				e.preventDefault();
				close();
				return;
			}
			if ( e.key === 'Tab' ) {
				var f = focusables();
				if ( ! f.length ) {
					return;
				}
				var first = f[ 0 ];
				var last = f[ f.length - 1 ];
				if ( e.shiftKey && document.activeElement === first ) {
					e.preventDefault();
					last.focus();
				} else if ( ! e.shiftKey && document.activeElement === last ) {
					e.preventDefault();
					first.focus();
				}
			}
		} );
		window.addEventListener( 'resize', function () {
			if ( ! menu.hidden && window.innerWidth >= 1024 ) {
				close();
			}
		} );
	}

	/* ---------------------------------------------------------- click-to-play */

	document.addEventListener( 'click', function ( e ) {
		var btn = e.target.closest ? e.target.closest( 'button.spa-player__facade' ) : null;
		if ( ! btn ) {
			return;
		}
		var id = btn.getAttribute( 'data-yt' ) || '';
		if ( ! /^[A-Za-z0-9_-]{11}$/.test( id ) ) {
			return;
		}
		var iframe = document.createElement( 'iframe' );
		// autoplay=1 only here: the visitor just pressed play.
		iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1';
		iframe.title = btn.getAttribute( 'data-title' ) || 'YouTube video';
		iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
		iframe.referrerPolicy = 'strict-origin-when-cross-origin';
		iframe.setAttribute( 'allowfullscreen', '' );
		btn.replaceWith( iframe );
		iframe.focus();
		capture( 'video_page_play', { video_id: id, type: btn.getAttribute( 'data-type' ) || '' } );
	} );

	/* ---------------------------------------------------------- newsletter */

	var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	Array.prototype.forEach.call( document.querySelectorAll( 'form.spa-news__form' ), function ( form ) {
		var input = form.querySelector( 'input[type="email"]' );
		var button = form.querySelector( 'button[type="submit"]' );
		var msg = document.getElementById( input.getAttribute( 'aria-describedby' ) );

		var say = function ( text, kind ) {
			if ( ! msg ) {
				return;
			}
			msg.textContent = text;
			if ( kind ) {
				msg.setAttribute( 'data-kind', kind );
			} else {
				msg.removeAttribute( 'data-kind' );
			}
		};
		var invalid = function ( on ) {
			if ( on ) {
				input.setAttribute( 'aria-invalid', 'true' );
			} else {
				input.removeAttribute( 'aria-invalid' );
			}
		};

		input.addEventListener( 'blur', function () {
			var v = input.value.trim();
			if ( v && ! EMAIL.test( v ) ) {
				invalid( true );
				say( 'Enter a valid email address.', 'error' );
			} else {
				invalid( false );
				if ( msg && msg.getAttribute( 'data-kind' ) === 'error' ) {
					say( '', '' );
				}
			}
		} );

		form.addEventListener( 'submit', function ( e ) {
			e.preventDefault();
			var v = input.value.trim();
			if ( ! EMAIL.test( v ) ) {
				invalid( true );
				say( 'Enter a valid email address.', 'error' );
				input.focus();
				return;
			}
			invalid( false );
			button.disabled = true;
			form.setAttribute( 'aria-busy', 'true' );
			say( 'Joining…', '' );
			fetch( form.getAttribute( 'data-endpoint' ) || 'https://absbyai.com/api/subscribe', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify( { email: v, source: 'sixpackabs' } )
			} ).then( function ( r ) {
				return r.json().catch( function () { return {}; } ).then( function ( d ) { return r.ok && d && d.ok; } );
			} ).then( function ( ok ) {
				if ( ok ) {
					say( "You're in! Check your inbox soon.", 'success' );
					form.reset();
					capture( 'newsletter_signup', { placement: form.getAttribute( 'data-placement' ) || '' } );
				} else {
					say( 'Something went wrong — please try again.', 'error' );
				}
			}, function () {
				say( 'Something went wrong — please try again.', 'error' );
			} ).then( function () {
				button.disabled = false;
				form.removeAttribute( 'aria-busy' );
			} );
		} );
	} );
} )();
