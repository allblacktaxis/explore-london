"""Builds the Explore London app icons, favicons and launch (splash) images
from branding/source-skyline.webp.  Run from the repo root:

    python3 branding/make_assets.py

Needs Pillow.  Writes into icons/ (PWA) and branding/ (masters for the
future iOS / Android apps).
"""
import sys, os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'branding/source-skyline.webp')
FONT = os.path.join(ROOT, 'branding/Archivo-800.ttf')
LOGO = Image.open(os.path.join(ROOT, 'branding/abt-logo.png')).convert('RGBA')  # All Black Taxis badge
NAVY = (15, 30, 61); ORANGE = (242, 140, 56); WHITE = (255, 255, 255)
_s = Image.open(SRC).convert('RGBA')
SKYC = (93, 189, 246)
src = Image.new('RGB', _s.size, SKYC); src.paste(_s, (0, 0), _s)  # top of artwork fades to transparent
SW, SH = src.size  # 1170 x 779
WATER = 640        # y where the river starts in the source

def font(px): return ImageFont.truetype(FONT, int(px))

def vfade(w, h, top_alpha, bottom_alpha):
    m = Image.new('L', (1, h))
    for y in range(h):
        t = y / max(1, h - 1); t = t * t * (3 - 2 * t)
        m.putpixel((0, y), int(top_alpha + (bottom_alpha - top_alpha) * t))
    return m.resize((w, h))

def text_center(d, cx, y, s, f, fill, track=0.0):
    # draw text with letter spacing (track = fraction of font size), top of caps at y
    size = f.size; sp = track * size
    widths = [d.textlength(ch, font=f) for ch in s]
    total = sum(widths) + sp * (len(s) - 1)
    x = cx - total / 2
    asc = f.getbbox('E')[1]
    for ch, w in zip(s, widths):
        d.text((x, y - asc), ch, font=f, fill=fill); x += w + sp
    return total

def lockup(img, cx, top, scale):
    """EXPLORE (orange, small, tracked) over LONDON (white, big)."""
    d = ImageDraw.Draw(img)
    f2 = font(scale * 1.0); capL = f2.getbbox('L')[3] - f2.getbbox('L')[1]
    f1 = font(scale * 0.52); capE = f1.getbbox('E')[3] - f1.getbbox('E')[1]
    text_center(d, cx, top, 'EXPLORE', f1, ORANGE, track=0.30)
    text_center(d, cx, top + capE + scale * 0.22, 'LONDON', f2, WHITE, track=0.06)
    return top + capE + scale * 0.22 + capL

def lockup_height(scale):
    f2 = font(scale); f1 = font(scale * 0.52)
    return (f1.getbbox('E')[3] - f1.getbbox('E')[1]) + scale * 0.22 + (f2.getbbox('L')[3] - f2.getbbox('L')[1])

def lockup_width(scale):
    d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    f2 = font(scale); return sum(d.textlength(c, font=f2) for c in 'LONDON') + 0.06 * scale * 5

# ---------- shared helpers ----------
SKYTOP = (52, 150, 228)

def padded(pad):
    """The artwork with `pad` rows of sky added above it (room for the logo)."""
    im = Image.new('RGB', (SW, SH + pad), SKYC)
    im.paste(Image.new('RGB', (SW, pad), SKYTOP), (0, 0), vfade(SW, pad, 255, 0))
    im.paste(src, (0, pad))
    return im

def put_logo(img, cx, top, width):
    lg = LOGO.resize((int(width), int(width * LOGO.height / LOGO.width)), Image.LANCZOS)
    img.paste(lg, (int(cx - lg.width / 2), int(top)), lg)
    return top + lg.height

def logo_h(width): return width * LOGO.height / LOGO.width

# ---------- app icon ----------
def icon(S, maskable=False):
    """Logo top-centre, full skyline, EXPLORE LONDON on navy at the bottom."""
    img = Image.new('RGB', (S, S), NAVY)
    lw = S * (0.60 if not maskable else 0.40)
    ltop = S * (0.05 if not maskable else 0.15)
    lbot = ltop + logo_h(lw)
    sc = S / SW                                        # whole skyline, full width
    pad = int(max(0, (lbot + S * 0.025) / sc - 40))    # Big Ben's tip sits just under the logo
    full = padded(pad)
    ih = int(full.height * sc)
    im = full.resize((S, ih), Image.LANCZOS)
    fade_h = int(S * 0.16)
    mask = Image.new('L', im.size, 255)
    mask.paste(vfade(S, fade_h, 255, 0), (0, ih - fade_h))
    img.paste(im, (0, 0), mask)
    band_top = int(S * (0.70 if not maskable else 0.56))
    shade = Image.new('RGB', (S, S - band_top), NAVY)
    img.paste(shade, (0, band_top), vfade(S, S - band_top, 0, 255).point(lambda a: min(255, int(a * 1.6))))
    put_logo(img, S / 2, ltop, lw)
    if not maskable:
        scale = S * 0.165
        lockup(img, S / 2, S * 0.955 - lockup_height(scale), scale)
    else:
        scale = S * 0.118  # stays inside the 80% safe circle
        lockup(img, S / 2, S * 0.795 - lockup_height(scale), scale)
    return img

# ---------- favicon (no text) ----------
def favicon(S):
    # tight crop on Big Ben's clock face and spire against the sky
    box = (553, 216, 637, 300)
    return src.crop(box).resize((S, S), Image.LANCZOS)

# ---------- launch / splash ----------
MAX_UPSCALE = 1.3   # the artwork is 1170px wide; enlarging it more than this looks soft

def splash(W, H):
    img = Image.new('RGB', (W, H), NAVY)
    tall = H / W > 1.8
    if W >= H or W / SW * (1.12 if tall else 1.0) > MAX_UPSCALE:
        return splash_card(W, H)          # iPads, desktops: keep the skyline sharp
    # portrait: logo in the sky, skyline in the middle, river fading to navy with title
    tall = H / W > 1.8                       # phones; iPads are squarer
    sc = W / SW * (1.12 if tall else 1.0)    # a touch of zoom so the skyline fills phone width
    iw, ih = int(SW * sc), int(SH * sc)
    im = src.resize((iw, ih), Image.LANCZOS).crop(((iw - W) // 2, 0, (iw - W) // 2 + W, ih))
    scale = W * 0.15
    group = ih + H * 0.035 + lockup_height(scale)
    top = int((H - group) * 0.56)
    sky = Image.new('RGB', (W, top + 2), SKYC)
    sky.paste(Image.new('RGB', (W, top + 2), SKYTOP), (0, 0), vfade(W, top + 2, 255, 0))
    img.paste(sky, (0, 0))
    mask = Image.new('L', im.size, 255)
    fade_h = int((SH - WATER) * sc * 0.9)
    mask.paste(vfade(W, fade_h, 255, 0), (0, ih - fade_h))
    img.paste(im, (0, top), mask)
    lockup(img, W / 2, top + ih + H * 0.035, scale)
    lw = W * (0.62 if tall else 0.48)
    put_logo(img, W / 2, max(H * 0.05, (top + 30 * sc) / 2 - logo_h(lw) / 2), lw)
    return img

def splash_card(W, H):
    """Large screens: logo, the skyline as a rounded picture at (near) its real size, title; all on navy."""
    sc = min(MAX_UPSCALE, W * 0.88 / SW)
    while True:
        cw, ch = int(SW * sc), int(SH * sc)
        lw = min(cw * 0.46, W * 0.5); lh = logo_h(lw)
        scale = cw * 0.105; th = lockup_height(scale)
        gap = max(H * 0.035, ch * 0.06)
        group = lh + gap + ch + gap * 1.2 + th
        if group <= H * 0.88 or sc < 0.3: break
        sc *= 0.97
    img = Image.new('RGB', (W, H), NAVY)
    y = (H - group) / 2
    put_logo(img, W / 2, y, lw); y += lh + gap
    pic = src.resize((cw, ch), Image.LANCZOS)
    m = Image.new('L', (cw * 4, ch * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, cw * 4 - 1, ch * 4 - 1), radius=int(cw * 0.035 * 4), fill=255)
    img.paste(pic, (int((W - cw) / 2), int(y)), m.resize((cw, ch), Image.LANCZOS)); y += ch + gap * 1.2
    lockup(img, W / 2, y, scale)
    return img

V = 4   # bump when the artwork changes so phones fetch the new files

# iOS launch screens: (CSS width, CSS height, pixel ratio, devices)
IOS = [
    (440, 956, 3, 'iPhone 16 Pro Max'), (402, 874, 3, 'iPhone 16 Pro'),
    (430, 932, 3, 'iPhone 14 Pro Max / 15 Plus / 15 Pro Max / 16 Plus'),
    (393, 852, 3, 'iPhone 14 Pro / 15 / 15 Pro / 16'),
    (428, 926, 3, 'iPhone 12/13 Pro Max / 14 Plus'), (390, 844, 3, 'iPhone 12/13/14'),
    (375, 812, 3, 'iPhone X/XS/11 Pro/12 mini/13 mini'), (414, 896, 3, 'iPhone XS Max / 11 Pro Max'),
    (414, 896, 2, 'iPhone XR / 11'), (414, 736, 3, 'iPhone 8 Plus'),
    (375, 667, 2, 'iPhone 8 / SE 2nd & 3rd gen'), (320, 568, 2, 'iPhone SE 1st gen'),
    (1032, 1376, 2, 'iPad Pro 13" (M4)'), (1024, 1366, 2, 'iPad Pro 12.9"'),
    (834, 1210, 2, 'iPad Pro 11" (M4)'), (834, 1194, 2, 'iPad Pro 11"'),
    (820, 1180, 2, 'iPad Air 10.9" / iPad 10th gen'), (834, 1112, 2, 'iPad Air 10.5"'),
    (810, 1080, 2, 'iPad 10.2"'), (768, 1024, 2, 'iPad 9.7" / iPad mini 5'),
    (744, 1133, 2, 'iPad mini 6'),
]

def main():
    I = os.path.join(ROOT, 'icons'); B = os.path.join(ROOT, 'branding')
    os.makedirs(os.path.join(I, 'splash'), exist_ok=True)
    master = icon(1024)
    master.save(os.path.join(B, 'icon-1024.png'))                    # iOS App Store / Android master
    for n in (512, 192):
        master.resize((n, n), Image.LANCZOS).save(os.path.join(I, f'icon-{n}.png'), optimize=True)
    master.resize((180, 180), Image.LANCZOS).save(os.path.join(I, 'apple-touch-icon-180.png'), optimize=True)
    mask = icon(1024, maskable=True)
    mask.save(os.path.join(B, 'icon-maskable-1024.png'))
    for n in (512, 192):
        mask.resize((n, n), Image.LANCZOS).save(os.path.join(I, f'maskable-{n}.png'), optimize=True)
    for n in (16, 32, 48):
        favicon(n).save(os.path.join(I, f'favicon-{n}.png'), optimize=True)
    favicon(48).save(os.path.join(ROOT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    # native splash masters for the future iOS / Android apps
    splash(1290, 2796).save(os.path.join(B, 'splash-portrait-1290x2796.png'), optimize=True)
    splash(2732, 2048).save(os.path.join(B, 'splash-landscape-2732x2048.png'), optimize=True)
    # in-app launch screen
    splash(1290, 2796).save(os.path.join(I, 'splash', 'launch-portrait.jpg'), quality=86, optimize=True, progressive=True)
    splash(2880, 1800).save(os.path.join(I, 'splash', 'launch-landscape.jpg'), quality=86, optimize=True, progressive=True)
    # iOS startup images + the <link> tags for index.html
    tags, srcs = [], []
    for w, h, r, name in IOS:
        for orient, (pw, ph) in (('portrait', (w * r, h * r)), ('landscape', (h * r, w * r))):
            if orient == 'landscape' and w < 700:
                continue  # iPhone home-screen apps launch in portrait
            fn = f'apple-splash-{pw}x{ph}.jpg'
            splash(pw, ph).save(os.path.join(I, 'splash', fn), quality=84, optimize=True, progressive=True)
            mq = f'(device-width: {w}px) and (device-height: {h}px) and (-webkit-device-pixel-ratio: {r}) and (orientation: {orient})'
            tags.append(f'<link rel="apple-touch-startup-image" href="icons/splash/{fn}?v={V}" media="{mq}">')
            srcs.append(f'<source media="{mq}" srcset="icons/splash/{fn}?v={V}">')
    # the in-app launch screen shows the exact same picture as iOS, then falls back
    srcs.append(f'<source media="(orientation: landscape)" srcset="icons/splash/launch-landscape.jpg?v={V}">')
    html = os.path.join(ROOT, 'index.html'); t = open(html).read()
    for name, body in (('launch-images', tags), ('launch-sources', srcs)):
        t = re.sub(f'(<!-- {name}:start -->\\n).*?(<!-- {name}:end -->)', lambda m: m.group(1) + '\n'.join(body) + '\n' + m.group(2), t, flags=re.S)
    open(html, 'w').write(t)
    print(len(tags), 'iOS launch images')

if __name__ == '__main__':
    main()
