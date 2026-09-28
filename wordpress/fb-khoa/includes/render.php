<?php
/** FB Khoa — HTML for the hero and the stage (shared by the shortcodes and the Elementor widgets). */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Default texts, in the page's language. Every one can be changed in the widget or shortcode. */
function fb_khoa_hero_defaults() {
	$tr = ( 'tr' === fb_khoa_lang() );
	return array(
		'eyebrow'     => $tr ? '● CANLI · DEMO SUNUCU' : '● LIVE · DEMO SERVER',
		'title'       => 'KHOA',
		'subtitle'    => $tr ? 'SUNUCUNUN YÜZÜ' : 'THE FACE OF THE SERVER',
		'line'        => $tr ? 'Ben Khoa. Sunucunun yüzüyüm.' : 'I am Khoa. The face of the server.',
		'text'        => $tr ? 'Gerçek bir ev sunucusunu izliyorum. Kalbini, ısısını ve her kapısını görüyorum. Bir şey olduğunda sana söylerim.' : 'I watch a real home server. I see its heart, its heat and every door. When something happens, I tell you.',
		'button'      => $tr ? 'KHOA İLE TANIŞ' : 'MEET KHOA',
		'button2'     => $tr ? 'ÜCRETSİZ AL' : 'GET HIM FREE',
		'button2_url' => '#own',
		'hint'        => $tr ? 'Sesi aç · konuşuyor. Fareyle başını çevir.' : 'Sound on · he speaks. Move the mouse to turn his head.',
		'credit'      => 'ÉCORCHÉ MESH BY DIEGO LUJÁN GARCÍA (CC BY 4.0, SKETCHFAB)',
		'height'      => '100vh',
	);
}

function fb_khoa_stage_defaults() {
	$tr = ( 'tr' === fb_khoa_lang() );
	return array(
		'hint'     => $tr ? 'Bir durum seç — Khoa gerçek sunucudaki gibi tepki verir. Klavyede 0–8 tuşları da çalışır.' : 'Pick a situation — Khoa reacts the way he does on the real server. Keys 0–8 work too.',
		'map_hint' => $tr ? 'Bir ajanı konuştur — Khoa ona döner, kolunu kaldırır ve kimlik kartını açar. Düğümlere tıklayarak da kartları görebilirsin.' : 'Make an agent speak — Khoa turns to them, raises his arm and opens their ID card. Click any node to read its card.',
		'height' => '640px',
	);
}

function fb_khoa_situations() {
	$tr = ( 'tr' === fb_khoa_lang() );
	$s  = array(
		'normal'    => array( 'normal', 'normal', '#4dff7a' ),
		'backup'    => array( 'backup', 'yedekleme', '#39ff6a' ),
		'intrusion' => array( 'intrusion', 'saldırı', '#ff2a1a' ),
		'heat'      => array( 'heat', 'ısınma', '#ff7a1a' ),
		'memory'    => array( 'memory', 'bellek', '#b86bff' ),
		'ssd'       => array( 'disk', 'disk', '#ffb347' ),
		'load'      => array( 'load', 'yük', '#e8f4ff' ),
		'update'    => array( 'update', 'güncelleme', '#4aa8ff' ),
		'alarm'     => array( 'alarm', 'alarm', '#ff4a3a' ),
	);
	$out = array();
	foreach ( $s as $k => $v ) {
		$out[ $k ] = array(
			'label' => $tr ? $v[1] : $v[0],
			'color' => $v[2],
		);
	}
	return $out;
}

function fb_khoa_crew() {
	return array(
		'serra'    => 'Serra',
		'watchman' => 'The Watchman',
		'locke'    => 'Locke',
		'corren'   => 'Corren',
		'quill'    => 'Quill',
		'dusk'     => 'Dusk',
		'relay'    => 'Relay',
		'mason'    => 'Mason',
	);
}

function fb_khoa_app_url( $embed, $page = 'khoa-web' ) {
	return add_query_arg(
		array(
			'embed' => $embed,
			'lang'  => fb_khoa_lang(),
			'v'     => FB_KHOA_VERSION,
		),
		FB_KHOA_URL . 'app/' . $page . '.html'
	);
}

function fb_khoa_render_hero( $a ) {
	$id    = 'khoa-hero-' . wp_unique_id();
	$title = esc_html( $a['title'] );
	ob_start();
	?>
<section class="khoa-hero" id="<?php echo esc_attr( $id ); ?>" style="--khoa-h:<?php echo esc_attr( $a['height'] ); ?>">
	<iframe class="khoa-frame" data-khoa-frame="hero" src="<?php echo esc_url( fb_khoa_app_url( 'hero' ) ); ?>" title="<?php echo esc_attr( wp_strip_all_tags( $a['title'] . ' — ' . $a['subtitle'] ) ); ?>" allow="autoplay; camera" loading="eager"></iframe>
	<div class="khoa-hero__over">
		<?php if ( '' !== $a['eyebrow'] ) : ?><div class="khoa-eyebrow khoa-eyebrow--live"><?php echo esc_html( $a['eyebrow'] ); ?></div><?php endif; ?>
		<h1 class="khoa-hero__title"><?php echo $title; // phpcs:ignore WordPress.Security.EscapeOutput ?></h1>
		<?php if ( '' !== $a['subtitle'] ) : ?><div class="khoa-hero__sub"><?php echo esc_html( $a['subtitle'] ); ?></div><?php endif; ?>
		<?php if ( '' !== $a['line'] ) : ?><p class="khoa-hero__line"><?php echo esc_html( $a['line'] ); ?></p><?php endif; ?>
		<?php if ( '' !== $a['text'] ) : ?><p class="khoa-hero__text"><?php echo esc_html( $a['text'] ); ?></p><?php endif; ?>
		<div class="khoa-hero__btns">
			<?php if ( '' !== $a['button'] ) : ?>
			<button type="button" class="khoa-btn khoa-btn--primary" data-khoa-cmd="intro" data-khoa-target="#<?php echo esc_attr( $id ); ?>">
				<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4l14 8-14 8z"/></svg><?php echo esc_html( $a['button'] ); ?>
			</button>
			<?php endif; ?>
			<?php if ( '' !== $a['button2'] ) : ?>
			<a class="khoa-btn" href="<?php echo esc_url( $a['button2_url'] ); ?>"><?php echo esc_html( $a['button2'] ); ?></a>
			<?php endif; ?>
		</div>
		<?php if ( '' !== $a['hint'] ) : ?><div class="khoa-hero__hint"><?php echo esc_html( $a['hint'] ); ?></div><?php endif; ?>
	</div>
	<?php if ( '' !== $a['credit'] ) : ?><div class="khoa-hero__credit"><?php echo esc_html( $a['credit'] ); ?></div><?php endif; ?>
</section>
	<?php
	return ob_get_clean();
}

function fb_khoa_render_stage( $a ) {
	$id   = 'khoa-stage-' . wp_unique_id();
	$sit  = fb_khoa_situations();
	$tr   = ( 'tr' === fb_khoa_lang() );
	$hint = isset( $a['hint'] ) ? $a['hint'] : '';
	$mh   = isset( $a['map_hint'] ) ? $a['map_hint'] : '';
	ob_start();
	?>
<div class="khoa-stage" id="<?php echo esc_attr( $id ); ?>" data-panel="face" style="--khoa-stage-h:<?php echo esc_attr( $a['height'] ); ?>">
	<div class="khoa-stage__panels" role="tablist" aria-label="<?php echo esc_attr( $tr ? 'Paneller' : 'Panels' ); ?>">
		<span class="khoa-stage__plbl"><?php echo esc_html( $tr ? 'PANELLER' : 'PANELS' ); ?></span>
		<button type="button" role="tab" aria-selected="true" class="khoa-panel is-on" data-khoa-panel="face" data-src="<?php echo esc_url( fb_khoa_app_url( 'full' ) ); ?>"><?php echo esc_html( $tr ? 'Sunucunun Yüzü' : 'Face of the Server' ); ?></button>
		<button type="button" role="tab" aria-selected="false" class="khoa-panel" data-khoa-panel="map" data-src="<?php echo esc_url( fb_khoa_app_url( 'full', 'map-web' ) ); ?>"><?php echo esc_html( $tr ? 'Komuta Haritası' : 'Command Map' ); ?></button>
	</div>
	<div class="khoa-stage__btns" data-khoa-group="face" role="group" aria-label="<?php echo esc_attr( $tr ? 'Durumlar' : 'Situations' ); ?>">
		<?php
		$i = 0;
		foreach ( $sit as $k => $s ) :
			?>
		<button type="button" class="khoa-sit<?php echo 'normal' === $k ? ' is-on' : ''; ?>" style="--c:<?php echo esc_attr( $s['color'] ); ?>" data-khoa-sit="<?php echo esc_attr( $k ); ?>" data-khoa-target="#<?php echo esc_attr( $id ); ?>">
			<span class="khoa-sit__key"><?php echo (int) $i; ?></span><span class="khoa-sit__name"><?php echo esc_html( $s['label'] ); ?></span>
		</button>
			<?php
			++$i;
		endforeach;
		?>
		<?php if ( '' !== $hint ) : ?><p class="khoa-stage__hint"><?php echo esc_html( $hint ); ?></p><?php endif; ?>
	</div>
	<div class="khoa-stage__btns khoa-stage__btns--crew" data-khoa-group="map" role="group" aria-label="<?php echo esc_attr( $tr ? 'Ekip' : 'The crew' ); ?>" hidden>
		<?php foreach ( fb_khoa_crew() as $k => $name ) : ?>
		<button type="button" class="khoa-sit" style="--c:#5fd6ff" data-khoa-talk="<?php echo esc_attr( $k ); ?>" data-khoa-target="#<?php echo esc_attr( $id ); ?>">
			<span class="khoa-sit__key"><?php echo esc_html( $tr ? 'KONUŞ' : 'SPEAK' ); ?></span><span class="khoa-sit__name"><?php echo esc_html( $name ); ?></span>
		</button>
		<?php endforeach; ?>
		<?php if ( '' !== $mh ) : ?><p class="khoa-stage__hint"><?php echo esc_html( $mh ); ?></p><?php endif; ?>
	</div>
	<div class="khoa-stage__screen">
		<iframe class="khoa-frame" data-khoa-frame="full" data-src="<?php echo esc_url( fb_khoa_app_url( 'full' ) ); ?>" title="Khoa" allow="autoplay; camera"></iframe>
		<button type="button" class="khoa-stage__start" data-khoa-start><?php echo esc_html( $tr ? '▶ PANOYU AÇ' : '▶ OPEN THE DASHBOARD' ); ?></button>
	</div>
</div>
	<?php
	return ob_get_clean();
}
