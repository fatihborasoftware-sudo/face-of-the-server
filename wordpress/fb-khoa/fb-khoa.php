<?php
/**
 * Plugin Name:       FB Khoa
 * Plugin URI:        https://khoa.fbserver.net
 * Description:       Khoa — the face of the server — on your WordPress site. Adds the "Khoa Hero" and "Khoa Stage" Elementor widgets (and the [khoa_hero] / [khoa_stage] shortcodes): the live 3D figure with demo data, his recorded voice in English and Turkish, the nine server situations and the Command Map of his crew.
 * Version:           1.2.1
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            FB Software Solutions · Fatih Bora
 * Author URI:        https://fbsoftwaresolutions.com
 * License:           MIT
 * Text Domain:       fb-khoa
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'FB_KHOA_VERSION', '1.2.1' );
define( 'FB_KHOA_DIR', plugin_dir_path( __FILE__ ) );
define( 'FB_KHOA_URL', plugin_dir_url( __FILE__ ) );

require_once FB_KHOA_DIR . 'includes/render.php';

/** Language of the current page: Polylang first, then the site locale. Only "en" and "tr" exist. */
function fb_khoa_lang() {
	$lang = '';
	if ( function_exists( 'pll_current_language' ) ) {
		$lang = (string) pll_current_language( 'slug' );
	}
	if ( '' === $lang ) {
		$lang = substr( determine_locale(), 0, 2 );
	}
	return ( 'tr' === strtolower( $lang ) ) ? 'tr' : 'en';
}

/** Front-end assets, registered once and only printed on pages that use Khoa. */
function fb_khoa_register_assets() {
	wp_register_style( 'fb-khoa-fonts', 'https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;900&family=IBM+Plex+Mono:wght@400;500;600&display=swap', array(), null );
	wp_register_style( 'fb-khoa', FB_KHOA_URL . 'assets/fb-khoa.css', array( 'fb-khoa-fonts' ), FB_KHOA_VERSION );
	wp_register_script( 'fb-khoa', FB_KHOA_URL . 'assets/fb-khoa.js', array(), FB_KHOA_VERSION, true );
}
add_action( 'wp_enqueue_scripts', 'fb_khoa_register_assets', 5 );
add_action( 'elementor/frontend/after_register_scripts', 'fb_khoa_register_assets' );
add_action( 'elementor/frontend/after_register_styles', 'fb_khoa_register_assets' );

function fb_khoa_enqueue() {
	if ( ! wp_style_is( 'fb-khoa', 'registered' ) ) {
		fb_khoa_register_assets();
	}
	wp_enqueue_style( 'fb-khoa' );
	wp_enqueue_script( 'fb-khoa' );
}

/* ---------- shortcodes ---------- */
add_shortcode(
	'khoa_hero',
	function ( $atts ) {
		fb_khoa_enqueue();
		return fb_khoa_render_hero( shortcode_atts( fb_khoa_hero_defaults(), $atts, 'khoa_hero' ) );
	}
);
add_shortcode(
	'khoa_stage',
	function ( $atts ) {
		fb_khoa_enqueue();
		return fb_khoa_render_stage( shortcode_atts( fb_khoa_stage_defaults(), $atts, 'khoa_stage' ) );
	}
);

/* ---------- Elementor widgets ---------- */
add_action(
	'elementor/widgets/register',
	function ( $widgets_manager ) {
		require_once FB_KHOA_DIR . 'includes/elementor-widgets.php';
		$widgets_manager->register( new \FB_Khoa_Hero_Widget() );
		$widgets_manager->register( new \FB_Khoa_Stage_Widget() );
	}
);
add_action(
	'elementor/elements/categories_registered',
	function ( $elements_manager ) {
		$elements_manager->add_category(
			'fb-khoa',
			array(
				'title' => 'FB Khoa',
				'icon'  => 'eicon-person',
			)
		);
	}
);

/* Stop page-speed plugins from rewriting the Khoa files. */
add_filter(
	'litespeed_optm_js_defer_exc',
	function ( $list ) {
		$list[] = 'fb-khoa';
		return $list;
	}
);
