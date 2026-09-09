#!/usr/bin/env python3
"""Replace WalterWoshid's official German Hoenn/Kanto place names with the names
the Njeri hack currently uses, in the given files. Derived from both projects'
region_map_sections JSON; route-number renames are excluded (too risky as blind
substring replace)."""
import json, sys, re, pathlib

ROOT = pathlib.Path("/home/denotzgii/pokeemerald-expansion")
subs = json.load(open("/tmp/claude-1000/-home-denotzgii-pokeemerald-expansion/50494e28-2f58-4c35-847d-ea81458384e8/scratchpad/name_subs.json"))

# drop the risky ROUTE NNN entries; keep everything else
PAIRS = {g: c for g, c in subs.items() if not g.startswith("ROUTE ")}
# person / misc names not in the region map
PAIRS.update({
    "PROF. BIRK": "PROF. LUNTE",
})
# also handle the "CITY"-less short forms WW sometimes uses in prose
for g, c in list(PAIRS.items()):
    if g.endswith(" CITY"):
        PAIRS.setdefault(g[:-5], c.replace(" CITY", "").replace(" TOWN", ""))
    if g.endswith(" TOWN"):
        PAIRS.setdefault(g[:-5], c.replace(" TOWN", "").replace(" CITY", ""))

# longest first so "GRANITHÖHLE" is tried before "GRANIT", etc.
ordered = sorted(PAIRS.items(), key=lambda kv: -len(kv[0]))

def fix(text):
    n = 0
    for g, c in ordered:
        if g in text:
            text = text.replace(g, c)
            n += text.count(c)
    return text, n

total = 0
for rel in sys.argv[1:]:
    p = ROOT / rel
    t = p.read_text()
    nt, _ = fix(t)
    if nt != t:
        p.write_text(nt)
        changed = sum(1 for g, c in ordered if g in t)
        print(f"  {rel}: replaced names from {changed} entries")
        total += 1
print(f"{total} files changed")
