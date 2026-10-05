# Pilot Lines Monitor for chip designers (alpha)

Independent weekly view of the 11 pilot lines of the EU Chips Act (Chips for Europe Initiative) from the design side: how far each line is on the road to open access, which design kits (PDKs, ADKs) and multi-project wafer runs it offers, when external users get in, and how the European Chips Design Platform (EuroCDP) connects designers to the lines.

- Live page: https://smarterinstruments.github.io/PilotlinesE/
- Prepared by Stanislav Černý, Czech National Semiconductor Cluster
- Feedback until 1 November 2026: cerny@semicz.eu
- Not an official publication of EuroCDP, the Chips JU, the European Commission or the pilot lines.

The page uses the visual language of the European Chips Design Platform (eurocdp.eu) and links to its sections, but is a separate site. A sister edition for the network of Chips Competence Centres lives in its own repository.

## Embedding

Add `?embed` to the URL to hide the page's own top bar and footer, so it can sit inside another site, for example as an iframe on eurocdp.eu. A section can be opened directly with an anchor (`#radar`, `#lines`, `#timeline`, `#design`, `#news`, `#events`).

```
<iframe src="https://smarterinstruments.github.io/PilotlinesE/?embed" style="width:100%;height:1600px;border:0" title="Pilot Lines Monitor for chip designers"></iframe>
```

## Data and weekly build

The page is generated from the data of the EU Chips Act Pillar I Monitor (the `monitor-data` JSON block), keeping what concerns the pilot lines and the design platform. All data sit in one JSON block (`<script type="application/json" id="monitor-data">`) inside `index.html`; the page renders itself from it. Updates are published weekly after editorial review.

```
python3 tools/build_pl_e.py pillar1-monitor.html eu-pilot-lines-eurocdp.html   # page from the Pillar I data
python3 tools/publish.py eu-pilot-lines-eurocdp.html index.html               # wrap for GitHub Pages
```

`tools/pl_e_template.html` holds the layout and styles; `tools/build_pl_e.py` holds the selection rules and the texts of the design section.
