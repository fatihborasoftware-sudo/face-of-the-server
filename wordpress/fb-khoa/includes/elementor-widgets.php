<?php
/** FB Khoa — Elementor widgets. Every text is a normal Elementor control, so the page stays editable by hand. */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class FB_Khoa_Hero_Widget extends \Elementor\Widget_Base {
	public function get_name() {
		return 'fb_khoa_hero';
	}
	public function get_title() {
		return 'Khoa Hero';
	}
	public function get_icon() {
		return 'eicon-person';
	}
	public function get_categories() {
		return array( 'fb-khoa' );
	}
	public function get_keywords() {
		return array( 'khoa', '3d', 'hero', 'fb server' );
	}
	public function get_style_depends() {
		return array( 'fb-khoa' );
	}
	public function get_script_depends() {
		return array( 'fb-khoa' );
	}

	protected function register_controls() {
		$d = fb_khoa_hero_defaults();
		$this->start_controls_section( 'content', array( 'label' => 'Khoa Hero' ) );
		$fields = array(
			'eyebrow'     => array( 'Small line above the title', \Elementor\Controls_Manager::TEXT ),
			'title'       => array( 'Title', \Elementor\Controls_Manager::TEXT ),
			'subtitle'    => array( 'Subtitle', \Elementor\Controls_Manager::TEXT ),
			'line'        => array( 'Khoa\'s line', \Elementor\Controls_Manager::TEXT ),
			'text'        => array( 'Text', \Elementor\Controls_Manager::TEXTAREA ),
			'button'      => array( 'Button: starts the intro', \Elementor\Controls_Manager::TEXT ),
			'button2'     => array( 'Second button', \Elementor\Controls_Manager::TEXT ),
			'button2_url' => array( 'Second button link', \Elementor\Controls_Manager::TEXT ),
			'hint'        => array( 'Hint under the buttons', \Elementor\Controls_Manager::TEXT ),
			'credit'      => array( 'Model credit (keep it: CC BY licence)', \Elementor\Controls_Manager::TEXT ),
			'height'      => array( 'Height (for example 100vh or 800px)', \Elementor\Controls_Manager::TEXT ),
		);
		foreach ( $fields as $key => $f ) {
			$this->add_control(
				$key,
				array(
					'label'       => $f[0],
					'type'        => $f[1],
					'default'     => $d[ $key ],
					'label_block' => true,
				)
			);
		}
		$this->end_controls_section();
	}

	protected function render() {
		$s = $this->get_settings_for_display();
		$a = fb_khoa_hero_defaults();
		foreach ( $a as $k => $v ) {
			if ( isset( $s[ $k ] ) ) {
				$a[ $k ] = (string) $s[ $k ];
			}
		}
		fb_khoa_enqueue();
		echo fb_khoa_render_hero( $a ); // phpcs:ignore WordPress.Security.EscapeOutput -- escaped inside.
	}
}

class FB_Khoa_Stage_Widget extends \Elementor\Widget_Base {
	public function get_name() {
		return 'fb_khoa_stage';
	}
	public function get_title() {
		return 'Khoa Stage (situations)';
	}
	public function get_icon() {
		return 'eicon-play';
	}
	public function get_categories() {
		return array( 'fb-khoa' );
	}
	public function get_keywords() {
		return array( 'khoa', 'situations', 'dashboard', 'fb server' );
	}
	public function get_style_depends() {
		return array( 'fb-khoa' );
	}
	public function get_script_depends() {
		return array( 'fb-khoa' );
	}

	protected function register_controls() {
		$d = fb_khoa_stage_defaults();
		$this->start_controls_section( 'content', array( 'label' => 'Khoa Stage' ) );
		$this->add_control(
			'hint',
			array(
				'label'       => 'Hint under the buttons',
				'type'        => \Elementor\Controls_Manager::TEXTAREA,
				'default'     => $d['hint'],
				'label_block' => true,
			)
		);
		$this->add_control(
			'map_hint',
			array(
				'label'       => 'Hint under the crew buttons (Command Map)',
				'type'        => \Elementor\Controls_Manager::TEXTAREA,
				'default'     => $d['map_hint'],
				'label_block' => true,
			)
		);
		$this->add_control(
			'height',
			array(
				'label'   => 'Screen height (for example 640px)',
				'type'    => \Elementor\Controls_Manager::TEXT,
				'default' => $d['height'],
			)
		);
		$this->end_controls_section();
	}

	protected function render() {
		$s = $this->get_settings_for_display();
		$a = fb_khoa_stage_defaults();
		foreach ( $a as $k => $v ) {
			if ( isset( $s[ $k ] ) ) {
				$a[ $k ] = (string) $s[ $k ];
			}
		}
		fb_khoa_enqueue();
		echo fb_khoa_render_stage( $a ); // phpcs:ignore WordPress.Security.EscapeOutput -- escaped inside.
	}
}
