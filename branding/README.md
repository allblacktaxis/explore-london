# Explore London – app artwork

`source-skyline.webp` is the master artwork and `abt-logo.png` the All Black Taxis badge (placed top-centre on the icon and launch screens; not used on the favicon). `make_assets.py` builds everything from it:

    python3 branding/make_assets.py

| Output | Used for |
|---|---|
| `img/abt-logo.png` | Logo in the app header (a 480px copy of `abt-logo.png`) |
| `icons/icon-192.png`, `icon-512.png`, `maskable-*.png`, `apple-touch-icon-180.png` | PWA / home-screen icon (with "Explore London") |
| `favicon.ico`, `icons/favicon-16/32/48.png` | Website favicon (Big Ben clock, no text) |
| `icons/splash/apple-splash-*.jpg` | iOS home-screen launch images (links in `index.html`) |
| `icons/splash/launch-*.jpg` | In-app launch screen shown when opened as an installed app (Android shows this after its own icon splash) |
| `branding/icon-1024.png`, `icon-maskable-1024.png` | Masters for the future App Store / Play Store icons |
| `branding/splash-portrait-1290x2796.png`, `splash-landscape-2732x2048.png` | Masters for the future native launch screens |

The source is 1170×779 px, so the larger images are upscaled. A higher-resolution
original (3000 px wide or more) dropped in as `source-skyline.webp` and re-running the
script will sharpen everything.
