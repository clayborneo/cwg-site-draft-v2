#!/usr/bin/env python3
"""Build site-draft-v2/brand-home.html: a copy of the draft home page with a floating
color-variation switcher (A-G) that swaps CSS variables and the logo images live."""
import pathlib, re
ROOT = pathlib.Path('/Users/clayborneo/Desktop/claude-code/cwg/site-draft-v2')
VARS = [
 ('a','Velvet Orchid + Sage Teal','#5E2D5E','#2F5D56','#C7A65A'),
 ('b','Midnight Navy + Sage Teal','#1E2A44','#2F5D56','#C7A65A'),
 ('c','Orchid, tone on tone','#5E2D5E','#B48AB7','#C7A65A'),
 ('d','Navy + Soft Orchid','#1E2A44','#B48AB7','#C7A65A'),
 ('e','Sage Teal + Orchid','#2F5D56','#5E2D5E','#C7A65A'),
 ('f','Plum monochrome','#5E2D5E','#5E2D5E','#5E2D5E'),
]
def hex2rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def rgb2hex(c): return '#%02X%02X%02X' % tuple(max(0,min(255,int(round(v)))) for v in c)
def mix(a, b, t):  # a toward b by t
    return tuple(a[i]*(1-t)+b[i]*t for i in range(3))
def tokens(p, s, a):
    P, S, A = hex2rgb(p), hex2rgb(s), hex2rgb(a)
    return {
        '--primary': p,
        '--primary-dark': rgb2hex(mix(P,(0,0,0),0.28)),
        '--primary-light': rgb2hex(mix(P,(255,255,255),0.90)),
        '--brand-pink': p,
        '--periwinkle': rgb2hex(mix(P,(255,255,255),0.45)),
        '--soft-pink': rgb2hex(mix(P,(255,255,255),0.45)),
        '--teal': s,
        '--secondary-dark': rgb2hex(mix(S,(0,0,0),0.15)),
        '--secondary-light': rgb2hex(mix(S,(255,255,255),0.88)),
        '--gold': a,
        '--secondary': a,
    }
js_vars = ',\n'.join(
    "  %s: {name: %r, tokens: {%s}}" % (k, name, ', '.join("'%s': '%s'" % kv for kv in tokens(p,s,a).items()))
    for k, name, p, s, a in VARS)

t = (ROOT / 'index.html').read_text()
# mark the two logo images so the switcher can swap them
t = t.replace('<img src="assets/img/brand-v6/badge-karen.png" alt="" width="46" height="46" class="site-logo-mark">',
              '<img src="assets/img/brand-review/badge-a.png" alt="" width="46" height="46" class="site-logo-mark" id="sw-badge">', 1)
t = t.replace('<img class="hero-lockup-img" src="assets/img/brand-v6/lockup-v1.png" alt="Caring with Grace">',
              '<img class="hero-lockup-img" src="assets/img/brand-review/lockup-a.png" alt="Caring with Grace" id="sw-lockup">', 1)
t = t.replace('<title>Caring with Grace | Aging Life Care Professionals in Dallas</title>',
              '<title>Home page color try-on | Caring with Grace (review)</title>', 1)
t = t.replace('<link rel="canonical" href="https://clayborneo.github.io/cwg-site-draft-v2/">', '', 1)
# draft banner becomes the switcher explanation
t = re.sub(r'<div class="draft-banner">.*?</div>',
           '<div class="draft-banner">Color try-on: pick a letter in the panel to see the draft home page in that palette. <a href="brand-review.html">Back to the logo review &rarr;</a></div>', t, count=1, flags=re.S)
assert 'id="sw-badge"' in t and 'id="sw-lockup"' in t

buttons = ''.join(
    '<button type="button" data-var="%s" title="%s"><span class="sw-dot" style="background:%s"></span><span class="sw-dot" style="background:%s"></span><b>%s</b></button>'
    % (k, name, p, s, k.upper()) for k, name, p, s, a in VARS)
panel = '''
<div id="color-switch" aria-label="Color variation">
  <div class="sw-title">Try a palette</div>
  <div class="sw-buttons">%s</div>
  <div class="sw-name" id="sw-name">A &middot; Velvet Orchid + Sage Teal</div>
</div>
<style>
  #color-switch { position: fixed; right: 18px; bottom: 18px; z-index: 999; background: #fff; border: 1px solid #E3DED4; border-radius: 12px; box-shadow: 0 14px 34px rgba(30,42,68,.18); padding: 12px 14px 10px; width: 232px; font-family: 'DM Sans', sans-serif; }
  #color-switch .sw-title { font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; color: #6b635f; margin-bottom: 8px; }
  #color-switch .sw-buttons { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
  #color-switch button { display: flex; align-items: center; justify-content: center; gap: 3px; border: 1px solid #E3DED4; background: #fff; border-radius: 8px; padding: 6px 4px; cursor: pointer; font-family: inherit; }
  #color-switch button b { font-size: .8rem; color: #1E2A44; margin-left: 2px; }
  #color-switch button.active { border-color: #1E2A44; box-shadow: 0 0 0 2px rgba(30,42,68,.12); }
  #color-switch .sw-dot { width: 10px; height: 10px; border-radius: 50%%; display: inline-block; }
  #color-switch .sw-name { font-size: .78rem; color: #1E2A44; margin-top: 8px; }
  @media (max-width: 600px) { #color-switch { right: 10px; bottom: 10px; width: 200px; } }
</style>
<script>
(function(){
  var VARS = {
%s
  };
  var root = document.documentElement;
  function apply(k){
    var v = VARS[k]; if (!v) return;
    Object.keys(v.tokens).forEach(function(name){ root.style.setProperty(name, v.tokens[name]); });
    document.getElementById('sw-lockup').src = 'assets/img/brand-review/lockup-' + k + '.png';
    document.getElementById('sw-badge').src = 'assets/img/brand-review/badge-' + k + '.png';
    document.getElementById('sw-name').textContent = k.toUpperCase() + ' \\u00b7 ' + v.name;
    document.querySelectorAll('#color-switch button').forEach(function(b){ b.classList.toggle('active', b.dataset.var === k); });
    try { history.replaceState(null, '', '#' + k); } catch (e) {}
  }
  document.querySelectorAll('#color-switch button').forEach(function(b){ b.addEventListener('click', function(){ apply(b.dataset.var); }); });
  var start = (location.hash || '#a').slice(1);
  apply(VARS[start] ? start : 'a');
})();
</script>
''' % (buttons, js_vars)
t = t.replace('<script src="assets/js/main.js"></script>', panel + '<script src="assets/js/main.js"></script>', 1)
(ROOT / 'brand-home.html').write_text(t)
print('brand-home.html written')
