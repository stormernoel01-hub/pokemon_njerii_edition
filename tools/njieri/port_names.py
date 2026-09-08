#!/usr/bin/env python3
"""Port German move/ability/item NAMES + DESCRIPTIONS from WalterWoshid, keyed by
the MOVE_/ABILITY_/ITEM_ constant. Only replaces when the expansion's current
English text is byte-identical to WalterWoshid's English for that constant.
"""
import re, sys, urllib.request, pathlib

RAW = "https://raw.githubusercontent.com/WalterWoshid/pokeemerald-german/master/"
ROOT = pathlib.Path("/home/denotzgii/pokeemerald-expansion")

def fetch(rel):
    return urllib.request.urlopen(RAW + rel).read().decode("utf-8")

def split_lang(text):
    """return (english_text, german_text) by slicing the #if ENGLISH/#elif GERMAN/#endif"""
    lines = text.split("\n")
    en, de, cur = [], [], None
    for l in lines:
        s = l.strip()
        if re.match(r'#\s*if\b.*ENGLISH', s): cur='en'; continue
        if re.match(r'#\s*elif\b.*GERMAN', s): cur='de'; continue
        if re.match(r'#\s*elif\b', s) or re.match(r'#\s*else\b', s): cur='x'; continue
        if re.match(r'#\s*endif', s): cur=None; continue
        if cur=='en': en.append(l)
        elif cur=='de': de.append(l)
    return "\n".join(en), "\n".join(de)

# --- move names: [MOVE_X] = _("NAME"),
KV_RE = re.compile(r'\[(?P<k>(?:MOVE|ABILITY|ITEM)_[A-Z0-9_]+)\]\s*=\s*_\("(?P<v>(?:[^"\\]|\\.)*)"\)')

def kv_map(text):
    return {m.group('k'): m.group('v') for m in KV_RE.finditer(text)}

def port_move_names(apply):
    ww = fetch("src/data/text/move_names.h")
    en_t, de_t = split_lang(ww)
    en, de = kv_map(en_t), kv_map(de_t)
    p = ROOT / "src/data/moves_info.h"
    txt = p.read_text()
    # each move block: [MOVE_X] =\n    {\n        .name = COMPOUND_STRING("..."),
    blk = re.compile(r'(\[(?P<k>MOVE_[A-Z0-9_]+)\]\s*=\s*\{.*?\n\s*\.name = COMPOUND_STRING\(")(?P<v>(?:[^"\\]|\\.)*)("\))', re.S)
    norm = lambda s: re.sub(r'[^A-Z0-9]', '', s.upper())
    stats = {'repl':0,'already':0,'nowd':0,'div':0}
    diverged=[]
    out=[]; last=0
    for m in blk.finditer(txt):
        k, v = m.group('k'), m.group('v')
        d = de.get(k); e = en.get(k)
        if d is None: stats['nowd']+=1; continue
        if v == d: stats['already']+=1; continue
        # replace when expansion's current name normalizes to WW's English name
        # (expansion decapitalised / respaced, but it's still the vanilla name)
        if e is not None and norm(v) == norm(e):
            out.append(txt[last:m.start('v')]); out.append(d); last = m.end('v')
            stats['repl']+=1
        else:
            stats['div']+=1
            diverged.append((k, v, d))
    if "--verbose" in sys.argv:
        for k,v,d in diverged[:60]: print(f"  DIV {k}: exp={v!r} wwDE={d!r}")
    out.append(txt[last:])
    new = "".join(out)
    print("move names:", stats)
    if apply: p.write_text(new)

def _generic(exp_rel, ww_rel, const_prefix, blk_pat, apply):
    ww = fetch(ww_rel)
    en_t, de_t = split_lang(ww)
    en = {m.group('k'): m.group('v') for m in re.finditer(
        r'\[(?P<k>%s_[A-Z0-9_]+)\]\s*=\s*_\("(?P<v>(?:[^"\\]|\\.)*)"\)' % const_prefix, en_t)}
    de = {m.group('k'): m.group('v') for m in re.finditer(
        r'\[(?P<k>%s_[A-Z0-9_]+)\]\s*=\s*_\("(?P<v>(?:[^"\\]|\\.)*)"\)' % const_prefix, de_t)}
    # WW item names live in per-item #if blocks, not the [K]=_() array form
    if not de:
        for k, body in re.findall(r'\[(%s_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},' % const_prefix, ww, re.S):
            me = re.search(r'#if ENGLISH\s*\n\s*\.name = _\("([^"]*)"\)', body)
            md = re.search(r'#elif GERMAN\s*\n\s*\.name = _\("([^"]*)"\)', body)
            if me: en[k] = me.group(1)
            if md: de[k] = md.group(1)
    p = ROOT / exp_rel
    txt = p.read_text()
    blk = re.compile(blk_pat, re.S)
    norm = lambda s: re.sub(r'[^A-Z0-9]', '', s.upper())
    stats = {'repl':0,'already':0,'nowd':0,'div':0}; div=[]
    out=[]; last=0
    for m in blk.finditer(txt):
        k, v = m.group('k'), m.group('v')
        d = de.get(k); e = en.get(k)
        if d is None: stats['nowd']+=1; continue
        if v == d: stats['already']+=1; continue
        if e is not None and norm(v) == norm(e):
            out.append(txt[last:m.start('v')]); out.append(d); last=m.end('v'); stats['repl']+=1
        else:
            stats['div']+=1; div.append((k,v,d))
    out.append(txt[last:])
    print(f"{exp_rel}:", stats)
    if "--verbose" in sys.argv:
        for k,v,d in div[:50]: print(f"  DIV {k}: {v!r} -> {d!r}")
    if apply: p.write_text("".join(out))

def port_ability_names(apply):
    _generic("src/data/abilities.h", "src/data/text/abilities.h", "ABILITY",
        r'\[(?P<k>ABILITY_[A-Z0-9_]+)\]\s*=\s*\{[^{}]*?\.name = _\("(?P<v>(?:[^"\\]|\\.)*)"\)', apply)

def port_item_names(apply):
    _generic("src/data/items.h", "src/data/items.h", "ITEM",
        r'\[(?P<k>ITEM_[A-Z0-9_]+)\]\s*=\s*\{[^{}]*?\.name = ITEM_NAME\("(?P<v>(?:[^"\\]|\\.)*)"\)', apply)

if __name__ == "__main__":
    a = "--apply" in sys.argv
    port_move_names(a)
    port_ability_names(a)
    port_item_names(a)
