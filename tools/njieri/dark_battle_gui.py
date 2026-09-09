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
