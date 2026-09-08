#!/usr/bin/env python3
"""Port German .string translations from WalterWoshid/pokeemerald-german into
the expansion's .inc text files, matching by gText_ label.

Usage: port_de.py <relative/path/to/file.inc> [--apply]
Without --apply: dry run, prints a report.
"""
import sys, re, subprocess, urllib.request, pathlib

RAW = "https://raw.githubusercontent.com/WalterWoshid/pokeemerald-german/master/"
EXP_ROOT = pathlib.Path("/home/denotzgii/pokeemerald-expansion")

def fetch(rel):
    with urllib.request.urlopen(RAW + rel) as r:
        return r.read().decode("utf-8")

LABEL_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)::\s*$')

def parse_blocks(text):
    """label -> list of raw lines belonging to that block (excluding the label line)."""
    lines = text.split("\n")
    blocks = {}
    cur = None
    for ln in lines:
        m = LABEL_RE.match(ln)
        if m:
            cur = m.group(1)
            blocks[cur] = []
            continue
        if cur is not None:
            if ln.strip() == "" :
                cur = None
            else:
                blocks[cur].append(ln)
    return blocks

STR_RE = re.compile(r'^\s*\.string\s')

def extract_german(block_lines):
    """From a block that may contain .ifdef ENGLISH / .ifdef GERMAN, return the
    list of German .string lines. If there is no .ifdef, return the plain
    .string lines (already-translated or shared)."""
    joined = "\n".join(block_lines)
    if "GERMAN" not in joined:
        # no german variant present
        return None
    out = []
    state = None  # None, 'en', 'de'
    depth = 0
    for ln in block_lines:
        s = ln.strip()
        if s.startswith(".ifdef ENGLISH"):
            state = "en"; continue
        if s.startswith(".ifdef GERMAN"):
            state = "de"; continue
        if s == ".else":
            continue
        if s == ".endif":
            state = None; continue
        if state == "de" and STR_RE.match(ln):
            out.append(ln)
    return out or None

BASELINE = "6382807d40"  # pre-Njeri-work commit; files unchanged since here are safe to auto-port

def is_pristine(rel):
    r = subprocess.run(["git", "-C", str(EXP_ROOT), "diff", "--quiet", BASELINE, "HEAD", "--", rel])
    return r.returncode == 0

def main():
    rel = sys.argv[1]
    apply = "--apply" in sys.argv
    force = "--force" in sys.argv
    if not is_pristine(rel) and not force:
        print(f"REFUSE {rel}: modified since {BASELINE} (likely custom Swiss-German). Use --force to override.")
        return
    exp_path = EXP_ROOT / rel
    exp_text = exp_path.read_text()
    try:
        de_text = fetch(rel)
    except Exception as e:
        print(f"SKIP {rel}: not in walterwoshid ({e})")
        return

    de_blocks = parse_blocks(de_text)
    exp_lines = exp_text.split("\n")

    matched, no_german, missing_in_exp = [], [], []
    # find german strings per label
    de_strings = {}
    for lbl, blk in de_blocks.items():
        g = extract_german(blk)
        if g:
            de_strings[lbl] = g
        else:
            no_german.append(lbl)

    out_lines = []
    i = 0
    n = len(exp_lines)
    exp_labels = set()
    while i < n:
        ln = exp_lines[i]
        m = LABEL_RE.match(ln)
        if not m:
            out_lines.append(ln); i += 1; continue
        lbl = m.group(1)
        exp_labels.add(lbl)
        out_lines.append(ln); i += 1
        # collect this block's lines
        blk_start = i
        while i < n and exp_lines[i].strip() != "" and not LABEL_RE.match(exp_lines[i]):
            i += 1
        blk = exp_lines[blk_start:i]
        if lbl in de_strings and any(STR_RE.match(x) for x in blk):
            # replace .string lines, keep any non-.string lines (rare)
            new_blk = []
            replaced = False
            for x in blk:
                if STR_RE.match(x):
                    if not replaced:
                        new_blk.extend(de_strings[lbl])
                        replaced = True
                else:
                    new_blk.append(x)
            out_lines.extend(new_blk)
            matched.append(lbl)
        else:
            out_lines.extend(blk)

    for lbl in de_strings:
        if lbl not in exp_labels:
            missing_in_exp.append(lbl)

    print(f"=== {rel} ===")
    print(f"  matched & translated : {len(matched)}")
    print(f"  exp labels w/o german match : {sorted(set(l for l in exp_labels if l not in matched))}")
    print(f"  german labels not in exp    : {missing_in_exp}")
    print(f"  walterwoshid blocks w/o german : {no_german}")

    if apply:
        exp_path.write_text("\n".join(out_lines))
        print(f"  --> written {exp_path}")

if __name__ == "__main__":
    main()
