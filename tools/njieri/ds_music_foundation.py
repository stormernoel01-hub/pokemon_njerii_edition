#!/usr/bin/env python3
"""One-shot: import the DPPt/HGSS instrument foundation (voicegroup191 + voicegroup229
trees, their samples, keysplit tables, direct_sound_data entries) from
CyanSMP64/pokeemerald branch `dppt_hgss_music` into this pokeemerald-expansion tree.

After this runs once and the tree builds, individual DS songs can be added with
add_ds_song.py -- each song is then just a .mid + 3 wiring lines.

Run from repo root:  python3 tools/njieri/ds_music_foundation.py
Requires:  git remote `cyan` with `cyan/dppt_hgss_music` fetched.
"""
import os, re, subprocess, sys

BRANCH = "cyan/dppt_hgss_music"
ROOTS = ["191", "229"]  # DPPt main, HGSS main


def git_show(path):
    return subprocess.run(["git", "show", f"{BRANCH}:{path}"],
                          capture_output=True).stdout


def git_text(path):
    return git_show(path).decode("utf-8", "replace")


def main():
    if not os.path.isfile("sound/voice_groups.inc"):
        sys.exit("run from repo root")

    # --- 1. transitive closure of voicegroups from the two roots ---
    vg_seen, stack = set(), list(ROOTS)
    vg_text = {}
    while stack:
        n = stack.pop()
        if n in vg_seen:
            continue
        vg_seen.add(n)
        t = git_text(f"sound/voicegroups/voicegroup{n}.inc")
        vg_text[n] = t
        for sub in re.findall(r"\bvoicegroup(\d+)\b", t):
            if sub not in vg_seen:
                stack.append(sub)
    print(f"voicegroups in closure: {len(vg_seen)}")

    # samples + keysplit tables referenced anywhere in the closure
    samples, kstabs = set(), set()
    for t in vg_text.values():
        samples.update(re.findall(r"DirectSoundWaveData_(\w+)", t))
        kstabs.update(re.findall(r"\b(KeySplitTable\d+)\b", t))
    print(f"samples referenced: {len(samples)}   keysplit tables: {len(kstabs)}")

    # --- 2. copy voicegroup files ---
    for n in sorted(vg_seen, key=int):
        dst = f"sound/voicegroups/voicegroup{n}.inc"
        if os.path.exists(dst):
            continue
        with open(dst, "wb") as f:
            f.write(git_show(f"sound/voicegroups/voicegroup{n}.inc"))

    # --- 3. append includes to voice_groups.inc ---
    with open("sound/voice_groups.inc", "r") as f:
        vgi = f.read()
    add = [f'.include "sound/voicegroups/voicegroup{n}.inc"\n'
           for n in sorted(vg_seen, key=int)
           if f"voicegroups/voicegroup{n}.inc" not in vgi]
    if add:
        with open("sound/voice_groups.inc", "a") as f:
            f.write("\n@ --- DPPt/HGSS music foundation ---\n")
            f.writelines(add)
    print(f"added {len(add)} voice_groups.inc includes")

    # --- 4. copy sample .aif files ---
    src_dsd = git_text("sound/direct_sound_data.inc")
    # map symbol -> incbin path from the source direct_sound_data.inc
    sym_path = {}
    cur = None
    for line in src_dsd.splitlines():
        m = re.match(r"\s*DirectSoundWaveData_(\w+)::", line)
        if m:
            cur = m.group(1)
        m = re.search(r'\.incbin "([^"]+)"', line)
        if m and cur:
            sym_path[cur] = m.group(1)
            cur = None

    copied = 0
    missing = []
    for s in sorted(samples):
        p = sym_path.get(s)
        if not p:
            missing.append(s)
            continue
        aif = p[:-4] + ".aif" if p.endswith(".bin") else p
        dst = aif
        if os.path.exists(dst):
            continue
        data = git_show(aif)
        if not data:
            missing.append(s)
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(data)
        copied += 1
    print(f"copied {copied} sample .aif files; missing: {len(missing)} {missing[:8]}")

    # --- 5. append direct_sound_data.inc entries ---
    with open("sound/direct_sound_data.inc", "r") as f:
        dsd = f.read()
    blocks = []
    # re-split source into per-symbol blocks
    for m in re.finditer(
            r"(\s*\.align 2\s*\n)?\s*DirectSoundWaveData_(\w+)::\s*\n\s*\.incbin \"([^\"]+)\"\s*\n",
            src_dsd):
        sym, path = m.group(2), m.group(3)
        if sym not in samples:
            continue
        if f"DirectSoundWaveData_{sym}::" in dsd:
            continue
        aifpath = path[:-4] + ".aif" if path.endswith(".bin") else path
        blocks.append(f"\n\t.align 2\nDirectSoundWaveData_{sym}::\n\t.incbin \"{aifpath}\"\n")
    if blocks:
        with open("sound/direct_sound_data.inc", "a") as f:
            f.write("\n@ --- DPPt/HGSS music foundation ---\n")
            f.writelines(blocks)
    print(f"added {len(blocks)} direct_sound_data.inc entries")

    # --- 6. append keysplit tables ---
    src_ks = git_text("sound/keysplit_tables.inc")
    with open("sound/keysplit_tables.inc", "r") as f:
        ks = f.read()
    # each table:  .set KeySplitTableN, . - NN  ...  up to next .set or EOF
    parts = re.split(r"(?=^\.set KeySplitTable\d+,)", src_ks, flags=re.M)
    add_ks = []
    for part in parts:
        m = re.match(r"\.set (KeySplitTable\d+),", part)
        if not m:
            continue
        if m.group(1) in kstabs and f".set {m.group(1)}," not in ks:
            add_ks.append(part.rstrip() + "\n")
    if add_ks:
        with open("sound/keysplit_tables.inc", "a") as f:
            f.write("\n@ --- DPPt/HGSS music foundation ---\n")
            f.write("\n".join(add_ks))
    print(f"added {len(add_ks)} keysplit tables")

    print("\nDone. Next: wire the aif2pcm tool (see ds_music_setup notes) then build.")


if __name__ == "__main__":
    main()
