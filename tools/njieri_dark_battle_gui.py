from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path(".")
BACKUP = ROOT / "backups" / f"njieri_dark_battle_gui_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

FILES_TO_BACKUP = [
    "graphics/battle_interface/textbox.gbapal",
    "graphics/battle_interface/textbox_0.gbapal",
    "graphics/battle_interface/textbox_1.gbapal",

    "graphics/battle_interface/healthbox_doubles_opponent.png",
    "graphics/battle_interface/healthbox_doubles_player.png",
    "graphics/battle_interface/healthbox_doubles_frameend.png",
    "graphics/battle_interface/healthbox_doubles_frameend_bar.png",
    "graphics/battle_interface/healthbox_singles_opponent.png",
    "graphics/battle_interface/healthbox_singles_player.png",
    "graphics/battle_interface/healthbox_safari.png",

    "graphics/battle_interface/hpbar.png",
    "graphics/battle_interface/hpbar_anim.png",
    "graphics/battle_interface/hpbar_anim_unused.png",
]

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def rgb_to_bgr555(rgb):
    r, g, b = rgb
    r5 = clamp(round(r / 8), 0, 31)
    g5 = clamp(round(g / 8), 0, 31)
    b5 = clamp(round(b / 8), 0, 31)
    return r5 | (g5 << 5) | (b5 << 10)

def patch_gbapal(path, patches):
    path = ROOT / path
    data = bytearray(path.read_bytes())

    for index, rgb in patches.items():
        off = index * 2
        if off + 1 >= len(data):
            print(f"skip {path}: index {index} out of range")
            continue
        val = rgb_to_bgr555(rgb)
        data[off:off+2] = val.to_bytes(2, "little")

    path.write_bytes(data)
    print(f"patched palette: {path}")

def is_beige_healthbox_color(r, g, b):
    return (
        r >= 105 and g >= 95 and b >= 55
        and r >= g - 18
        and r <= g + 45
        and g >= b + 8
    )

def darken_beige_to_gray(r, g, b):
    lum = (r * 0.30 + g * 0.59 + b * 0.11)
    shade = clamp(26 + (lum - 105) * 0.20, 28, 74)
    return (shade, shade, shade)

def saturate_hp_green(r, g, b):
    # Keep brightness differences, but make green more vivid.
    if g > 110 and g > r + 35 and g > b + 35:
        new_r = clamp(r * 0.35)
        new_g = clamp(g * 1.25, 0, 248)
        new_b = clamp(b * 0.45)
        return (new_r, new_g, new_b)
    return (r, g, b)

def patch_png_palette(path, mode):
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit(
            "Pillow fehlt. Installier es mit:\n"
            "sudo apt update && sudo apt install python3-pil\n"
        )

    path = ROOT / path
    img = Image.open(path)

    if img.mode != "P":
        print(f"skip {path}: not indexed PNG mode P")
        return

    pal = img.getpalette()
    changed = 0

    for i in range(0, len(pal), 3):
        r, g, b = pal[i], pal[i+1], pal[i+2]
        nr, ng, nb = r, g, b

        if mode == "healthbox":
            if is_beige_healthbox_color(r, g, b):
                nr, ng, nb = darken_beige_to_gray(r, g, b)

        elif mode == "hpbar":
            nr, ng, nb = saturate_hp_green(r, g, b)

        if (nr, ng, nb) != (r, g, b):
            pal[i], pal[i+1], pal[i+2] = nr, ng, nb
            changed += 1

    img.putpalette(pal)
    img.save(path)
    print(f"patched png palette: {path} ({changed} colors changed)")

def backup_files():
    BACKUP.mkdir(parents=True, exist_ok=True)
    for f in FILES_TO_BACKUP:
        src = ROOT / f
        if src.exists():
            dst = BACKUP / f
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    print(f"backup created: {BACKUP}")

backup_files()

# Untere Battle-Textbox:
# index 12/13/14 = Rot-Töne vom Rahmen
# index 15 = Teal/Grün Hintergrund
patch_gbapal("graphics/battle_interface/textbox_0.gbapal", {
    12: (88, 8, 18),
    13: (120, 8, 20),
    14: (64, 8, 18),
    15: (24, 24, 24),
})

# Rechtes Fight/Bag/Pokemon/Run Fenster:
# index 5/7 sind helle Window-Flächen.
patch_gbapal("graphics/battle_interface/textbox_1.gbapal", {
    5: (72, 72, 72),
    7: (52, 52, 52),
})

# Kombinierte Battle-Textbox-Palette, die graphics.c direkt lädt.
patch_gbapal("graphics/battle_interface/textbox.gbapal", {
    # Erste 16 Farben = textbox_0
    12: (88, 8, 18),
    13: (120, 8, 20),
    14: (64, 8, 18),
    15: (24, 24, 24),

    # Zweite 16 Farben = textbox_1
    21: (72, 72, 72),
    23: (52, 52, 52),
})

# Pokémon-Namen/KP-Boxen dunkel machen.
for f in [
    "graphics/battle_interface/healthbox_doubles_opponent.png",
    "graphics/battle_interface/healthbox_doubles_player.png",
    "graphics/battle_interface/healthbox_doubles_frameend.png",
    "graphics/battle_interface/healthbox_doubles_frameend_bar.png",
    "graphics/battle_interface/healthbox_singles_opponent.png",
    "graphics/battle_interface/healthbox_singles_player.png",
    "graphics/battle_interface/healthbox_safari.png",
]:
    patch_png_palette(f, "healthbox")

# HP-Balken-Grün sättigen.
for f in [
    "graphics/battle_interface/hpbar.png",
    "graphics/battle_interface/hpbar_anim.png",
    "graphics/battle_interface/hpbar_anim_unused.png",
]:
    patch_png_palette(f, "hpbar")

# Weisse Schrift auf den (dunkelgrauen) Namens-/KP-Boxen.
# sHealthBoxTextColor in src/battle_interface.c nutzt foreground=1, shadow=3.
def whiten_healthbox_text(path):
    from PIL import Image
    p = ROOT / path
    im = Image.open(p)
    if im.mode != "P":
        print(f"skip {p}: not mode P"); return
    pal = im.getpalette()
    pal[1*3:1*3+3] = [248, 248, 248]   # foreground -> weiss
    pal[3*3:3*3+3] = [24, 24, 24]      # shadow -> fast schwarz
    im.putpalette(pal)
    im.save(p)
    print(f"whitened healthbox text: {p}")

for f in [
    "graphics/battle_interface/healthbox_singles_player.png",
    "graphics/battle_interface/healthbox_singles_opponent.png",
    "graphics/battle_interface/healthbox_doubles_player.png",
    "graphics/battle_interface/healthbox_doubles_opponent.png",
    "graphics/battle_interface/healthbox_doubles_frameend.png",
    "graphics/battle_interface/healthbox_doubles_frameend_bar.png",
    "graphics/battle_interface/healthbox_safari.png",
]:
    whiten_healthbox_text(f)

print("done")
