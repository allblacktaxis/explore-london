# Explore London: iPhone and Android apps

The apps are the website wrapped in a native app shell ([Capacitor](https://capacitorjs.com)).

- **App ID** (same as the existing App Store app): `uk.co.allblacktaxis.explorelondon`
- **Version:** 2.0. The build number goes up on every cloud build.

## How it works

1. **The app has its own copy of the website.** `scripts/web_bundle.py --www www` copies the website files into `app/www`, and that copy is built into the app. So the app opens straight away and works with no signal.
2. **The map tiles are built in.** The cloud build downloads `map-tiles-v3.pmtiles` from the tiles server into `www/tiles/map.pmtiles`. The page reads pieces of that file through the app's own small plugin, **AppTiles** (`android/.../AppTilesPlugin.java` and `ios/App/App/AppTilesPlugin.swift`). If the tiles are missing, the app falls back to the online map.
3. **Website changes reach the apps over the air.** On every Netlify deploy, `netlify.toml` runs `web_bundle.py --zip app-bundle`, which publishes:
   - `https://explorelondon.allblacktaxis.co.uk/app-bundle/latest.json`
   - a zip of the website (about 4 MB, without the map tiles)

   A few seconds after the app opens, it checks `latest.json`. If the version is different from its own `bundle.json`, it downloads the zip and switches to it once the app has been closed, or left in the background for 5 minutes. This is done by the `@capgo/capacitor-updater` plugin, self-hosted, with no Capgo account. If a new copy fails to start, the plugin goes back to the previous one by itself.
4. **App-only behaviour lives in `index.html`** and is switched on by `NATIVE`. Inside the app:
   - the map tiles come from the app;
   - sharing uses the phone's share sheet;
   - location comes from the phone;
   - there is no "add to home screen" help.

## What needs a new store build instead of an over-the-air update

- New map tiles
- A new native plugin or permission, such as push notifications or camera
- The app's icon, name or launch screen
- Capacitor upgrades

Website code must not depend on a native plugin that older app builds don't have. Check it with `Capacitor.isPluginAvailable('Name')` first.

## Building (on GitHub, no computer needed)

Go to **Actions** on GitHub, choose a workflow, then **Run workflow**:

- **Android app:** makes a test APK, which appears under **Artifacts** on the finished run. All test builds share `android/test-signing/test.keystore`, so a new one installs over the old one. That key is only for testing. The Play Store needs a separate release key, supplied as GitHub secrets (`ANDROID_KEYSTORE_*`).
- **iPhone app:** builds, signs and uploads to TestFlight. It needs four GitHub secrets, listed at the top of `.github/workflows/ios.yml`.

## Icons and launch screens

These are generated from `branding/`. The sources are in `app/assets/`. To remake them:

```bash
npx capacitor-assets generate --ios --android --iconBackgroundColor '#0F1E3D' --splashBackgroundColor '#0F1E3D'
```
