#!/usr/bin/env python3
"""Port German MOVE descriptions from WalterWoshid into moves_info.h.
Match by MOVE_ constant + normalized English text (ignoring line breaks).
"""
import re, sys, urllib.request, pathlib

RAW = "https://raw.githubusercontent.com/WalterWoshid/pokeemerald-german/master/"
ROOT = pathlib.Path("/home/denotzgii/pokeemerald-expansion")

def fetch(rel):
    return urllib.request.urlopen(RAW + rel).read().decode("utf-8")

def norm(s):
    s = re.sub(r'\\[np]', ' ', s)          # \n \p -> space
    s = re.sub(r'\{[^}]*\}', '', s)         # drop {TOKENS}
    s = re.sub(r'[^A-Za-z0-9]', '', s).upper()
    return s

# WW: static const u8 sXDescription[] = _(  "..."  "..."  );
SYM_RE = re.compile(r'static const u8 (\w+)\[\]\s*=\s*_\(\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)\s*;', re.S)
def parse_syms(text):
    out = {}
    for m in SYM_RE.finditer(text):
        parts = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2))
        out[m.group(1)] = "".join(parts)
    return out

def main():
    apply = "--apply" in sys.argv
    ww = fetch("src/data/text/move_descriptions.h")
    gi = ww.index("#elif GERMAN"); ei = ww.index("#endif", gi)
    en_syms = parse_syms(ww[:gi])
    de_syms = parse_syms(ww[gi:ei])
    # pointer array: [MOVE_X - 1] = sXDescription,
    ptr = dict(re.findall(r'\[(MOVE_[A-Z0-9_]+)\s*-\s*1\]\s*=\s*(\w+)\s*,', ww[ei:]))
    move_en = {k: en_syms[v] for k, v in ptr.items() if v in en_syms}
    move_de = {k: de_syms[v] for k, v in ptr.items() if v in de_syms}
    print(f"WW: {len(move_en)} en / {len(move_de)} de move descriptions")

    p = ROOT / "src/data/moves_info.h"
    txt = p.read_text()
    # [MOVE_X] = { ... .description = COMPOUND_STRING( "..." "..." ),
    blk = re.compile(
        r'(\[(?P<k>MOVE_[A-Z0-9_]+)\]\s*=\s*\{.*?\.description = COMPOUND_STRING\(\s*)'
        r'(?P<body>(?:"(?:[^"\\]|\\.)*"\s*)+)(\))', re.S)
    stats = {'repl':0,'already':0,'nowd':0,'div':0}
    out=[]; last=0
    for m in blk.finditer(txt):
        k = m.group('k'); body = m.group('body')
        cur = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', body))
        d = move_de.get(k); e = move_en.get(k)
        if d is None: stats['nowd']+=1; continue
        if norm(cur) == norm(d): stats['already']+=1; continue
        if e is not None and norm(cur) == norm(e):
            new = '"%s"' % d
            out.append(txt[last:m.start('body')]); out.append(new + "\n            ")
            last = m.end('body')
            stats['repl']+=1
        else:
            stats['div']+=1
    out.append(txt[last:])
    print("move descriptions:", stats)
    if apply:
        p.write_text("".join(out))
        print("wrote", p)

if __name__ == "__main__":
    main()
