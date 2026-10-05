"""Wrap the Pilot Lines Monitor (EuroCDP edition) page for GitHub Pages.

Usage: python3 tools/publish.py <eu-pilot-lines-eurocdp.html> [index.html]

The editorial page is a fragment (title, styles, markup, data block, script). This adds the
doctype, head metadata and body so GitHub Pages serves a complete document. The data block
<script type="application/json" id="monitor-data"> is kept as it is.
"""
import sys, pathlib

DESC = ("Independent weekly view of the 11 EU Chips Act pilot lines from the design side: readiness for open access, "
        "design kits and MPW runs, access timeline and the link to the European Chips Design Platform (EuroCDP). Alpha version.")

def build(src):
    if src.lstrip().lower().startswith('<!doctype'):
        return src
    assert 'id="monitor-data"' in src, 'data block missing'
    head_end = src.index('</style>') + len('</style>')
    meta = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<meta name="description" content="{DESC}">\n<meta name="robots" content="noindex">\n')
    return ('<!doctype html>\n<html lang="en">\n<head>\n' + meta + src[:head_end] + '\n</head>\n<body>\n'
            + src[head_end:] + '\n</body>\n</html>\n')

if __name__ == '__main__':
    out = build(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
    if len(sys.argv) > 2:
        pathlib.Path(sys.argv[2]).write_text(out, encoding='utf-8')
    else:
        sys.stdout.write(out)
