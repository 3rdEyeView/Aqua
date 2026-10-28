<?php
/**
 * Axiom Front Page
 * Serves the new Home page (ID 952) as the static front page.
 * Rollback: delete or unpublish this snippet; the stored Reading
 * settings (previous homepage) are left untouched.
 */
namespace AngieSnippets\AxiomFrontPage_1134;

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const HOME_ID = 952;

add_filter(
	'pre_option_show_on_front',
	function () {
		return 'page';
	}
);

add_filter(
	'pre_option_page_on_front',
	function () {
		return HOME_ID;
	}
);
