#!/usr/bin/env python3
"""Njeri: dark-grey battle healthboxes ("name boxes") with white text.

The healthbox sprite tiles use palette *indices*; the actual colours come from
graphics/battle_interface/ball_status_bar.png at runtime
(battle_gfx_sfx_util.c: gBattleInterface_BallStatusBarPal -> TAG_HEALTHBOX_PAL).
The HP bar uses ball_display.png (-> TAG_HEALTHBAR_PAL).

sHealthBoxTextColor in src/battle_interface.c uses foreground=1, shadow=3.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(".")

def patch(rel, changes):
    p = ROOT / rel
    im = Image.open(p)
    assert im.mode == "P", f"{p} not indexed"
    pal = im.getpalette()
    for i, rgb in changes.items():
        pal[i*3:i*3+3] = list(rgb)
    im.putpalette(pal)
    im.save(p)
    print(f"patched {p}: {sorted(changes)}")

# name box: 1 = border + text fg, 2 = fill, 3 = text shadow / shade, 4 = edge
patch("graphics/battle_interface/ball_status_bar.png", {
    1: (248, 248, 248),   # white
    2: (64, 64, 64),      # dark grey fill
    3: (32, 32, 32),      # near-black
    4: (48, 48, 48),      # dark grey
})

# HP bar: darken the beige track (keep the green/yellow/red fill + white "HP")
patch("graphics/battle_interface/ball_display.png", {
    3: (40, 40, 40),
})

print("done")

# --- battle textbox frame: saturated red instead of the vanilla blue/grey ---
# real sources are the JASC .pal files; textbox.gbapal = textbox_0 + textbox_1
def write_jasc(path, colors):
    lines = ["JASC-PAL", "0100", str(len(colors))] + [f"{r} {g} {b}" for r, g, b in colors]
    (ROOT / path).write_text("\r\n".join(lines) + "\r\n")

write_jasc("graphics/battle_interface/textbox_0.pal", [
    (0,0,0),(255,255,255),(255,56,56),(176,32,40),(224,64,72),(255,255,255),
    (176,52,60),(255,150,140),(140,24,32),(96,16,24),(168,48,56),(150,36,48),
    (224,80,72),(248,88,72),(208,64,72),(56,16,20),
])
write_jasc("graphics/battle_interface/textbox_1.pal", [
    (0,0,0),(140,28,36),(176,32,40),(224,64,72),(40,12,16),(255,255,255),
    (176,52,60),(255,150,140),(120,32,36),(232,128,128),(216,56,64),(150,36,48),
    (0,0,0),(0,0,0),(0,0,0),(0,0,0),
])
print("textbox frame -> red")
