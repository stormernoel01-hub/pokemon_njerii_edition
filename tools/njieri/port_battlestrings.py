#!/usr/bin/env python3
"""Port German gBattleStringsTable entries (STRINGID_*) from WalterWoshid.
WW: sText_X symbols in #if ENGLISH / #elif GERMAN, mapped by a pointer array
[STRINGID_X - BATTLESTRINGS_TABLE_START] = sText_X.
Expansion: [STRINGID_X] = COMPOUND_STRING("..."), inline in gBattleStringsTable.
Replace only when expansion's current English normalizes to WW's English.
"""
import re, sys, urllib.request, pathlib

RAW = "https://raw.githubusercontent.com/WalterWoshid/pokeemerald-german/master/src/data/text/../../battle_message.c"
WW_URL = "https://raw.githubusercontent.com/WalterWoshid/pokeemerald-german/master/src/battle_message.c"
EXP = pathlib.Path("/home/denotzgii/pokeemerald-expansion/src/battle_message.c")

def norm(s):
    s = re.sub(r'\\[np]', ' ', s)
    s = re.sub(r'\{[^}]*\}', '', s)
    return re.sub(r'[^A-Za-z0-9]', '', s).upper()

SYM_RE = re.compile(r'static const u8 (\w+)\[\]\s*=\s*_\(\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)\s*;', re.S)
def parse_syms(text):
    return {m.group(1): "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)))
            for m in SYM_RE.finditer(text)}

def main():
    apply = "--apply" in sys.argv
    ww = urllib.request.urlopen(WW_URL).read().decode()
    # english region: from "#if ENGLISH" (first) to matching "#elif GERMAN"
    e0 = ww.index("#if ENGLISH")
    g0 = ww.index("#elif GERMAN", e0)
    e1 = ww.index("#endif", g0)
    # there are multiple such blocks; collect all
    en_syms, de_syms = {}, {}
    pos = 0
    while True:
        try:
            a = ww.index("#if ENGLISH", pos)
        except ValueError:
            break
        b = ww.index("#elif GERMAN", a)
        c = ww.index("#endif", b)
        en_syms.update(parse_syms(ww[a:b]))
        de_syms.update(parse_syms(ww[b:c]))
        pos = c + 1
    # pointer array
    ptr = dict(re.findall(r'\[(STRINGID_[A-Z0-9_]+)\s*-\s*BATTLESTRINGS_TABLE_START\]\s*=\s*(\w+)', ww))
    sid_en = {k: en_syms[v] for k, v in ptr.items() if v in en_syms}
    sid_de = {k: de_syms[v] for k, v in ptr.items() if v in de_syms}
    print(f"WW: {len(ptr)} STRINGID ptrs, {len(sid_en)} en, {len(sid_de)} de")

    txt = EXP.read_text()
    blk = re.compile(
        r'(\[(?P<k>STRINGID_[A-Z0-9_]+)\]\s*=\s*COMPOUND_STRING\(\s*)'
        r'(?P<body>(?:"(?:[^"\\]|\\.)*"\s*)+)(\))', re.S)
    st = {'repl':0,'already':0,'nowd':0,'div':0}; div=[]
    out=[]; last=0
    for m in blk.finditer(txt):
        k = m.group('k'); body = m.group('body')
        cur = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', body))
        d = sid_de.get(k); e = sid_en.get(k)
        if d is None: st['nowd']+=1; continue
        if norm(cur) == norm(d): st['already']+=1; continue
        toks = lambda s: set(re.findall(r'\{B_[A-Z0-9_]+\}', s))
        loose = "--loose" in sys.argv
        if e is not None and norm(cur) == norm(e):
            out.append(txt[last:m.start('body')]); out.append('"%s"' % d); last = m.end('body')
            st['repl']+=1
        elif loose and toks(cur) == toks(d) and toks(cur):
            # wording diverged but the German uses exactly the placeholders this
            # context provides -> safe drop-in
            out.append(txt[last:m.start('body')]); out.append('"%s"' % d); last = m.end('body')
            st['repl']+=1
        else:
            st['div']+=1; div.append((k, cur[:45], d[:45]))
    out.append(txt[last:])
    print("battle strings:", st)
    if "--verbose" in sys.argv:
        for k,c,d in div[:80]: print(f"  DIV {k}: {c!r} -> {d!r}")
    if apply:
        EXP.write_text("".join(out)); print("wrote")

if __name__ == "__main__":
    main()
