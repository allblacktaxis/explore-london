/* App Store screenshots of Explore London (plain, no frames or headlines).
   Run by .github/workflows/screenshots.yml:  node app/screenshots/take.js <website folder> <map tiles file> <output folder>
   The website is served locally and the map tiles come from the downloaded file, so the map shows our real map. */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http');
const [site, tilesFile, out] = process.argv.slice(2);
const tiles = fs.readFileSync(tilesFile);
const TYPES = {'.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.pbf': 'application/x-protobuf', '.ico': 'image/x-icon', '.webmanifest': 'application/manifest+json'};

/* a tiny web server for the website folder */
const server = http.createServer((q, r) => {
  let f = decodeURIComponent(q.url.split('?')[0]); if (f.endsWith('/')) f += 'index.html';
  const p = path.join(site, f);
  fs.readFile(p, (err, data) => { if (err) { r.writeHead(404); return r.end(); } r.writeHead(200, {'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream'}); r.end(data); });
}).listen(8790);

/* the screens to capture */
const SAVED = [347, 348, 160, 42, 399, 136];          // My List: Tower of London, Westminster Abbey, Ye Olde Cheshire Cheese, Borough Market, Sherlock Holmes Museum, The Old Bank of England
const SHOTS = [
  ['01-home', '#/', 2500],
  ['02-map', '#/map', 12000],
  ['03-place', '#/place/347', 6000],             // Tower of London
  ['04-walk', '#/walk/music-trail', 12000],
  ['05-day-plans', '#/plans', 3000],
  ['06-my-list', '#/list', 4000]
];
const DEVICES = [
  ['iphone-6.9in', {viewport: {width: 440, height: 956}, deviceScaleFactor: 3, isMobile: true, hasTouch: true, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'}],
  ['ipad-13in', {viewport: {width: 1032, height: 1376}, deviceScaleFactor: 2, isMobile: true, hasTouch: true, userAgent: 'Mozilla/5.0 (iPad; CPU OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'}]
];

(async () => {
  const browser = await chromium.launch();
  for (const [dev, opts] of DEVICES) {
    fs.mkdirSync(path.join(out, dev), {recursive: true});
    const ctx = await browser.newContext({...opts, geolocation: {latitude: 51.5117, longitude: -0.1240}, permissions: ['geolocation'], locale: 'en-GB', timezoneId: 'Europe/London'});
    /* map tiles: answer requests for the online tiles file from the downloaded copy */
    await ctx.route(/maptiles\.allblacktaxi\.co\.uk/, route => {
      const req = route.request(), cors = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Expose-Headers': 'Content-Range, Content-Length, ETag'};
      if (req.method() === 'OPTIONS') return route.fulfill({status: 204, headers: cors});
      const m = /bytes=(\d+)-(\d+)/.exec(req.headers()['range'] || '');
      const a = m ? +m[1] : 0, b = m ? Math.min(+m[2], tiles.length - 1) : tiles.length - 1;
      route.fulfill({status: m ? 206 : 200, headers: {...cors, 'Content-Type': 'application/octet-stream', 'Content-Range': `bytes ${a}-${b}/${tiles.length}`}, body: tiles.subarray(a, b + 1)});
    });
    await ctx.addInitScript(saved => {
      /* show the screens as the app shows them (no "add to home screen" help); the map tiles come from the online file above */
      window.Capacitor = {isNativePlatform: () => true, getPlatform: () => 'ios', nativePromise: async (plugin, method) => {
        if (plugin === 'AppTiles') return {available: false};
        if (plugin === 'Geolocation') return {coords: {latitude: 51.5117, longitude: -0.1240, accuracy: 10}};
        if (plugin === 'CapacitorUpdater') return method === 'list' ? {bundles: []} : {};
        return {};
      }};
      try { localStorage.setItem('el_seen', '1'); localStorage.setItem('el_welcome', '1'); localStorage.setItem('el_a2_off', '1'); localStorage.setItem('el_saved', JSON.stringify(saved)); } catch (e) {}
    }, SAVED);
    const page = await ctx.newPage();
    for (const [name, hash, wait] of SHOTS) {
      await page.goto('http://localhost:8790/' + hash);
      await page.waitForTimeout(wait);
      await page.screenshot({path: path.join(out, dev, name + '.png')});
      console.log(dev, name, await page.evaluate(() => (window.vecStyle && window.vecStyle.sources.openmaptiles.url) || ''), await page.evaluate(() => { try { return sessionStorage.getItem('el_vec'); } catch (e) { return ''; } }));
    }
    await ctx.close();
  }
  await browser.close(); server.close();
})();
