<?php
/**
 * Axiom Mobile Menu
 * Adds an accessible menu button to the site header at tablet/mobile widths
 * (<=1024px, where the inline header nav is hidden). The menu is built from
 * the header's existing nav links, so each item keeps its current target.
 * Desktop is unchanged. Without JavaScript the header behaves as before.
 * Rollback: unpublish or delete this snippet.
 */
namespace AngieSnippets\AxiomMobileMenu_1135;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function should_run() {
	if ( is_admin() || wp_doing_ajax() || is_customize_preview() ) {
		return false;
	}
	// Skip inside the Elementor editor preview iframe.
	if ( isset( $_GET['elementor-preview'] ) ) {
		return false;
	}
	return true;
}

add_action(
	'wp_head',
	function () {
		if ( ! should_run() ) {
			return;
		}
		echo '<style id="axm-menu-css">' . \trim( CSS ) . '</style>' . "\n";
	},
	50
);

add_action(
	'wp_footer',
	function () {
		if ( ! should_run() ) {
			return;
		}
		echo '<script id="axm-menu-js">' . \trim( JS ) . '</script>' . "\n";
	},
	50
);

const CSS = <<<'AXMCSS'
.axm-group{display:flex;align-items:center;gap:8px;flex:0 0 auto}
.axm-toggle{display:none}
@media (max-width:1024px){
.axm-group .axm-toggle,.axm-group .axm-toggle:hover,.axm-group .axm-toggle:focus,.axm-group .axm-toggle:active{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;min-height:0;margin:-3px 0;padding:0;border:1px solid var(--ax-line,#E2E7EE);border-radius:10px;background:#fff;color:var(--ax-ink,#0A1628);box-shadow:none;cursor:pointer;-webkit-tap-highlight-color:transparent;flex:0 0 44px;text-decoration:none}
.axm-group .axm-toggle:hover,.axm-group .axm-toggle.axm-open{border-color:#C9D2DE;background:var(--ax-paper,#F5F7FA)}
.axm-toggle:focus-visible,.axm-panel a:focus-visible{outline:2px solid var(--ax-blue,#1D6CE2);outline-offset:2px}
.axm-bars{position:relative;display:block;width:18px;height:12px}
.axm-bars span{position:absolute;left:0;width:18px;height:2px;border-radius:2px;background:currentColor;transition:transform .2s ease,opacity .15s ease,top .2s ease}
.axm-bars span:nth-child(1){top:0}
.axm-bars span:nth-child(2){top:5px}
.axm-bars span:nth-child(3){top:10px}
.axm-open .axm-bars span:nth-child(1){top:5px;transform:rotate(45deg)}
.axm-open .axm-bars span:nth-child(2){opacity:0}
.axm-open .axm-bars span:nth-child(3){top:5px;transform:rotate(-45deg)}
}
@media (max-width:380px){
.axm-group .ax-btn{padding-left:.75rem!important;padding-right:.75rem!important}
}
.axm-scrim{position:fixed;z-index:98;left:0;right:0;bottom:0;top:var(--axm-top,60px);background:rgba(10,22,40,.32);opacity:0;transition:opacity .18s ease}
.axm-panel{position:fixed;z-index:99;left:0;right:0;top:var(--axm-top,60px);max-height:calc(100vh - var(--axm-top,60px));max-height:calc(100dvh - var(--axm-top,60px));overflow-y:auto;overscroll-behavior:contain;background:#fff;border-bottom:1px solid var(--ax-line,#E2E7EE);box-shadow:0 18px 40px rgba(10,22,40,.14);padding:8px 1.5rem 20px;box-sizing:border-box;opacity:0;transform:translateY(-6px);transition:opacity .18s ease,transform .18s ease;font-family:var(--ax-body,Inter),sans-serif}
.axm-scrim[hidden],.axm-panel[hidden]{display:none}
.axm-shown .axm-scrim{opacity:1}
.axm-shown .axm-panel{opacity:1;transform:none}
@media (min-width:1025px){.axm-scrim,.axm-panel{display:none!important}}
@media (prefers-reduced-motion:reduce){.axm-scrim,.axm-panel,.axm-bars span{transition:none}}
.axm-inner{max-width:72rem;margin:0 auto}
.axm-list{list-style:none;margin:0;padding:0}
.axm-list li{margin:0;border-bottom:1px solid var(--ax-line,#E2E7EE)}
.axm-list a{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:56px;padding:10px 0;text-decoration:none;color:var(--ax-ink,#0A1628);font-family:var(--ax-display,Manrope),sans-serif;font-weight:700;font-size:1.0625rem;letter-spacing:-.01em;line-height:1.25;box-sizing:border-box}
.axm-list a:hover{color:var(--ax-blue,#1D6CE2)}
.axm-list a[aria-current="page"]{color:var(--ax-blue,#1D6CE2)}
.axm-label{display:flex;flex-direction:column;gap:3px}
.axm-sub{font-family:var(--ax-body,Inter),sans-serif;font-weight:500;font-size:.8125rem;letter-spacing:0;color:var(--ax-muted,#566174)}
.axm-tag{flex:0 0 auto;font-family:var(--ax-body,Inter),sans-serif;font-weight:700;font-size:.6875rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ax-blue,#1D6CE2);background:var(--ax-blue-soft,#EAF1FD);border-radius:999px;padding:4px 9px}
.axm-note{margin:16px 0 0;font-size:.875rem;line-height:1.5;color:var(--ax-muted,#566174)}
.axm-note strong{color:var(--ax-ink,#0A1628);font-weight:700}
@media (max-width:767px){.axm-panel{padding-left:1rem;padding-right:1rem}}

AXMCSS;

const JS = <<<'AXMJS'
(function () {
	var nav = document.querySelector('nav');
	if (!nav || document.querySelector('.axm-toggle')) return;
	var bar = nav.parentElement;
	var header = bar && bar.parentElement;
	// The CTA may already sit in an .axm-group (the Axiom Business Phone snippet
	// renders one around the phone link and the CTA).
	var cta = bar && bar.querySelector(':scope > a.ax-btn, :scope > .axm-group > a.ax-btn');
	var links = Array.prototype.slice.call(nav.querySelectorAll('a[href]'));
	if (!header || !cta || links.length < 3) return;

	var mq = window.matchMedia('(max-width: 1024px)');
	var here = location.pathname.replace(/\/+$/, '') || '/';

	var group = cta.parentNode.classList.contains('axm-group') ? cta.parentNode : null;
	if (!group) {
		group = document.createElement('div');
		group.className = 'axm-group';
		cta.parentNode.insertBefore(group, cta);
		group.appendChild(cta);
	}

	var toggle = document.createElement('button');
	toggle.type = 'button';
	toggle.className = 'axm-toggle';
	toggle.setAttribute('aria-controls', 'axm-panel');
	toggle.setAttribute('aria-expanded', 'false');
	toggle.setAttribute('aria-label', 'Open menu');
	toggle.innerHTML = '<span class="axm-bars" aria-hidden="true"><span></span><span></span><span></span></span>';
	group.appendChild(toggle);

	var scrim = document.createElement('div');
	scrim.className = 'axm-scrim';
	scrim.hidden = true;

	var panel = document.createElement('nav');
	panel.id = 'axm-panel';
	panel.className = 'axm-panel';
	panel.setAttribute('aria-label', 'Site menu');
	panel.hidden = true;

	var inner = document.createElement('div');
	inner.className = 'axm-inner';
	var list = document.createElement('ul');
	list.className = 'axm-list';

	links.forEach(function (src) {
		var href = src.getAttribute('href');
		var text = src.textContent.trim();
		var li = document.createElement('li');
		var a = document.createElement('a');
		a.href = href;
		var path = a.pathname.replace(/\/+$/, '') || '/';
		if (path === here) a.setAttribute('aria-current', 'page');
		var label = document.createElement('span');
		label.className = 'axm-label';
		label.appendChild(document.createTextNode(text));
		if (/\/add-ons\/?$/.test(path)) {
			var sub = document.createElement('span');
			sub.className = 'axm-sub';
			sub.textContent = 'Lead response & follow-up automation';
			label.appendChild(sub);
			a.appendChild(label);
			var tag = document.createElement('span');
			tag.className = 'axm-tag';
			tag.textContent = 'Optional';
			a.appendChild(tag);
		} else {
			a.appendChild(label);
		}
		li.appendChild(a);
		list.appendChild(li);
	});

	// Click-to-call row, when the header has a phone link (Axiom Business Phone).
	var call = group.querySelector('a.axp-call[href^="tel:"]');
	var num = call && call.querySelector('.axp-num');
	if (num) {
		var cli = document.createElement('li');
		var ca = document.createElement('a');
		ca.href = call.getAttribute('href');
		var clabel = document.createElement('span');
		clabel.className = 'axm-label';
		clabel.appendChild(document.createTextNode('Call ' + num.textContent.trim()));
		ca.appendChild(clabel);
		cli.appendChild(ca);
		list.appendChild(cli);
	}

	var note = document.createElement('p');
	note.className = 'axm-note';
	note.innerHTML = 'Plans from <strong>$299/month</strong> with essential automations included. Growth ($599/month) adds Google Ads management.';

	inner.appendChild(list);
	inner.appendChild(note);
	panel.appendChild(inner);
	// Sibling of the header, not a child: a header with backdrop-filter would
	// otherwise become the containing block for these fixed elements.
	header.parentNode.insertBefore(scrim, header.nextSibling);
	header.parentNode.insertBefore(panel, scrim.nextSibling);

	function inside(el) {
		return header.contains(el) || panel.contains(el);
	}

	function setTop() {
		document.documentElement.style.setProperty('--axm-top', Math.round(header.getBoundingClientRect().bottom) + 'px');
	}

	function isOpen() {
		return toggle.getAttribute('aria-expanded') === 'true';
	}

	function open() {
		setTop();
		scrim.hidden = false;
		panel.hidden = false;
		toggle.setAttribute('aria-expanded', 'true');
		toggle.setAttribute('aria-label', 'Close menu');
		toggle.classList.add('axm-open');
		requestAnimationFrame(function () {
			document.documentElement.classList.add('axm-shown');
		});
	}

	function close(returnFocus) {
		if (!isOpen()) return;
		toggle.setAttribute('aria-expanded', 'false');
		toggle.setAttribute('aria-label', 'Open menu');
		toggle.classList.remove('axm-open');
		document.documentElement.classList.remove('axm-shown');
		scrim.hidden = true;
		panel.hidden = true;
		if (returnFocus) toggle.focus();
	}

	toggle.addEventListener('click', function () {
		isOpen() ? close(false) : open();
	});
	scrim.addEventListener('click', function () {
		close(false);
	});
	panel.addEventListener('click', function (e) {
		if (e.target.closest('a')) close(false);
	});
	document.addEventListener('keydown', function (e) {
		if ((e.key === 'Escape' || e.key === 'Esc') && isOpen()) close(true);
	});
	function onFocusOut(e) {
		if (isOpen() && e.relatedTarget && !inside(e.relatedTarget)) close(false);
	}
	header.addEventListener('focusout', onFocusOut);
	panel.addEventListener('focusout', onFocusOut);
	window.addEventListener('resize', function () {
		if (isOpen()) mq.matches ? setTop() : close(false);
	});
})();

AXMJS;
