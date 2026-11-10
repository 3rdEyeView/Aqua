"""Arroyo V4 preview: an offline copy of the CURRENT live page (live.html, fetched read-only) with only the hero media swapped.
Outputs  arroyo-v4-higgsfield-preview.html  (real drone footage -> AI-generated transition -> real project photo)
and      arroyo-current-hero-reference.html (same offline copy with the existing drone hero, for side-by-side comparison).
Nothing here talks to WordPress; tracking, chat and the #lead-demo walkthrough are stripped from both files."""
import base64, html, json, mimetypes, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); rd = lambda *p: open(os.path.join(HERE, *p), encoding="utf8").read()
IDX = json.load(open(os.path.join(HERE, "live-assets", "index.json")))
def uri(path):
    mime = {".woff2": "font/woff2", ".webp": "image/webp", ".mp4": "video/mp4"}.get(os.path.splitext(path)[1]) or mimetypes.guess_type(path)[0]
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(HERE, path), "rb").read()).decode()
def asset(url): return os.path.join("live-assets", IDX[html.unescape(url)])
KEEP_JS = ("hello-frontend", "frontend-handlers", "accordion-selected-state-handler", "alpinejs")
KEEP_INLINE = ("axm-menu-js", "arl-demo-js")
POSTER_LIVE = "https://axiomsystems.systems/wp-content/uploads/2026/11/arroyos-demo-hero-poster.jpg"

def build(variant):
    s = rd("live.html")
    # --- strip the live #lead-demo walkthrough, tracking pixels, and every script we do not explicitly keep
    s = re.sub(r'<style id="axl-lead-css">.*?</style>\s*<script id="axl-lead-early">.*?</script>', "", s, flags=re.S)
    s = re.sub(r'<template id="axl-lead-tpl">.*?</template>\s*<script id="axl-lead-js">.*?</script>', "", s, flags=re.S)
    assert "axl-lead" not in s
    s = re.sub(r"<noscript>.*?</noscript>", "", s, flags=re.S)
    s = re.sub(r'<img[^>]+(?:clickcease|facebook\.com/tr)[^>]*>', "", s)
    def script(m):
        attrs, body = m.group(1), m.group(2)
        src = re.search(r'src=["\']([^"\']+)', attrs); sid = re.search(r'id=["\']([^"\']+)', attrs)
        if src:
            if any(k in src.group(1) for k in KEEP_JS): return "<script>" + rd(asset(src.group(1))).replace("</script", "<\\/script") + "</script>"
            return ""
        return m.group(0) if sid and sid.group(1) in KEEP_INLINE else ""
    s = re.sub(r"<script([^>]*)>(.*?)</script>", script, s, flags=re.S)
    # --- stylesheets inline; fonts embedded (same two families the page uses)
    def link(m):
        tag = m.group(0); href = re.search(r'href=["\']([^"\']+)', tag)
        if "stylesheet" in tag and href and "axiomsystems.systems" in href.group(1):
            return "<style>" + rd(asset(href.group(1))) + "</style>"
        return ""
    s = re.sub(r"<link[^>]*>", link, s)
    fonts = re.sub(r"url\((fonts/[^)]+)\)", lambda m: f"url({uri(os.path.join('..', '2026-11-10-arroyos-v2', m.group(1)))})", rd("..", "2026-11-10-arroyos-v2", "fonts", "fonts.css"))
    s = s.replace("</head>", "<style>" + fonts + "</style>\n</head>", 1)
    # --- images inline
    def img(m):
        tag = re.sub(r'\s(?:srcset|sizes)="[^"]*"', "", m.group(0)); src = re.search(r'src="([^"]+)"', tag).group(1)
        return tag.replace(src, uri(asset(src)))
    s = re.sub(r"<img[^>]*>", img, s)
    # --- Cloudflare-obfuscated email links back to plain ones
    s = re.sub(r'href="/cdn-cgi/l/email-protection#[0-9a-f]+"', 'href="mailto:info@arroyoslawncare.com"', s)
    s = re.sub(r'<span class="__cf_email__"[^>]*>.*?</span>', "info@arroyoslawncare.com", s, flags=re.S)
    # --- hero media
    poster = uri("assets/hero-v4-poster.jpg" if variant == "v4" else "assets/hero-current-poster.jpg")
    assert POSTER_LIVE in s; s = s.replace(POSTER_LIVE, poster).replace(POSTER_LIVE.replace("/", "\\/"), poster)
    s = re.sub(r'\s(?:x-data|x-bind)="(?:eBackgroundVideo\w+|rootState|controlsWrapper|playButton|pauseButton)"', "", s)
    old = re.search(r'<video class="e-background-video__media".*?</video>', s, re.S).group(0)
    if variant == "v4":
        new = ('<video class="e-background-video__media" aria-hidden="true" muted playsinline preload="auto" poster="%s" src="%s"></video>'
               '<img class="v4-still" alt="" src="%s"><div class="v4-shade"></div><p class="v4-chip" aria-live="polite"><i></i><span></span></p>' % (poster, uri("assets/hero-v4.mp4"), uri("assets/hero-v4-still.jpg")))
        s = s.replace("</body>", "<style>" + rd("v4.css") + "</style>\n<script>\n" + rd("v4.js") + "</script>\n</body>", 1)
        note = "Preview only · not published · V4 concept: real drone footage, one AI-generated transition (Higgsfield), then a real Arroyo project photo"
    else:
        new = '<video class="e-background-video__media" aria-hidden="true" autoplay muted loop playsinline preload="auto" poster="%s" src="%s"></video>' % (poster, uri("assets/hero-current.mp4"))
        s = s.replace("</body>", "<script>\n" + rd("current.js") + "</script>\n</body>", 1)
        note = "Offline reference copy of the current live page (existing drone hero) · not published"
    s = s.replace(old, new)
    s = re.sub(r"(<body[^>]*>)", r'\1<div style="background:#f8981d;color:#0c1509;font:600 13px/1.35 Figtree,system-ui,sans-serif;text-align:center;padding:6px 12px">' + note + "</div>", s, count=1)
    s = re.sub(r"<title>.*?</title>", "<title>Arroyo’s Lawn Care — %s (not live)</title>" % ("V4 Higgsfield preview" if variant == "v4" else "current hero reference"), s, flags=re.S)
    left = sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"', s)))
    out = "arroyo-v4-higgsfield-preview.html" if variant == "v4" else "arroyo-current-hero-reference.html"
    open(os.path.join(HERE, out), "w", encoding="utf8").write(s)
    print(out, round(len(s.encode()) / 1e6, 2), "MB; remaining absolute links:", [u for u in left if not re.search(r"facebook\.com/profile|instagram\.com|flickr\.com|creativecommons\.org", u)])
build("v4"); build("current")
