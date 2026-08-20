# -*- coding: utf-8 -*-
"""
Drops the freshly generated gate art into index.html, replacing whatever is
between the markers already there. Anchors on class names rather than on the
section banners, whose box-drawing characters do not survive every shell.
"""

import io
import re
import subprocess
import sys

frag = subprocess.run([sys.executable, 'build-gate.py'], capture_output=True, text=True,
                      encoding='utf-8', check=True).stdout


def piece(tag, nxt):
    a = frag.index(f'<!-- {tag} -->') + len(f'<!-- {tag} -->')
    b = frag.index(f'<!-- {nxt} -->') if nxt else len(frag)
    return frag[a:b].strip()


leaf_l = piece('LEAF-LEFT', 'LEAF-RIGHT')
leaf_r = piece('LEAF-RIGHT', 'SURROUND')
surround = piece('SURROUND', 'GARLAND')
garland = piece('GARLAND', None)

p = 'index.html'
s = io.open(p, encoding='utf-8').read()


def swap(container_open, art, label):
    """Replace the single <svg> living inside `container_open`'s element."""
    global s
    i = s.index(container_open) + len(container_open)
    j = s.index('</svg>', i) + len('</svg>')
    s = s[:i] + art + s[j:]
    print(f'  {label}: {j - i} -> {len(art)} chars')


print('swapping gate art:')
swap('<div class="gate__surround">', surround, 'surround')
swap('<div class="gate__leaf gate__leaf--left">', leaf_l, 'left leaf')
swap('<div class="gate__mirror">', leaf_r, 'right leaf')
swap('<div class="gate__garland" aria-hidden="true">', garland, 'garland')

io.open(p, 'w', encoding='utf-8').write(s)
print('done;', len(s), 'chars')
