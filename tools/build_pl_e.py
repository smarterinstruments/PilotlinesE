"""Build the EU Pilot Lines Monitor, EuroCDP edition, from the Pillar I Monitor data.

Usage: python3 tools/build_pl_e.py <pillar1-monitor.html | data.json> [eu-pilot-lines-eurocdp.html]

Reads the shared monitor data (the <script type="application/json" id="monitor-data"> block of the
Pillar I Monitor page, or a data.json), keeps what concerns the pilot lines, adds the design-side
layer (EuroCDP services, design teams and roadmap, pilot-line design kits) and fills
tools/pl_e_template.html. tools/publish.py wraps the result for GitHub Pages.
This edition links to EuroCDP only; it carries no aCCCess or competence-centre content.
"""
import json, sys, os, re

TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pl_e_template.html')
SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else 'eu-pilot-lines-eurocdp.html'

raw = open(SRC, encoding='utf-8').read()
m = re.search(r'<script type="application/json" id="monitor-data">\n?(.*?)\n?</script>', raw, re.S)
d = json.loads((m.group(1) if m else raw).replace('<\\/', '</'))

lines = d['lines']
cdp = d['cdp']
ring = lambda n: [l['name'] for l in lines if l['ring'] == n]
quant = [l for l in lines if l['sector'] == 'quant']
KIT = re.compile(r'\bPDKs?\b|\bADKs?\b|\bMPW\b|design kit', re.I)
kits_now = [l['name'] for l in lines if KIT.search(l['now'])]
kits_next = [l['name'] for l in lines if not KIT.search(l['now']) and KIT.search(l['next'])]
pdk_svc = next((s for s in cdp['services'] if 'PDK' in s['s']), None)

stats = [
    {"v": str(len(lines)), "l": "pilot lines", "s": f"{len(lines) - len(quant)} semiconductor, {len(quant)} quantum"},
    {"v": str(len(ring(1)) + len(ring(2))), "l": "take external users today",
     "s": "open access: " + ", ".join(ring(1)) + "; early access: " + ", ".join(ring(2))},
    {"v": str(len(kits_now)), "l": "offer design kits or MPW today", "s": ", ".join(kits_now) + "; " + str(len(kits_next)) + " more have announced PDKs, ADKs or MPW runs"},
    {"v": (pdk_svc or {}).get('st', 'planned'), "l": "pilot-line PDKs on EuroCDP", "s": (pdk_svc or {}).get('n', '')},
]

design = [{"id": l['id'], "name": l['name'], "sector": l['sector'], "ring": l['ring'], "now": l['now'], "next": l['next'], "entry": l['entry'],
           "kit": "now" if KIT.search(l['now']) else ("next" if KIT.search(l['next']) else "")}
          for l in lines]

cdp_links = dict(cdp['links'])
legal = [
    "Chips JU Work Programme (decision GB 2023.51): pilot-line PDKs must be available through the European design platform.",
    "Chips Act 2.0 proposal COM(2026) 504: the pilot lines continue, and the design platform is proposed to continue with pilot-line PDKs integrated.",
]

skip = ('aCCCess', 'competence centres', 'Chips Venture Forum', 'Blumorpho', 'survey', 'HCHiP', 'training catalogue')
seen, sources = set(), []
for name, url in d['sources']:
    if any(k.lower() in name.lower() for k in skip) or not url or url in seen:
        continue
    seen.add(url); sources.append([name, url])

out = {
    "meta": {**d['meta'],
             "lede": "Where the 11 pilot lines of the EU Chips Act stand on the road to open access, which design kits and multi-project wafer runs they offer, and how the European Chips Design Platform (EuroCDP) connects chip designers to them. Updated weekly from the lines' own channels, CORDIS and the Chips JU."},
    "stats": stats,
    "sectors": d['sectors'],
    "rings": d['rings'],
    "lines": [{k: v for k, v in l.items() if k != 'ccc'} for l in lines],
    "design": design,
    "newsTypes": d['newsTypes'],
    "news": sorted([n for n in d['news'] if 'pl' in n['c']], key=lambda n: n['d'], reverse=True),
    "events": sorted([e for e in d['events'] if ('pl' in e['c'] or 'cdp' in e['c']) and not ('acc' in e['c'] and 'cdp' not in e['c'])], key=lambda e: e['d']),
    "next": [x for x in d['overview']['next'] if x['c'] == 'pl'],
    "cdp": {
        "lede": "EuroCDP, the European Chips Design Platform, is the design-side entry point of the Chips for Europe Initiative: EDA tools, IP, training, design support and venture development for start-ups and SMEs. Under the Chips JU Work Programme, pilot-line design kits are to become available through the design platform; until then the lines hand out their kits directly.",
        "ctas": [
            {"t": "Design tools and IP", "p": "EDA framework agreements and IP access for start-ups and SMEs, with training to match.", "b": "Services", "u": cdp_links.get('Services', 'https://eurocdp.eu/services/')},
            {"t": "Training", "p": "Courses on analog and digital IC design, open-source flows and high-level synthesis.", "b": "Training", "u": "https://eurocdp.eu/training/"},
            {"t": "Start-up programme", "p": "Incubate and Accelerate tracks for chip start-ups; EuroCDP takes no equity.", "b": "Start-up programme", "u": cdp_links.get('Start-up programme', 'https://eurocdp.eu/startup-programme/')},
        ],
        "facts": cdp['facts'],
        "services": cdp['services'],
        "agreements": cdp['agreements'],
        "dets": cdp['dets'],
        "roadmap": cdp['roadmap'],
    },
    "legal": legal,
    "feedback": {
        "banner": d['feedback']['banner'],
        "intro": "This page is an independent view of the EU Chips Act pilot lines from the design side, built to sit alongside the European Chips Design Platform. It reports what the lines and EuroCDP publish. Tell us what is wrong, what is missing and what would make it useful.",
        "questions": [
            ["Accuracy", "Is your pilot line or service described correctly? What is missing or out of date?"],
            ["Design kits", "Which PDK, ADK or MPW information is missing? Which release dates should we track?"],
            ["Readiness scale", "Do the four levels (open access running, early access, preparing access, ramp-up) describe readiness well?"],
            ["Indicators", "Which two or three indicators would help designers most? For example PDKs available on the design platform, MPW run dates, turnaround times, published prices."],
            ["Data contribution", "Would your pilot line or design team send a short monthly status line?"],
            ["Home", "Should this page stay independent, or be linked or hosted by EuroCDP or the Chips JU?"],
        ],
        "contactNote": "Short answers are enough; a correction can be one line. Please mention which pilot line or service you refer to.",
        "email": d['feedback']['email'],
    },
    "sources": sources,
    "method": "Compiled from the pilot lines' and EuroCDP's websites and LinkedIn company pages, CORDIS, the Chips JU and partner press releases. Each weekly edition adds new items and changes only the facts they affect. Dates marked ≈ are derived from the relative age of a post. Design-kit flags are set where a line's published offer names PDKs, ADKs or MPW runs.",
}

dump = lambda v: json.dumps(v, ensure_ascii=False)
parts = []
for i, (k, v) in enumerate(out.items()):
    end = ',' if i < len(out) - 1 else ''
    if isinstance(v, list):
        parts.append(f'  {dump(k)}: [\n' + ',\n'.join(f'    {dump(x)}' for x in v) + f'\n  ]{end}')
    else:
        parts.append(f'  {dump(k)}: {dump(v)}{end}')
body = ('{\n' + '\n'.join(parts) + '\n}').replace('</', '<\\/')
html = open(TPL, encoding='utf-8').read().replace('/*__DATA__*/', body)
open(OUT, 'w', encoding='utf-8').write(html)
print(OUT, len(html), 'news', len(out['news']), 'events', len(out['events']), 'sources', len(sources), 'kits now', kits_now, 'next', kits_next)
