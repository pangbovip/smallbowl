# Builds the responsive image set the pages use. Run after adding or replacing a photo in images/:
#   python make_responsive_images.py
# Hero: portrait 4:5 for desktop, wide 3:2 crop for phones. Cards: 3:2. Each size as AVIF plus a JPEG fallback.
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")
WALL = ["wall-panda", "wall-bund", "wall-xlb", "wall-bike"]   # hero photo wall, 3:2
CARDS = ["douzhi", "xlb", "bike", "pay", "metro", "hotpot", "water", "toilet",
         "roujiamo", "hsr", "didi", "duck", "jianbing", "gaiwan"]
AVIF_Q = 58
JPEG_Q = 80

def crop_ratio(im, rw, rh, focus_y=0.5):
    w, h = im.size; t = rw / rh
    if w / h > t:
        nw = int(h * t); x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w / t); y = int((h - nh) * focus_y)
    return im.crop((0, y, w, y + nh))

def emit(im, stem, widths, jpeg_width):
    out = []
    for w in widths:
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        p = os.path.join(IMG, "%s-%d.avif" % (stem, w))
        r.save(p, "AVIF", quality=AVIF_Q, speed=4)
        out.append((os.path.basename(p), os.path.getsize(p)))
        if w == jpeg_width:
            pj = os.path.join(IMG, "%s-%d.jpg" % (stem, w))
            r.save(pj, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
            out.append((os.path.basename(pj), os.path.getsize(pj)))
    return out

if __name__ == "__main__":
    report = []
    hero = Image.open(os.path.join(IMG, "tiantan.jpg")).convert("RGB")      # 1400x1750, 4:5
    report += emit(hero, "tiantan", [560, 840, 1120], 840)
    wide = crop_ratio(hero, 3, 2, focus_y=0.30)                              # matches object-position 50% 30%
    report += emit(wide, "tiantan-wide", [480, 800, 1200], 800)
    for wid in WALL:
        im = Image.open(os.path.join(IMG, wid + ".jpg")).convert("RGB")
        report += emit(crop_ratio(im, 3, 2), wid, [320, 560], 560)
    for cid in CARDS:
        im = Image.open(os.path.join(IMG, cid + ".jpg")).convert("RGB")      # 1200x800, 3:2
        report += emit(im, cid, [400, 800], 800)
    total = sum(s for _, s in report)
    for name, size in report:
        print("%-26s %5d KB" % (name, size // 1024))
    print("files:", len(report), "| total KB:", total // 1024)
