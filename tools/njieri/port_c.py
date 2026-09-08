#!/usr/bin/env python3
"""Port German strings for a C source file (multi-line + multi-region aware).

WalterWoshid uses  #ifdef ENGLISH ... #elif GERMAN ... #endif  blocks scattered
through the file. We collect label->body for English (outside any GERMAN region)
and German (inside GERMAN regions), then in the expansion file replace a string
only when its current body is byte-identical to WalterWoshid's English body.
"""
import re, sys, pathlib, urllib.request

RAW = "https://raw.githubusercontent.com/WalterWoshid/pokeemerald-german/master/"

# matches: <prefix> <label>[..] = _( ... );   where ... may span lines
DECL_RE = re.compile(
    r'(?P<pre>\b(?:static\s+)?(?:ALIGNED\(\d+\)\s+)?const u8 (?P<label>[A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*=\s*)_\(',
)

def iter_decls(text):
    """yield (label, start_idx, body_start, body_end, end_idx) for each const u8 X[] = _(...);"""
    for m in DECL_RE.finditer(text):
        i = m.end()  # just after "_("
        depth = 1
        in_str = False
        esc = False
        j = i
        while j < len(text) and depth > 0:
            c = text[j]
            if in_str:
                if esc: esc = False
                elif c == '\\': esc = True
                elif c == '"': in_str = False
            else:
                if c == '"': in_str = True
                elif c == '(': depth += 1
                elif c == ')': depth -= 1
            j += 1
        body = text[i:j-1]           # between _( and )
        yield m.group('label'), m.start('pre'), i, j-1, j

def region_kind(text):
    """return list of (start_line_idx, kind) markers; kind in {'EN','GERMAN','JP','OFF'}"""
    pass

def collect(text, want):
    """want in {'en','de'}: return label->body dict for that language region."""
    lines = text.split('\n')
    # build per-char language state
    state = []  # stack
    cur = 'EN'  # default outside any block
    langflags = {'ENGLISH':'EN','GERMAN':'DE','JAPANESE':'JP','JPN':'JP'}
    charlang = []
    for ln in lines:
        s = ln.strip()
        m = re.match(r'#\s*if(?:def)?\s+(\w+)', s)
        me = re.match(r'#\s*elif\s+(?:defined\()?(\w+)', s)
        if s.startswith('#ifdef') or s.startswith('#if '):
            g = re.findall(r'\b(ENGLISH|GERMAN|JAPANESE|JPN)\b', s)
            state.append(cur)
            cur = langflags.get(g[0], cur) if g else cur
        elif s.startswith('#elif'):
            g = re.findall(r'\b(ENGLISH|GERMAN|JAPANESE|JPN)\b', s)
            if g: cur = langflags[g[0]]
        elif s.startswith('#else'):
            cur = 'EN' if cur != 'EN' else cur
        elif s.startswith('#endif'):
            cur = state.pop() if state else 'EN'
        charlang.append(cur)
        charlang.append(cur)  # placeholder; we'll map by line below
    # simpler: map line index -> lang, then for each decl find its start line
    linelang = []
    state = []
    cur = 'EN'
    for ln in lines:
        s = ln.strip()
        applied = cur
        if s.startswith('#ifdef') or s.startswith('#if '):
            g = re.findall(r'\b(ENGLISH|GERMAN|JAPANESE|JPN)\b', s)
            state.append(cur)
            if g: cur = langflags[g[0]]
        elif s.startswith('#elif'):
            g = re.findall(r'\b(ENGLISH|GERMAN|JAPANESE|JPN)\b', s)
            if g: cur = langflags[g[0]]
            applied = cur
        elif s.startswith('#else'):
            applied = cur
        elif s.startswith('#endif'):
            cur = state.pop() if state else 'EN'
            applied = cur
        linelang.append(cur)
    # offsets of line starts
    offs = [0]
    for ln in lines:
        offs.append(offs[-1] + len(ln) + 1)
    def lang_at(idx):
        # binary search line
        lo, hi = 0, len(lines)-1
        while lo < hi:
            mid = (lo+hi)//2
            if offs[mid+1] <= idx: lo = mid+1
            else: hi = mid
        return linelang[lo]
    out = {}
    tgt = 'EN' if want == 'en' else 'DE'
    for label, ps, bs, be, es in iter_decls(text):
        if lang_at(ps) == tgt:
            out.setdefault(label, text[bs:be])
    return out

def main():
    rel = sys.argv[1]
    apply = "--apply" in sys.argv
    verbose = "--verbose" in sys.argv
    exp_path = pathlib.Path("/home/denotzgii/pokeemerald-expansion") / rel
    exp = exp_path.read_text()
    ww = urllib.request.urlopen(RAW + rel).read().decode("utf-8")

    en = collect(ww, 'en')
    de = collect(ww, 'de')
    print(f"WW: {len(en)} english, {len(de)} german labels")

    # apply replacements right-to-left to keep offsets valid
    repls = []
    stats = {'replaced':0,'already':0,'no_de':0,'diverged':0}
    diverged=[]
    for label, ps, bs, be, es in iter_decls(exp):
        body = exp[bs:be]
        d = de.get(label)
        e = en.get(label)
        if d is None:
            stats['no_de'] += 1; continue
        if body == d:
            stats['already'] += 1; continue
        if e is not None and body == e:
            repls.append((bs, be, d)); stats['replaced'] += 1
        else:
            stats['diverged'] += 1
            diverged.append((label, body[:60]))
    for bs, be, d in sorted(repls, reverse=True):
        exp = exp[:bs] + d + exp[be:]
    print(stats)
    if verbose:
        for l,b in diverged: print("  DIV", l, repr(b))
    if apply:
        exp_path.write_text(exp)
        print("WROTE", exp_path)

if __name__ == "__main__":
    main()
