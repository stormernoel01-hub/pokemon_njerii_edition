#!/usr/bin/env python3
"""Port German translations for src/strings.c from WalterWoshid/pokeemerald-german.

Only replaces a string when the expansion's current text is byte-identical to
WalterWoshid's ENGLISH version for that label (i.e. untranslated vanilla) AND a
German version exists. Anything the user already changed is left alone.
"""
import re, sys, pathlib, urllib.request

EXP = pathlib.Path("/home/denotzgii/pokeemerald-expansion/src/strings.c")
WW_URL = "https://raw.githubusercontent.com/WalterWoshid/pokeemerald-german/master/src/strings.c"

LINE_RE = re.compile(r'^(?P<pre>.*?\bconst u8 (?P<label>gText_\w+)\s*(\[[^\]]*\])?\s*=\s*)_\((?P<body>.*)\)(?P<post>;.*)$')

def parse(text, lo, hi):
    out = {}
    for i, ln in enumerate(text.split("\n")):
        if i < lo or i >= hi:
            continue
        m = LINE_RE.match(ln)
        if m:
            out.setdefault(m.group("label"), m.group("body"))
    return out

def main():
    apply = "--apply" in sys.argv
    ww = urllib.request.urlopen(WW_URL).read().decode("utf-8")
    ww_lines = ww.split("\n")
    ger_start = next(i for i, l in enumerate(ww_lines) if l.strip() == "#elif GERMAN")
    ger_end = next(i for i in range(ger_start + 1, len(ww_lines)) if ww_lines[i].strip() == "#endif")
    ww_en = parse(ww, 0, ger_start)
    ww_de = parse(ww, ger_start, ger_end)
    print(f"WW: {len(ww_en)} english labels, {len(ww_de)} german labels")

    exp = EXP.read_text()
    exp_lines = exp.split("\n")
    replaced, already, no_de, user_modified = [], 0, [], []
    for idx, ln in enumerate(exp_lines):
        m = LINE_RE.match(ln)
        if not m:
            continue
        lbl, body = m.group("label"), m.group("body")
        de = ww_de.get(lbl)
        en = ww_en.get(lbl)
        if de is None:
            no_de.append(lbl); continue
        if body == de:
            already += 1; continue
        if en is not None and body == en:
            exp_lines[idx] = m.group("pre") + "_(" + de + ")" + m.group("post")
            replaced.append(lbl)
        else:
            user_modified.append((lbl, body[:50]))

    print(f"replaced        : {len(replaced)}")
    print(f"already german  : {already}")
    print(f"no german in WW : {len(no_de)}")
    print(f"user-modified / diverged (skipped): {len(user_modified)}")
    if "--verbose" in sys.argv:
        print("\n-- skipped (diverged) --")
        for l, b in user_modified: print(f"  {l}: {b}")
        print("\n-- no german --")
        print("  " + " ".join(no_de))

    if apply:
        EXP.write_text("\n".join(exp_lines))
        print("WROTE", EXP)

if __name__ == "__main__":
    main()
