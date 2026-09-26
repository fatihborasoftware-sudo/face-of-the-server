# Changelog

All versions are tags on this repository. Each one is a working pair of pages — fork whichever you like.

## v1.1 — 26 September 2026
- **Lite mode** (`?lite`, automatic on localhost): pixel ratio 0.6, no bloom, ~25 % of the particles, no landscape/dust — for the server's own screen (an old laptop GPU).
- **CAMERA button**: the figure looks at you through the webcam (MediaPipe face detection, motion-centroid fallback). Needs https or localhost. Remembers on/off; `?cam` auto-starts.
- Camera tuning: bigger head movement, camera takes priority over the mouse, label shows LOOKING AT · YOU.
- **Assembly sound**: a rising sweep with a rumble, quickening pulse and a lock-in hit when the body finishes, played on ↻ REPLAY (and on the first click while still assembling). Synthesized live, no audio files.
- Tools: `patch_lite.py`, `patch_cam.py` + `webcam.js`, `patch_cam2.py`, `patch_sound.py`.

## v1.0 — 26 September 2026
- The Face (`index.html`): particle écorché body from a CC-BY mesh, head rig, four voice states, scary mode, assembly, bloom pipeline.
- The Command Map (`map.html`): vitals on the figure (heart + network, load rings, storage), status-coloured veins, radial crew/app map, ID-card popups with the SPEAKING waveform, arm gesture that clicks the speaking agent, sci-fi sounds.
