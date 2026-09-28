# Master prompt: build your own "Face of the Server" dashboard (Khoa)

Copy everything between the two lines into Claude as your first message. Fill in the three lines marked **YOUR** first. Then answer Claude's questions one at a time.

---

## Who I am and what I want

I am not a coder, so guide me one step at a time. When I need to do something myself, tell me exactly where to click or which window to type in, give real values instead of placeholders, and give one command per line.

I want a **3D "face" for my home server**: a full-screen web dashboard where a glowing particle figure (a human anatomy / écorché body made of light) lives in the middle of the screen. He watches the server, turns to look at me, speaks out loud, and changes colour and mood when something happens.

- **YOUR** server: (for example "Ubuntu 24.04 on an old laptop" — or "no server, demo data only")
- **YOUR** figure's name and first sentence: (for example "Khoa" — "I am Khoa. The face of the server.")
- **YOUR** languages: (for example "English, plus Turkish when the visitor chooses")

## How we work (please follow this order)

1. **Mockup first.** Before writing real code, show me a clickable mockup (desktop and phone). Wait for my "approved".
2. **Plan in steps.** Number the steps. Do one step, test it yourself, show me the result, then continue.
3. **Test your own work.** After every step, open the page in a headless browser, check the console for errors, and take a screenshot of it on desktop and on phone size.
4. **Deliver files.** I get every version as a downloadable file (and a zip when there are several files). Keep a CHANGELOG.
5. **Back up before changing anything live.** Take a backup or snapshot of the server/site first, every time.

## The page: `index.html` ("Face of the Server")

Build one self-contained HTML file. Use three.js r128, stored locally as `three.min.js` next to the page (no CDN at runtime). Use the IBM Plex Mono font. The background is near-black blue (`#000306`), with cyan `#6fdcff` as the main accent and amber `#ffb347` as the second.

### The figure

- A human anatomy mesh (écorché) turned into **particles**. Write a small Python tool, `build_body.py`, that samples points from the mesh surface and stores them inside the page, so the page needs no model file.
  - Use a mesh with a Creative Commons licence and keep the credit visible in the footer. Mine was "Male Full Body Ecorche" by Diego Luján García, CC BY 4.0, from Sketchfab. I download the mesh myself and give it to you.
- Custom shader points with a soft **bloom** glow, and a slow breathing shimmer.
- **Assembling intro:** the particles fly in from a cloud and build the body over about 7 seconds. The status line shows `ASSEMBLING... 0–100%`. A rising synth "assemble" sound ends in a lock-in hit, made with Web Audio only, no sound files.
- **Look-at:** the head and eyes follow the mouse (`LOOKING AT · MOUSE`). Expose `window.serraLookAt(x,y)` so a webcam can drive it later. Add an optional CAMERA button that uses face detection, falls back to motion, and runs only over https.
- **Idle life:** subtle sway, and he "falls asleep" (slumps and dims) after a few minutes with no one there, then wakes up on a touch or key press.
- **Scene:** fine dust particles around him that get swept when he moves, a faint particle mountain range far behind, and orbiting rings.
- **States:** `idle · listening · thinking · speaking`, shown as small chips. While speaking, the arms make slow talking gestures (only the arms bend, the body stays still) and particles stream from the hand.

### The HUD and dashboard (around the figure)

- **Top bar:** the name ("KHOA · THE FACE OF THE SERVER"), the status line, a clock, the date, uptime and `NET ▼ ▲`.
- **Side panels, thin and see-through:**
  - SYSTEM LOAD: CPU, memory, root disk and CPU temperature as ring gauges, with "cool / warm / hot".
  - STORAGE: disks and free space.
  - SERVICES: "11 / 12 OK".
  - NETWORK: down/up speed, interface, address.
  - ACCESS: "LAN ONLY", sessions, failed logins, last login.
  - LATEST EVENTS: the last 5 lines.
- **Data source:** every 5 seconds the page reads `data.json` from the server. If it can't, it uses built-in **demo data**, so the page always works.
  - Write a small server script (Python, run by systemd) that writes `data.json`: CPU, memory, disks, temperature, services, network, logins, last backup, events.
- **Buttons at the bottom:** `↻ REPLAY` (intro again), `☠ SCARY` (a dramatic red mode), `■ QUIET` (mute).

### Situations (the heart of it)

Nine situations. Keys **0–8** on the keyboard switch between them, and so does a command from the server. Each one tints the whole body, adds an effect, shows a big banner title with a live gauge, plays a short sound, and makes him say a sentence.

| Key | Situation | Colour | Gauge |
|---|---|---|---|
| 0 | NORMAL | cyan `#6fdcff` | none |
| 1 | BACKUP RUNNING | green `#39ff6a` | backup % and "x GB of 28 GB" |
| 2 | INTRUSION DETECTED | red `#ff2a1a`, blinking | failed logins and the attacker's address |
| 3 | OVERHEATING | orange `#ff7a1a` | CPU °C: cool / warm / hot / throttling |
| 4 | MEMORY PRESSURE | purple `#b86bff` | memory % and swap |
| 5 | DISK ALMOST FULL | amber `#ffb347` | SSD %, GB left |
| 6 | HIGH LOAD | white `#e8f4ff` | load average, cores |
| 7 | UPDATING | blue `#4aa8ff` | packages x of 27 |
| 8 | SERVICE DOWN | red `#ff4a3a`, blinking | services running x of 12 |

The banner text must follow the real value. For example, don't show "OVERHEATING" at 45 °C.

### His voice

- Record the voice with **Piper** (offline text-to-speech):
  - English: `en_GB-alan-medium`
  - Turkish (if wanted): `tr_TR-dfki-medium`. Make it slower and a bit deeper, with a faint metallic echo, and first give me 5–6 short samples to choose from.
- **On the server:** a small TTS service (Python, systemd, port 8082) with a queue. Add a terminal command `khoa say "text" --sit heat --value 63` that puts a line in the queue. The page checks the queue every 1.5 s and speaks each new line.
- **On a public website (no server):** pre-record every sentence as small mp3 files and play those.
- **LIVE mode:** while he speaks, the camera pushes in a little, the dashboard dims to about 18 %, a big title appears on the left, and captions appear under it word by word. Everything fades back about 2.5 s after the last word.

### Performance

- Add a **lite mode** (`?lite`, and automatically on phones, touch screens or narrow screens): lower pixel ratio, no bloom, about 25 % of the particles, no mountains or dust.
- Pause all animation when the tab is hidden or scrolled off screen.
- It must run smoothly on an old laptop (i5, 8 GB).

## The second page: `map.html` ("Command Map")

Use the same figure, smaller, in the middle. Around him, **nodes** connected by glowing wires:

- **The crew (cyan):** my AI agents. Each has a name, a role, a code, a command, "what it handles" (3 lines), "example requests" (2 lines) and an ID-card picture. **YOUR** crew: (list them, or ask Claude to invent 8)
- **The apps (amber):** the tools on my server, for example Cockpit, a file drive, a hosting panel, a test lab and a guide site.
- Clicking a node opens its ID card as a popup.
- When an agent "speaks", the figure turns towards it, raises an arm, the node lights up and the card opens.
- Add a **PANELS** switch to move between "Face of the Server" and "Command Map".

## Optional: put it on a public website

Wrap both pages in a **WordPress plugin** with two Elementor widgets:

- **Hero:** the figure only, full screen, with a "Meet him" button that plays the intro.
- **Stage:** the dashboard, with the 9 situation buttons and the crew buttons.

Details:
- Use only demo data, with no private addresses on the public site.
- Load the stage only when the visitor clicks.
- Switch language through Polylang (English default at `/`, other language at `/tr/`).
- The parent page talks to the pages with `postMessage` (`intro`, `sit`, `talk`, `pause`).
- I upload each plugin version myself. Back up before every upload.

## Finish

When it all works, prepare a **GitHub upload folder**: the pages, the tools, a README with screenshots and a "make it yours" section, a CHANGELOG, and the MIT licence. Then check that the upload matches my folder file by file.

---

### Tips for using this prompt

- **Go piece by piece.** The original took several long sessions. Ask for the figure first, then the dashboard, situations, voice, Command Map, and finally the website.
- **Keep the mockup step.** It saves hours of rebuilding.
- **If something looks wrong, say so right away.** For example "the cards have white edges". Claude fixes it, tests it, and then continues.
