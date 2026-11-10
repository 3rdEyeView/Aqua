# Arroyo's Lawn Care — V4 hero concept with a Higgsfield-generated transition (2026-11-10), NOT published

Preview only. The live page (WordPress page 1716) was fetched read-only as the base; nothing was saved in WordPress or
Elementor, no media was uploaded to Axiom, and the live `#lead-demo` walkthrough (snippet 1818) was not touched.

- `arroyo-v4-higgsfield-preview.html`: the deliverable. Offline copy of the current live page with only the hero media changed.
- `arroyo-current-hero-reference.html`: the same offline copy with the existing drone hero, for comparison.
- `shots/side-by-side-desktop.mp4`, `shots/side-by-side-mobile.mp4`, `shots/before-after-*.jpg`: comparison material.
- `python3 -I fetch_live.py` (read-only download of the page's CSS, Elementor scripts and images), `python3 -I build.py`, `node check.js`.
  Both files have tracking, chat, the lead walkthrough and every other third-party script stripped, and make no network requests.

## The one change: the hero sequence (`v4.js`, `v4.css`)
1. Arroyo's own drone footage, last 7.04 s of their clip (real).
2. A 6.58 s transition generated with Higgsfield (`generate_video`, model `minimax_h3`, 2560×1440, job
   `1c2ea0d7-7fc4-4b58-bcb8-baaccc067b89`, 12 credits: quoted 10 for 5 s, run at 6 s; the account balance read 110 before and 98 after). Start keyframe = the drone clip's real last frame; end keyframe = Arroyo's real photo `clean-1011`
   (bottle palms and ti plants), cropped to 16:9. Everything between those two frames is AI-generated, including the invented
   wider views of both properties and the whip-blur between them.
3. Cross-fade to the real photo itself, held 6.5 s, then the sequence restarts.
A label in the hero always says which of the three is on screen ("AI-generated transition" in orange). The generated footage
appears nowhere else; the project gallery is unchanged. Headline, buttons and badges are the live page's own, with an extra
shade behind them from the generated part onwards. Reduced motion: no video, the real photo is shown.

## How the keyframes got to Higgsfield
This container cannot reach Higgsfield's upload host, so the two keyframes were prepared in Higgsfield's sandbox from the
already-public drone clip (axiomsystems.systems) and photo (arroyoslawncare.com). A personal cloud environment "Aqua" was
created (with approval) so the result could be downloaded.
