/* ===== Explore London · desktop layout (7 Nov 2026) =====
   Add ONE line to index.html, just before </body> (after the app's own script):
     <script src="desktop.js"></script>
   Phones are not changed at all (tablets held upright get the phone layout at full width, see index.html). On landscape screens 1024px and wider the app gets:
   a left-hand menu instead of the bottom tab bar, wider pages, lists in columns,
   a full-height map, walks with the map beside the stops, and place pages in two columns. */
(function () {
  var DESK = '(min-width: 1024px) and (orientation: landscape)';
  var css = `
@media ${DESK} {
  :root{--el-side:248px;--el-wide:1180px;--el-toph:120px}
  body{background:#E6EBF2}
  #app{max-width:none;margin:0 0 0 var(--el-side);min-height:100vh;box-shadow:none}
  #app.el-nonav{margin:0 auto;max-width:480px}

  /* bottom tab bar -> left-hand menu */
  nav.tabs{left:0;top:0;bottom:0;right:auto;transform:none;width:var(--el-side);max-width:none;display:flex;flex-direction:column;gap:4px;padding:22px 14px 18px;grid-template-columns:none}
  nav.tabs::before{content:'Explore London';display:block;font:800 22px/1.1 'Archivo','Poppins',sans-serif;color:#fff;padding:4px 14px 6px}
  nav.tabs::after{content:'Picked by London cabbies \\00B7  free, no sign-up';margin-top:auto;padding:12px 14px 0;font-size:13px;line-height:1.4;color:#A9B6CE;border-top:1px solid rgba(255,255,255,.12)}
  nav.tabs a:first-of-type{margin-top:18px}
  nav.tabs a{flex-direction:row;justify-content:flex-start;gap:14px;min-height:50px;padding:0 14px;border-radius:12px;font-size:16px;position:relative;transition:background .12s,color .12s}
  nav.tabs a:hover{background:rgba(255,255,255,.08);color:#fff}
  nav.tabs a.on{background:rgba(255,255,255,.12)}
  nav.tabs a i{position:absolute;left:0;top:12px;bottom:12px;width:4px;height:auto;margin:0;border-radius:0 3px 3px 0}

  /* wider pages, content kept to a comfortable reading width */
  .top{padding-left:max(32px,calc((100% - var(--el-wide)) / 2)) !important;padding-right:max(32px,calc((100% - var(--el-wide)) / 2)) !important}
  #app:not(.el-place):not(.el-walk) .content{padding-left:max(32px,calc((100% - var(--el-wide)) / 2));padding-right:max(32px,calc((100% - var(--el-wide)) / 2))}
  .top{padding-top:18px;padding-bottom:18px}
  .top .search{max-width:640px}
  .content{padding-top:22px;padding-bottom:56px;gap:16px}
  .content .bigbtn,.content .ghost{max-width:460px}
  .content .row .bigbtn,.content .row .ghost{max-width:none}
  .toast{bottom:32px;left:calc(50% + var(--el-side) / 2)}

  /* Home tiles: one long row of tiles, or the grouped tiles two groups side by side */
  .tiles{grid-template-columns:repeat(8,minmax(0,1fr));gap:12px}
  .el-tgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 32px}
  .el-tgroup{display:flex;flex-direction:column;gap:8px;min-width:0}
  .el-tgroup .tiles{grid-template-columns:repeat(4,minmax(0,1fr))}
  .tile{min-height:104px}
  .tile .ic{width:52px;height:52px;border-radius:26px}
  .tile span.l{font-size:14px}

  /* side-scrolling rows become wrapping rows (no swiping with a mouse) */
  .hscroll{flex-wrap:wrap;overflow:visible;margin:0;padding:0}
  .ncard{flex:0 0 180px}.ncard.more{flex-basis:140px}
  .wcard{width:210px}

  /* lists in columns */
  .el-grid:not([style*="display: none"]):not([style*="display:none"]){display:grid !important;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:10px;align-items:stretch;align-content:start;grid-auto-rows:min-content}
  .el-grid > :not(.row-card){grid-column:1/-1}
  .row-card{padding:10px}
  .cpills,.pills{grid-template-columns:repeat(6,minmax(0,1fr))}
  .filters{max-width:1000px;flex-wrap:nowrap}
  .filters.four select{flex:1 1 0}

  /* hover feedback for mouse users */
  .row-card,.tile,.wcard,.ncard{transition:transform .12s,box-shadow .12s}
  .row-card:hover,.wcard:hover,.ncard:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(15,30,61,.14)}
  .tile:hover{transform:translateY(-2px)}
  .cpill:hover,.chip:hover,.hpill:hover{filter:brightness(.96)}

  /* place page: photo across the top, details left, story + nearby right */
  #app.el-place{display:grid;grid-template-columns:minmax(0,1fr) 380px;column-gap:28px;align-content:start;padding:28px max(32px,calc((100% - var(--el-side) - var(--el-wide)) / 2)) 56px}
  #app.el-place > .hero{grid-column:1/-1;height:380px;border-radius:22px;overflow:hidden}
  #app.el-place.el-nophoto > .hero{height:240px}
  #app.el-place > .credit{grid-column:1/-1;padding:6px 4px 0}
  #app.el-place > .sheet{grid-column:1;margin-top:18px;border-radius:22px;padding:24px 28px;align-self:start}
  #app.el-place > .sheet h1{font-size:34px}
  #app.el-place > .sheet p{font-size:17px;max-width:70ch}
  #app.el-place > .content{grid-column:2;padding:18px 0 0}
  #app.el-place > :not(.hero):not(.credit):not(.sheet):not(.content):not(nav){grid-column:1/-1}
  #app.el-place > .content [style*="repeat(2"]{grid-template-columns:1fr !important}
  #app.el-place .hero .acts{left:20px;right:20px;top:18px}

  /* map page: map fills the screen under the header */
  .map{height:calc(100vh - var(--el-toph)) !important;min-height:480px}
  .map .overlay:not(.iconbtn){right:auto;width:420px}

  /* walk page: stops on the left, map on the right, map stays put while you scroll */
  #app.el-walk{display:grid;grid-template-columns:minmax(380px,1fr) minmax(0,1.25fr);grid-template-rows:auto 1fr;align-items:start}
  #app.el-walk > .top{grid-column:1/-1}
  #app.el-walk > .el-walkmap{grid-column:2;grid-row:2;position:sticky !important;top:var(--el-toph);height:calc(100vh - var(--el-toph)) !important}
  #app.el-walk > .content{grid-column:1;grid-row:2;padding:24px 28px 56px 32px}
  #app.el-walk > :not(.top):not(.el-walkmap):not(.content):not(nav){grid-column:1}
}`;
  var st = document.createElement('style'); st.id = 'el-desktop-css'; st.textContent = css; document.head.appendChild(st);

  var mq = window.matchMedia(DESK), app = document.getElementById('app'), busy = false, lastWalkFit = null;
  function getMap() { try { return typeof emap !== 'undefined' ? emap : null; } catch (e) { return null; } }

  /* Home: put each "heading + tiles" pair in a box, and the boxes two across */
  function groupTiles() {
    var ts = Array.prototype.slice.call(app.querySelectorAll('.tiles')).filter(function (t) { return !t.closest('.el-tgroup'); });
    if (ts.length < 2 || !ts.every(function (t) { return t.parentNode === ts[0].parentNode; })) return;
    var parent = ts[0].parentNode, grid = document.createElement('div'); grid.className = 'el-tgrid';
    var first = ts[0].previousElementSibling && !ts[0].previousElementSibling.querySelector('.tiles') && !ts[0].previousElementSibling.matches('.tiles,a,.bigbtn,.hscroll') ? ts[0].previousElementSibling : ts[0];
    parent.insertBefore(grid, first);
    ts.forEach(function (t) {
      var g = document.createElement('div'); g.className = 'el-tgroup';
      var h = t.previousElementSibling;
      if (h && h !== grid && !h.matches('.tiles,a,.bigbtn,.hscroll,.el-tgrid') && !h.querySelector('.tiles')) g.appendChild(h);
      g.appendChild(t); grid.appendChild(g);
    });
  }

  function scan() {
    if (busy) return; busy = true;
    try {
      var on = mq.matches, root = document.documentElement;
      var nav = app.querySelector('nav.tabs');
      app.classList.toggle('el-nonav', !nav);

      /* place page */
      app.classList.toggle('el-place', !!(app.querySelector(':scope > .hero') && app.querySelector(':scope > .sheet')));

      /* walk page: a map strip straight under the header (not the full Map tab, not inside My List) */
      var leaf = document.getElementById('leaf'), box = leaf && leaf.parentElement;
      var isWalk = !!(box && box.parentElement === app && !box.classList.contains('map'));
      app.classList.toggle('el-walk', isWalk);
      app.querySelectorAll('.el-walkmap').forEach(function (b) { if (b !== box || !isWalk) b.classList.remove('el-walkmap'); });
      if (isWalk) box.classList.add('el-walkmap');
      var hero = app.querySelector(':scope > .hero');
      app.classList.toggle('el-nophoto', !!hero && !/url\(/.test(hero.style.backgroundImage));
      var top = app.querySelector(':scope > .top');
      root.style.setProperty('--el-toph', (top ? top.offsetHeight : 0) + 'px');

      if (!on) return;

      /* any container holding 4+ place rows becomes a multi-column grid */
      app.querySelectorAll('.row-card').forEach(function (r) {
        var p = r.parentElement;
        if (p && !p.classList.contains('el-grid') && p.querySelectorAll(':scope > .row-card').length >= 4 && p.id !== 'app') p.classList.add('el-grid');
      });
      groupTiles();

      /* maps need telling when their box changes size */
      var m = getMap();
      if (m && leaf && document.body.contains(leaf)) {
        requestAnimationFrame(function () {
          try {
            m.resize();
            if (isWalk && lastWalkFit !== location.hash && m._elPts) {
              lastWalkFit = location.hash;
              if (m._elPts.length) fitTo(m, m._elPts, 50, 16);
            }
          } catch (e) {}
        });
      }
      if (!isWalk) lastWalkFit = null;
    } finally { busy = false; }
  }

  var t = null;
  new MutationObserver(function () { clearTimeout(t); t = setTimeout(scan, 30); }).observe(app, {childList: true, subtree: true});
  addEventListener('resize', function () { clearTimeout(t); t = setTimeout(scan, 80); });
  if (mq.addEventListener) mq.addEventListener('change', scan);

  /* "/" jumps to the search box, as on most websites */
  addEventListener('keydown', function (e) {
    if (!mq.matches || e.key !== '/' || /INPUT|TEXTAREA|SELECT/.test((document.activeElement || {}).tagName || '')) return;
    var q = app.querySelector('input[type=search]'); if (q) { e.preventDefault(); q.focus(); }
  });
  scan();
})();
