// Preview palette switch for the review team. Open any page with ?palette=f
// (plum monochrome) and the whole draft site takes that palette for the tab.
(function () {
  var VARS = {
    f: {'--primary': '#5E2D5E', '--primary-dark': '#442044', '--primary-light': '#EFEAEF', '--brand-pink': '#5E2D5E', '--periwinkle': '#A68CA6', '--soft-pink': '#A68CA6', '--teal': '#5E2D5E', '--secondary-dark': '#502650', '--secondary-light': '#ECE6EC', '--gold': '#5E2D5E', '--secondary': '#5E2D5E'}
  };
  var m = location.search.match(/[?&]palette=([a-z])/);
  var k = m ? m[1] : null;
  try {
    if (k === 'off') { sessionStorage.removeItem('cwg-palette'); k = null; }
    else if (k) sessionStorage.setItem('cwg-palette', k);
    else k = sessionStorage.getItem('cwg-palette');
  } catch (e) {}
  if (!k || !VARS[k]) return;
  var root = document.documentElement;
  Object.keys(VARS[k]).forEach(function (n) { root.style.setProperty(n, VARS[k][n]); });
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('img.site-logo-mark').forEach(function (i) { i.src = 'assets/img/brand-review/badge-' + k + '.png'; });
    document.querySelectorAll('img.hero-lockup-img').forEach(function (i) { i.src = 'assets/img/brand-review/lockup-' + k + '.png'; });
    document.querySelectorAll('a[href]').forEach(function (a) {
      var h = a.getAttribute('href');
      if (/^[a-z0-9-]+\.html(#.*)?$/i.test(h)) a.setAttribute('href', h.replace(/\.html/, '.html?palette=' + k));
    });
  });
})();
