#!/usr/bin/env python3
"""Wire one DPPt/HGSS song from CyanSMP64/pokeemerald `dppt_hgss_music` into the
build.  The instrument foundation must already be present (run
ds_music_foundation.py once first).

Usage:
    python3 tools/njieri/add_ds_song.py <mid_basename> [CONSTANT_NAME]

    <mid_basename>   e.g.  mus_dp_route209_day   (no .mid)
    CONSTANT_NAME    e.g.  MUS_DP_ROUTE209_DAY   (default: upper(basename))

Does three things:
  1. copies sound/songs/midi/<basename>.mid  from cyan/dppt_hgss_music
  2. adds the midi.cfg line (mid2agb flags copied verbatim from dppt songs.mk)
  3. appends the `song` entry to sound/song_table.inc and the numeric
     `#define` to include/constants/songs.h  (next free id)

Idempotent: re-running for the same song is a no-op.
"""
import os, re, subprocess, sys

BRANCH = "cyan/dppt_hgss_music"


def sh(*a):
    return subprocess.run(a, capture_output=True)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    base = sys.argv[1].removesuffix(".mid")
    const = sys.argv[2] if len(sys.argv) > 2 else base.upper()
    if not os.path.isfile("sound/song_table.inc"):
        sys.exit("run from repo root")

    # --- flags from dppt songs.mk ---
    smk = sh("git", "show", f"{BRANCH}:songs.mk").stdout.decode()
    m = re.search(rf"{re.escape(base)}\.s:.*?\n\s*\$\(MID\)\s+\$<\s+\$@\s+(.*)", smk)
    if not m:
        sys.exit(f"no songs.mk entry for {base} on {BRANCH}")
    flags = m.group(1).strip()

    # --- 1. copy .mid ---
    dst = f"sound/songs/midi/{base}.mid"
    if not os.path.exists(dst):
        data = sh("git", "show", f"{BRANCH}:{dst}").stdout
        if not data:
            sys.exit(f"{dst} not found on {BRANCH}")
        with open(dst, "wb") as f:
            f.write(data)
        print(f"copied {dst}")
    else:
        print(f"{dst} already present")

    # --- 2. midi.cfg ---
    cfg_path = "sound/songs/midi/midi.cfg"
    cfg = open(cfg_path).read()
    if f"{base}.mid:" not in cfg:
        with open(cfg_path, "a") as f:
            if not cfg.endswith("\n"):
                f.write("\n")
            f.write(f"{base}.mid: {flags}\n")
        print(f"midi.cfg += {base}.mid: {flags}")
    else:
        print("midi.cfg entry already present")

    # --- 3. song_table.inc + songs.h ---
    st = open("sound/song_table.inc").read()
    if re.search(rf"^\s*song {re.escape(base)},", st, re.M):
        print("song_table entry already present")
    else:
        n = len(re.findall(r"^\s*song ", st, re.M))  # next free id
        st = st.replace("\n\t.align 2\ndummy_song_header:",
                        f"\tsong {base}, MUSIC_PLAYER_BGM, 0\n\n\t.align 2\ndummy_song_header:", 1)
        open("sound/song_table.inc", "w").write(st)

        sh_h = "include/constants/songs.h"
        h = open(sh_h).read()
        if f"#define {const} " not in h and f"#define {const}\t" not in h:
            h = h.replace("#define MUS_ROUTE118",
                          f"#define {const:<26} {n}\n#define MUS_ROUTE118", 1)
            open(sh_h, "w").write(h)
        print(f"song id {n}  ->  {const}")

    print("\nDone. Assign it on a map (music field) or via playbgm, then build.")


if __name__ == "__main__":
    main()
