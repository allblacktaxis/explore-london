#!/usr/bin/env python3
"""Pack the Explore London website for the iPhone / Android apps.

The apps carry their own copy of the website, so they open instantly and work offline,
and they fetch a newer copy over the air whenever the website changes.

  python3 app/scripts/web_bundle.py --www app/www
      copies the website into app/www (the copy built into the app). Run before `npx cap sync`.

  python3 app/scripts/web_bundle.py --zip app-bundle
      makes app-bundle/web-<version>.zip and app-bundle/latest.json, which the apps check
      for updates. Netlify runs this on every deploy (see netlify.toml).

Both write bundle.json ({"version": ...}) into the copy, so the app knows which version it has.
The version is a fingerprint of the files, so the same website always gets the same version.
The map tiles are NOT in the over-the-air copy: they are built into the app itself
(tiles/map.pmtiles, read by the app's AppTiles plugin).
"""
import argparse, hashlib, json, os, shutil, sys, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = 'https://explorelondon.allblacktaxis.co.uk'

# top-level files and folders that are not part of the website
SKIP_TOP = {'app', 'app-bundle', 'branding', 'tiles', 'netlify.toml', 'CLAUDE.md', 'README.md', 'Claude outputs', 'node_modules'}


def website_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir == '.':
            dirnames[:] = [d for d in dirnames if d not in SKIP_TOP and not d.startswith('.')]
        else:
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for f in filenames:
            rel = os.path.normpath(os.path.join(rel_dir, f)).replace(os.sep, '/')
            if f.startswith('.') or (rel_dir == '.' and f in SKIP_TOP):
                continue
            if f.endswith(('.py', '.md', '.pmtiles')):
                continue
            # iPhone "add to home screen" launch pictures: not needed inside the app (the in-app launch-*.jpg are kept)
            if rel.startswith('icons/splash/apple-splash-'):
                continue
            out.append(rel)
    return sorted(out)


def fingerprint(files):
    h = hashlib.sha256()
    for rel in files:
        h.update(rel.encode() + b'\0')
        with open(os.path.join(ROOT, rel), 'rb') as fh:
            h.update(hashlib.sha256(fh.read()).digest())
    return h.hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--www', help='copy the website into this folder (built into the app)')
    ap.add_argument('--zip', help='write the over-the-air update zip and latest.json into this folder')
    a = ap.parse_args()
    if not a.www and not a.zip:
        ap.error('give --www and/or --zip')
    files = website_files()
    if 'index.html' not in files:
        sys.exit('index.html not found - run from the website repository')
    version = fingerprint(files)
    meta = json.dumps({'version': version}).encode()

    if a.www:
        www = os.path.abspath(a.www)
        tiles = os.path.join(www, 'tiles')
        # keep the (large) map tiles if they are already there; replace everything else
        if os.path.isdir(www):
            for name in os.listdir(www):
                if name != 'tiles':
                    p = os.path.join(www, name)
                    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        os.makedirs(www, exist_ok=True)
        for rel in files:
            dst = os.path.join(www, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(ROOT, rel), dst)
        with open(os.path.join(www, 'bundle.json'), 'wb') as fh:
            fh.write(meta)
        if not os.path.isfile(os.path.join(tiles, 'map.pmtiles')):
            print('NOTE: no map tiles at', os.path.join(tiles, 'map.pmtiles'), '- the app will use the online map')
        print(f'website {version}: {len(files)} files copied to {www}')

    if a.zip:
        out = os.path.abspath(a.zip)
        os.makedirs(out, exist_ok=True)
        name = f'web-{version}.zip'
        with zipfile.ZipFile(os.path.join(out, name), 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for rel in files:
                z.write(os.path.join(ROOT, rel), rel)
            z.writestr('bundle.json', meta)
        with open(os.path.join(out, 'latest.json'), 'w') as fh:
            json.dump({'version': version, 'url': f'{SITE}/app-bundle/{name}'}, fh)
        size = os.path.getsize(os.path.join(out, name)) / 1e6
        print(f'website {version}: {name} ({size:.1f} MB) and latest.json written to {out}')


if __name__ == '__main__':
    main()
