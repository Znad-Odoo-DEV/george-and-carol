# -*- coding: utf-8 -*-
"""
Regenerates the blossom garland and drops it into index.html.

The surround and the two leaves used to be generated here too. They are
photographs now -- assets/door-frame.jpg and the two halves cut from it -- so
the garland is all that is still drawn. Its geometry is fitted to that
photograph's arch inside build-gate.py; change one and you must change both.
"""

import io
import subprocess
import sys

frag = subprocess.run([sys.executable, 'build-gate.py'], capture_output=True, text=True,
                      encoding='utf-8', check=True).stdout
art = frag[frag.index('<!-- GARLAND -->') + len('<!-- GARLAND -->'):].strip()

p = 'index.html'
s = io.open(p, encoding='utf-8').read()
open_tag = '<div class="gate__garland" aria-hidden="true">'
i = s.index(open_tag) + len(open_tag)
j = s.index('</svg>', i) + len('</svg>')
print(f'garland: {j - i} -> {len(art)} chars')
io.open(p, 'w', encoding='utf-8').write(s[:i] + art + s[j:])
