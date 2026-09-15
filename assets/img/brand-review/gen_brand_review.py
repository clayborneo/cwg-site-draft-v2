#!/usr/bin/env python3
"""Generate site-draft-v2/brand-review.html (logo colors + name badge mockups for Melissa/Angela)."""
import pathlib
ROOT = pathlib.Path('/Users/clayborneo/Desktop/claude-code/cwg/site-draft-v2')

VARS = [
 ('a','Velvet Orchid + Sage Teal','#5E2D5E','#2F5D56','#C7A65A','As it appears on the draft site today. Plum lettering, teal "with", gold sweep.'),
 ('b','Midnight Navy + Sage Teal','#1E2A44','#2F5D56','#C7A65A','Navy lettering, teal "with", gold sweep. The most traditional read.'),
 ('c','Orchid, tone on tone','#5E2D5E','#B48AB7','#C7A65A','Plum lettering with a soft orchid "with". Quieter, all one family, no teal.'),
 ('d','Navy + Soft Orchid','#1E2A44','#B48AB7','#C7A65A','Navy lettering, orchid "with". Keeps a purple note without any teal.'),
 ('e','Sage Teal + Orchid','#2F5D56','#5E2D5E','#C7A65A','The current pair swapped: teal lettering, plum "with".'),
 ('f','Plum monochrome','#5E2D5E','#5E2D5E','#5E2D5E','Everything in plum, for one-color uses such as embroidery, a stamp, or a fax cover.'),
]
PALETTE = [('Velvet Orchid','#5E2D5E','signature'),('Midnight Navy','#1E2A44','depth'),('Sage Teal','#2F5D56','balance'),
           ('Brushed Gold','#C7A65A','warmth'),('Soft Orchid','#B48AB7','tint'),('Warm Taupe','#ADA79D','neutral'),('Soft Ivory','#F6F4EF','ground')]
PERSON = ('Angela Thomas', 'MSN, RN, CMC &middot; Founder &amp; CEO')

def card(k, name, p, s, a, note):
    return f'''
      <div class="card" id="var-{k}">
        <div class="art">
          <img class="lk" src="assets/img/brand-review/lockup-{k}.png" alt="Caring with Grace lockup, {name}">
          <img class="bd" src="assets/img/brand-review/badge-{k}.png" alt="CG badge, {name}">
        </div>
        <div class="meta">
          <div class="meta-head"><span class="letter">{k.upper()}</span><h3>{name}</h3></div>
          <p>{note}</p>
          <div class="swatches"><span style="background:{p}"></span><span style="background:{s}"></span><span style="background:{a}"></span><small>{p} &middot; {s} &middot; {a}</small></div>
        </div>
      </div>'''

def badge(k, name, p, s, a, style='light'):
    mark = f'<img class="nb-mark" src="assets/img/brand-review/badge-{k}.png" alt="">'
    if style in ('primary', 'secondary'):
        bg = p if style == 'primary' else s
        strip = a if style == 'primary' else p
        label = 'solid ' + ('lettering color' if style == 'primary' else '"with" color')
        return f"""
      <figure class="nb-wrap">
        <div class="nb nb-dark" style="background:{bg}; border-color:{bg};">
          {mark}
          <div class="nb-text nb-text-light">
            <span class="nb-script" style="color:#fff;">Caring <em style="color:rgba(255,255,255,.8);">with</em> Grace</span>
            <strong>{PERSON[0]}</strong><span>{PERSON[1]}</span>
          </div>
          <div class="nb-strip" style="background:{strip};"></div>
        </div>
        <figcaption>{k.upper()} &middot; {label}</figcaption>
      </figure>"""
    if style == 'band':
        return f"""
      <figure class="nb-wrap">
        <div class="nb nb-band">
          <div class="nb-bandtop" style="background:{p};"><span class="nb-script nb-script-band">Caring <em style="color:rgba(255,255,255,.8);">with</em> Grace</span></div>
          <div class="nb-bandbody">
            {mark.replace('nb-mark', 'nb-mark-sm')}
            <div class="nb-text"><strong>{PERSON[0]}</strong><span>{PERSON[1]}</span></div>
          </div>
          <div class="nb-strip" style="background:{a};"></div>
        </div>
        <figcaption>{k.upper()} &middot; color band, white body</figcaption>
      </figure>"""
    return f"""
      <figure class="nb-wrap">
        <div class="nb">
          {mark}
          <div class="nb-text">
            <span class="nb-script" style="color:{p};">Caring <em style="color:{s};">with</em> Grace</span>
            <strong>{PERSON[0]}</strong><span>{PERSON[1]}</span>
          </div>
          <div class="nb-strip" style="background:{a};"></div>
        </div>
        <figcaption>{k.upper()} &middot; ivory badge</figcaption>
      </figure>"""

def badge_row(v):
    k, name = v[0], v[1]
    return f'<div class="nb-row"><h3><span class="letter">{k.upper()}</span>{name}</h3><div class="nb-grid">' + ''.join(badge(*v[:5], style=s) for s in ('light','primary','secondary','band')) + '</div></div>'
cards = ''.join(card(*v) for v in VARS)
badges = ''.join(badge_row(v) for v in VARS)
darks = ''
sw = ''.join(f'<div class="pal"><span style="background:{h}"></span><strong>{n}</strong><small>{h} &middot; {r}</small></div>' for n, h, r in PALETTE)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Logo, Colors &amp; a Name Badge | Caring with Grace (review)</title>
  <meta name="robots" content="noindex">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Ephesis&family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="icon" type="image/png" href="assets/img/brand-v6/badge-karen-64.png">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{ --plum:#5E2D5E; --navy:#1E2A44; --teal:#2F5D56; --gold:#C7A65A; --ivory:#F6F4EF; --taupe:#ADA79D; --ink:#2B2226; --muted:#6b635f; --border:#E6E1D8; }}
    body {{ font-family:'DM Sans',sans-serif; color:var(--ink); background:#FBFAF7; line-height:1.6; -webkit-font-smoothing:antialiased; }}
    .container {{ max-width:1160px; margin:0 auto; padding:0 24px; }}
    .hero {{ background:linear-gradient(120deg,#fff 0%,var(--ivory) 100%); border-bottom:3px solid var(--gold); padding:52px 0 42px; }}
    .kicker {{ text-transform:uppercase; letter-spacing:.18em; font-size:.76rem; color:var(--teal); font-weight:700; margin-bottom:8px; }}
    h1 {{ font-family:'DM Serif Display',serif; font-weight:400; font-size:2.5rem; color:var(--navy); line-height:1.15; }}
    .hero p {{ max-width:760px; color:var(--muted); margin-top:12px; font-size:1.02rem; }}
    section {{ padding:52px 0 16px; }}
    section.alt {{ background:#fff; border-top:1px solid var(--border); border-bottom:1px solid var(--border); }}
    h2 {{ font-family:'DM Serif Display',serif; font-weight:400; font-size:1.9rem; color:var(--navy); margin-bottom:6px; }}
    .note {{ color:var(--muted); max-width:780px; margin-bottom:28px; }}
    .grid {{ display:grid; gap:24px; margin-bottom:40px; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); }}
    .card {{ background:#fff; border:1px solid var(--border); border-radius:10px; overflow:hidden; }}
    .card .art {{ display:flex; align-items:center; justify-content:center; gap:22px; padding:28px 22px; min-height:230px; background:var(--ivory); }}
    .card .art .lk {{ width:62%; height:auto; }}
    .card .art .bd {{ width:26%; height:auto; }}
    .card .meta {{ border-top:1px solid var(--border); padding:14px 18px 16px; }}
    .meta-head {{ display:flex; align-items:center; gap:10px; margin-bottom:4px; }}
    .letter {{ display:inline-flex; width:28px; height:28px; align-items:center; justify-content:center; border-radius:50%; background:var(--navy); color:#fff; font-weight:700; font-size:.85rem; }}
    .card .meta h3 {{ font-size:1.05rem; color:var(--navy); font-weight:600; }}
    .card .meta p {{ font-size:.9rem; color:var(--muted); }}
    .swatches {{ display:flex; align-items:center; gap:6px; margin-top:10px; }}
    .swatches span {{ width:26px; height:26px; border-radius:6px; border:1px solid rgba(0,0,0,.08); }}
    .swatches small {{ margin-left:8px; color:var(--taupe); font-size:.78rem; letter-spacing:.02em; }}
    .today {{ display:grid; grid-template-columns:1.2fr .8fr; gap:24px; margin-bottom:28px; }}
    @media (max-width:820px) {{ .today {{ grid-template-columns:1fr; }} }}
    .panel {{ border:1px solid var(--border); border-radius:10px; display:flex; align-items:center; justify-content:center; padding:34px; min-height:260px; }}
    .panel img {{ max-width:100%; height:auto; }}
    .panel.dark {{ background:var(--plum); }}
    .panel.ivory {{ background:var(--ivory); }}
    .panel-stack {{ display:grid; gap:24px; }}
    .palette {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:14px; margin-bottom:24px; }}
    .pal {{ background:#fff; border:1px solid var(--border); border-radius:10px; padding:10px; }}
    .pal span {{ display:block; height:64px; border-radius:6px; border:1px solid rgba(0,0,0,.06); margin-bottom:8px; }}
    .pal strong {{ display:block; font-size:.9rem; color:var(--navy); }}
    .pal small {{ color:var(--taupe); font-size:.76rem; }}
    .nb-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:22px 20px; margin-bottom:8px; }}
    .nb-grid .nb {{ max-width:340px; }}
    .nb-wrap {{ margin:0; }}
    .nb-wrap figcaption {{ font-size:.85rem; color:var(--muted); margin-top:10px; text-align:center; }}
    .nb {{ position:relative; width:100%; max-width:360px; aspect-ratio:2/1; margin:0 auto; background:#FFFDF9; border:1px solid #E2DCD0; border-radius:10px;
          box-shadow:0 14px 30px rgba(30,42,68,.16), 0 2px 4px rgba(30,42,68,.10); display:flex; align-items:center; gap:14px; padding:18px 20px 22px 18px; overflow:hidden; }}
    .nb-mark {{ width:26%; height:auto; flex-shrink:0; }}
    .nb-text {{ display:flex; flex-direction:column; line-height:1.2; min-width:0; }}
    .nb-script {{ font-family:'Ephesis',cursive; -webkit-text-stroke:.5px currentColor; font-size:1.42rem; -webkit-text-stroke:.3px currentColor; margin-bottom:6px; white-space:nowrap; }}
    .nb-script em {{ font-style:normal; font-size:.78em; margin:0 .2em; }}
    .nb-text strong {{ font-size:.98rem; white-space:nowrap; color:var(--navy); font-weight:700; letter-spacing:.01em; }}
    .nb-text span:last-child {{ font-size:.72rem; color:var(--muted); margin-top:3px; }}
    .nb-strip {{ position:absolute; left:0; right:0; bottom:0; height:7px; }}
    .nb-dark {{ padding:16px 20px 22px 20px; }}
    .nb-row {{ margin-bottom:34px; }}
    .nb-row h3 {{ display:flex; align-items:center; gap:10px; font-size:1.05rem; color:var(--navy); font-weight:600; margin-bottom:14px; }}
    .nb-band {{ flex-direction:column; align-items:stretch; gap:0; padding:0; }}
    .nb-bandtop {{ height:38%; display:flex; align-items:center; justify-content:center; }}
    .nb-script-band {{ color:#fff; font-size:1.3rem; margin:0; }}
    .nb-bandbody {{ flex:1; display:flex; align-items:center; gap:12px; padding:8px 18px 14px 16px; }}
    .nb-mark-sm {{ width:16%; height:auto; flex-shrink:0; }}
    .nb-lockup {{ width:33%; height:auto; flex-shrink:0; }}
    .nb-text-light strong {{ color:#fff; }}
    .nb-text-light span:last-child {{ color:rgba(255,255,255,.75); }}
    .howto {{ background:#fff; border:1px solid var(--border); border-left:4px solid var(--gold); border-radius:0 10px 10px 0; padding:20px 24px; max-width:780px; margin-bottom:30px; }}
    .howto h3 {{ font-size:1.05rem; color:var(--navy); margin-bottom:6px; }}
    .howto p, .howto li {{ font-size:.95rem; color:var(--muted); }}
    .howto ul {{ padding-left:20px; margin-top:6px; }}
    footer {{ padding:36px 0 60px; color:#8a827c; font-size:.84rem; }}
    footer a {{ color:var(--plum); }}
  </style>
</head>
<body>

<div class="hero">
  <div class="container">
    <div class="kicker">For review &middot; Logo &amp; colors &middot; September 2026</div>
    <h1>The logo, its colors, and a name badge</h1>
    <p>The design is settled, so this page is about color. Section one shows the logo as it now appears on the draft site. Section two shows the same artwork in six color combinations, lettered A to F. Section three puts each one on a name badge so you can judge it at real-world size. Nothing here is final until you say so.</p>
    <p>One change since the last round: the lettering in the full logo, the round badge, and the website header now all use the same script, the one from the round badge (the C with the small inner curl and the open G). <a href="brand-home.html">See any palette on the draft home page &rarr;</a></p>
  </div>
</div>

<section>
  <div class="container">
    <h2>1. The logo today</h2>
    <p class="note">The full lockup, the reversed version for dark backgrounds, and the round CG badge used as the site's favicon and header mark. Below them, the seven colors the draft site is built on.</p>
    <div class="today">
      <div class="panel ivory"><img src="assets/img/brand-review/lockup-a.png" alt="Caring with Grace lockup" style="max-width:520px;"></div>
      <div class="panel-stack">
        <div class="panel dark"><img src="assets/img/brand-review/lockup-white.png" alt="Reversed lockup on plum" style="max-width:300px;"></div>
        <div class="panel ivory"><img src="assets/img/brand-review/badge-a.png" alt="CG badge" style="max-width:150px;"></div>
      </div>
    </div>
    <div class="palette">{sw}</div>
  </div>
</section>

<section class="alt">
  <div class="container">
    <h2>2. Color variations</h2>
    <p class="note">Same drawing every time. What changes is the lettering color, the color of "with" and the second set of leaves, and the sweep. Gold stays as the warm accent in all but the one-color version. When you reply, the letter is enough. To see a palette in context, <a href="brand-home.html">open the home page try-on</a> and pick a letter in the corner.</p>
    <div class="grid">{cards}</div>
  </div>
</section>

<section>
  <div class="container">
    <h2>3. On a name badge</h2>
    <p class="note">A standard 3 by 1.5 inch magnetic badge, four ways for each palette: an ivory badge with the round mark and the name in script, a solid badge in the lettering color, a solid badge in the "with" color, and a color band over a white body. Every badge carries the round mark. Angela's name is a stand-in for whoever wears it.</p>
    <div class="nb-grid">{badges}{darks}</div>
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="howto">
      <h3>How to respond</h3>
      <p>Reply with a letter for the logo colors (or "A" to keep it as is). If a badge style stands out, name it too. Two things still need a leadership call and are unchanged here:</p>
      <ul>
        <li>The round mark reads "C" and "G" with a small "with" between them. It could read "CwG" instead if you prefer the initials.</li>
        <li>Karen's deck asks leadership to pick one G-monogram variation as the master mark; this page uses her approved round badge.</li>
      </ul>
    </div>
  </div>
</section>

<footer>
  <div class="container">Prepared by Clay for Angela and Melissa &middot; artwork is the draft-site logo recolored, not redrawn &middot; <a href="index.html">back to the draft site</a></div>
</footer>

</body>
</html>
'''
(ROOT / 'brand-review.html').write_text(html)
print('written', len(html))
