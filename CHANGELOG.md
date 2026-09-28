# Changelog

All versions are tags on this repository. Each one is a working pair of pages — fork whichever you like.

## v1.3 — 28 September 2026 · Khoa on the web
Khoa gets a public home: **[khoa.fbserver.net](https://khoa.fbserver.net)**, in English and Turkish, and the WordPress plugin that runs it is in `wordpress/`.
- **FB Khoa plugin 1.2.1** (`wordpress/fb-khoa-1.2.1.zip`): Elementor widgets *Khoa Hero* and *Khoa Stage*, shortcodes `[khoa_hero]` and `[khoa_stage]`.
- **Web versions** of both pages (`khoa-web.html`, `map-web.html`), built by patches from `index.html` and `map.html`: demo data only, three.js bundled, lite on phones, pause when off screen, a small `postMessage` API so the page can start the intro, switch situations and make agents speak.
- **Recorded voice, two languages**: 24 English lines (Piper “Alan”) and 24 Turkish lines (Piper “dfki”, slower, 3 semitones deeper, faint metallic echo — “the voice of the server”).
- **Command Map on the web**: a demo crew member speaks every 15 seconds — Khoa turns, raises his arm, clicks the node and opens the ID card. Crew cards cleaned (no white rims), Turkish text for all 14 cards.
- **Full Turkish**: every dashboard label, gauge, date and status line follows the page language.

## v1.2 — 27 September 2026 · Khoa
The figure gets a name, **Khoa**, and his own voice. He is no longer Serra's body — Serra stays the crew's voice; Khoa is the face of the server.
- **Khoa's voice**: a deep Piper voice ("Alan") served by `khoa/khoa-tts.py`, a tiny local service on `127.0.0.1:8082`. Away from the server the page falls back to the browser's own voice (`speechSynthesis`), so it still talks when you open it from GitHub. `voices.html` lets you listen to the voice samples and pick one.
- **`khoa say`** — the server can make Khoa talk from any terminal or script: `khoa say "The backup finished." --sit backup`. The page polls the queue every 1.5 s.
- **Situations**: backup, intrusion, heat, memory, ssd, load, update, alarm, normal — each with its own title, colour, gauge and sentence (keys 0–8, or the ◈ SITUATIONS menu). Made to be driven by real server events later.
- **▶ INTRO**: a cinematic introduction — Khoa introduces himself, the camera pushes in, captions materialise word by word under the title.
- **LIVE mode**: the intro's look is now his normal behaviour whenever he speaks — title + transcript captions on the left, camera pushes in, the dashboard dims, then everything fades back.
- **Talk gestures**: the arms wander slowly while he speaks (only the arms move, the chest stays still), and a glitter "web" streams out along the arm.
- Smaller fixes: the situation gauge fades where it crosses the head, the wake line no longer overlaps the intro, no letterbox bars.
- Tools: `patch_sit.py`, `patch_voice*.py`, `patch_intro*.py`, `patch_live.py`, `patch_gesture*.py`, `patch_web.py`, `patch_gaugefade.py`, plus the sleep/wake, card and logo patches from the same night.

## v1.1 — 26 September 2026
- **Lite mode** (`?lite`, automatic on localhost): pixel ratio 0.6, no bloom, ~25 % of the particles, no landscape/dust — for the server's own screen (an old laptop GPU).
- **CAMERA button**: the figure looks at you through the webcam (MediaPipe face detection, motion-centroid fallback). Needs https or localhost. Remembers on/off; `?cam` auto-starts.
- Camera tuning: bigger head movement, camera takes priority over the mouse, label shows LOOKING AT · YOU.
- **Assembly sound**: a rising sweep with a rumble, quickening pulse and a lock-in hit when the body finishes, played on ↻ REPLAY (and on the first click while still assembling). Synthesized live, no audio files.
- **ID-card thumbnails** on the Command Map: every crew member's card sits next to their node (embedded webp, hover to enlarge, glows while they speak).
- Tools: `patch_lite.py`, `patch_cam.py` + `webcam.js`, `patch_cam2.py`, `patch_sound.py`, `patch_thumbs.py` + `thumbs.json`.

## v1.0 — 26 September 2026
- The Face (`index.html`): particle écorché body from a CC-BY mesh, head rig, four voice states, scary mode, assembly, bloom pipeline.
- The Command Map (`map.html`): vitals on the figure (heart + network, load rings, storage), status-coloured veins, radial crew/app map, ID-card popups with the SPEAKING waveform, arm gesture that clicks the speaking agent, sci-fi sounds.
