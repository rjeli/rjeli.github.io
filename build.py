#!/usr/bin/env python3
import json
import shutil
import tempfile
import subprocess
from pathlib import Path

Page = '''
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
        <title>{title}</title>
        <link rel="stylesheet" href="/res/style.css" />
        <script
          type="text/javascript"
          src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js"
          ></script>
    </head>
    <body>
        <h2><a href="/">rje.li</a></h2>
        {body}
    </body>
</html>
'''

HERE = Path(__file__).parent.resolve()
print(HERE)

OUT = HERE / 'docs'

shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()
shutil.copytree(HERE / 'res', OUT / 'res')
shutil.copytree(HERE / '.well-known', OUT / '.well-known')

'''
with tempfile.NamedTemporaryFile(suffix='.template', delete_on_close=False) as f:
    f.write('\n/* Syntax highlighting */\n$highlighting-css$'.encode('utf-8'))
    f.close()
    css = subprocess.run(
        ['pandoc', '--highlight-style=pygments', f'--template={f.name}'],
        check=True,
        input='`x`{.python}'.encode('utf-8'),
        capture_output=True,
    ).stdout.decode('utf-8')
with open(OUT / 'res' / 'style.css', 'a') as f:
    f.write(css)
'''

POSTS = []

def mkpost(stem, md):
    ymd = stem.split('-')[:3]
    title = md.split('\n')[0].lstrip('# ')
    body = subprocess.run(
        ['pandoc', '-f', 'markdown', '-t', 'html', '--mathjax'],
        check=True,
        input=md.encode('utf-8'),
        capture_output=True,
    ).stdout.decode('utf-8')
    html = Page.format(title=title, body=body)
    with open(OUT / (stem+'.html'), 'w') as f:
        f.write(html)
    POSTS.append(('-'.join(ymd), title, '/'+stem+'.html'))

for p in HERE.glob('posts/*.md'):
    with open(p, 'r') as f:
        mkpost(p.stem, f.read())

for p in HERE.glob('posts/*.ipynb'):
    with open(p, 'r') as f:
        j = json.load(f)
    md = ''
    for cell in j['cells']:
        src = cell['source']
        if cell['cell_type'] == 'markdown':
            md += ''.join(src) + '\n\n'
        elif cell['cell_type'] == 'code':
            if src[0].startswith('# @details'):
                summary = src[0].lstrip('# @details').rstrip()
                md += f'<details><summary>{summary}</summary>\n'
                md += '```python\n'
                md += ''.join(src[1:]) + '\n\n'
                md += '```\n'
                md += '</details>\n'
            else:
                md += '```python\n'
                md += ''.join(src) + '\n\n'
                md += '```\n'
            # if not cell.get('outputs', []):
                # md += '<p style="text-align: center;">✓</p>\n'

        for o in cell.get('outputs', []):
            md += '<div class=output>\n'
            if o['output_type'] == 'execute_result':
                md += ''.join(o['data']['text/latex']) + '\n\n'
            elif o['output_type'] == 'stream':
                md += '```\n'
                md += ''.join(o['text']) + '\n'
                md += '```\n'
            md += '</div>'

    mkpost(p.stem, md)

POSTS.sort(key=lambda x: x[0], reverse=True)
index = '<ul>\n'
for (ymd, title, href) in POSTS:
    index += f'<li>{ymd} <a href="{href}">{title}</a></li>\n'
index += '</ul>\n'

with open(OUT / 'index.html', 'w') as f:
    f.write(Page.format(title='rje.li', body=index))
