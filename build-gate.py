# -*- coding: utf-8 -*-
"""
Renders the arched-door gate as static SVG.

The original lives in the Ahmed & Alaa React project, where the fluting,
dentils, voussoirs and blossoms are produced by loops at render time. This
invitation is a single HTML file with no build step, so those loops are
unrolled here once and the result is pasted in.

    python build-gate.py > gate-fragment.html

Geometry is unchanged from the original: the leaf is drawn in a 190 x 670
space that maps onto the left half of the arched opening, and the surround in
600 x 900. Only the ids are namespaced differently, so the two mirrored leaves
never collide.
"""

import io
import math
import sys

out = []
w = out.append


def leaf(side):
    """One door leaf. The right-hand copy is this mirrored in CSS."""
    i = lambda n: f"door-{side}-{n}"

    # The eight-petal rosette at the head of the upper panel.
    petals = []
    for k in range(8):
        a = (k / 8) * math.pi * 2
        cx, cy = 95 + math.cos(a) * 16, 132 + math.sin(a) * 16
        rot = math.degrees(a) + 90
        petals.append(
            f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="3.4" ry="6.4" '
            f'transform="rotate({rot:.2f} {cx:.2f} {cy:.2f})"/>'
        )

    drop = []
    for cx, cy, r in [(95, 262, 7), (83, 253, 5), (107, 253, 5),
                      (88, 272, 4.4), (102, 272, 4.4), (95, 280, 3.6)]:
        drop.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.4:.2f}" fill="#f6ecd6" opacity=".7"/>'
        )

    rosettes = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="3.6" fill="url(#{i("gold")})" opacity=".8"/>'
        for cx, cy in [(46, 408), (144, 408), (46, 588), (144, 588)]
    )

    return f'''<svg class="door__svg" viewBox="0 0 190 670" preserveAspectRatio="none" fill="none" aria-hidden="true">
<defs>
<clipPath id="{i('clip')}"><path d="M0 670 V190 A190 190 0 0 1 190 0 V670 Z"/></clipPath>
<linearGradient id="{i('face')}" x1="0" y1="0" x2="1" y2="0.35">
<stop offset="0%" stop-color="#f6ecdd"/><stop offset="45%" stop-color="#efe2ce"/><stop offset="100%" stop-color="#e0cdb1"/>
</linearGradient>
<linearGradient id="{i('recess')}" x1="0" y1="0" x2="0.3" y2="1">
<stop offset="0%" stop-color="#d8c4a2"/><stop offset="100%" stop-color="#eee1cc"/>
</linearGradient>
<linearGradient id="{i('gold')}" x1="0" y1="0" x2="0.6" y2="1">
<stop offset="0%" stop-color="#eed7a0"/><stop offset="50%" stop-color="#c9a768"/><stop offset="100%" stop-color="#8f7240"/>
</linearGradient>
<linearGradient id="{i('shade')}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="#8a6f4e" stop-opacity=".16"/><stop offset="14%" stop-color="#8a6f4e" stop-opacity="0"/>
<stop offset="82%" stop-color="#8a6f4e" stop-opacity="0"/><stop offset="100%" stop-color="#6d5637" stop-opacity=".3"/>
</linearGradient>
</defs>
<g clip-path="url(#{i('clip')})">
<rect x="0" y="0" width="190" height="670" fill="url(#{i('face')})"/>
<path d="M12 670 V194 A178 178 0 0 1 190 16" stroke="#fbf5ea" stroke-width="3" fill="none" opacity=".9"/>
<path d="M18 670 V196 A172 172 0 0 1 190 24" stroke="#cdb693" stroke-width="1" fill="none" opacity=".7"/>
<path d="M30 306 V126 A65 65 0 0 1 160 126 V306 Z" fill="url(#{i('recess')})" stroke="#c3ac88" stroke-width="1.2"/>
<path d="M36 300 V128 A59 59 0 0 1 154 128 V300 Z" fill="none" stroke="#fbf5ea" stroke-width="1.5" opacity=".8"/>
<g fill="url(#{i('gold')})" opacity=".92">
<circle cx="95" cy="132" r="9"/><circle cx="95" cy="132" r="4" fill="#f3e6cd" opacity=".75"/>
{''.join(petals)}
</g>
<g stroke="url(#{i('gold')})" stroke-width="1.6" fill="none" stroke-linecap="round">
<path d="M95 158 C95 186 82 200 66 208 C56 213 50 224 54 234 C58 243 70 242 74 233 C79 221 72 210 62 208"/>
<path d="M95 158 C95 186 108 200 124 208 C134 213 140 224 136 234 C132 243 120 242 116 233 C111 221 118 210 128 208"/>
<path d="M95 168 V262" opacity=".75"/>
</g>
<g fill="url(#{i('gold')})" opacity=".85">{''.join(drop)}</g>
<rect x="30" y="326" width="130" height="46" rx="1" fill="url(#{i('recess')})" stroke="#c3ac88" stroke-width="1.2"/>
<g stroke="url(#{i('gold')})" stroke-width="1.3" fill="none" stroke-linecap="round">
<path d="M42 349 C58 336 76 336 95 349 C114 336 132 336 148 349"/>
<path d="M42 349 C58 362 76 362 95 349 C114 362 132 362 148 349" opacity=".6"/>
</g>
<circle cx="95" cy="349" r="3.4" fill="url(#{i('gold')})"/>
<rect x="30" y="392" width="130" height="212" rx="1" fill="url(#{i('recess')})" stroke="#c3ac88" stroke-width="1.2"/>
<rect x="36" y="398" width="118" height="200" rx="1" fill="none" stroke="#fbf5ea" stroke-width="1.5" opacity=".8"/>
<path d="M62 436 H128 V496 C128 534 95 552 95 552 C95 552 62 534 62 496 Z" fill="#f3e8d6" stroke="url(#{i('gold')})" stroke-width="1.6"/>
<path d="M69 443 H121 V494 C121 526 95 541 95 541 C95 541 69 526 69 494 Z" fill="none" stroke="url(#{i('gold')})" stroke-width=".8" opacity=".6"/>
<g stroke="url(#{i('gold')})" stroke-width="1.2" fill="none" stroke-linecap="round">
<path d="M95 460 C86 470 86 486 95 498 C104 486 104 470 95 460 Z"/><path d="M95 452 V462"/>
</g>
{rosettes}
<rect x="12" y="620" width="178" height="50" fill="#e3d2b8" opacity=".5"/>
<path d="M12 620 H190" stroke="#fbf5ea" stroke-width="2" opacity=".7"/>
<g>
<rect x="164" y="330" width="16" height="74" rx="8" fill="url(#{i('gold')})" opacity=".9"/>
<circle cx="172" cy="367" r="9" fill="#f3e6cd" opacity=".55"/>
<circle cx="172" cy="367" r="9" fill="none" stroke="url(#{i('gold')})" stroke-width="1.6"/>
<circle cx="172" cy="388" r="4.5" fill="none" stroke="url(#{i('gold')})" stroke-width="1.4"/>
</g>
<rect x="0" y="0" width="190" height="670" fill="url(#{i('shade')})"/>
</g></svg>'''


def surround():
    """Cornice, arch, fluted pilasters, panelled wall, polished floor."""
    dentils = "".join(
        f'<rect x="{4 + k * 15}" y="80" width="9" height="13" fill="#efe3d0" stroke="#d5c3a8" stroke-width=".5"/>'
        for k in range(40)
    )
    beads = "".join(
        f'<ellipse cx="{10 + k * 20}" cy="110" rx="7" ry="6" fill="#f3e8d6" stroke="#cdb693" stroke-width=".6"/>'
        for k in range(30)
    )

    pilasters = []
    for x in (56, 494):
        flutes = ""
        for f in range(5):
            fx = x + 8 + f * 8.5
            flutes += (
                f'<line x1="{fx}" y1="322" x2="{fx}" y2="806" stroke="#d7c6ab" stroke-width="2.2" stroke-linecap="round"/>'
                f'<line x1="{fx + 2}" y1="322" x2="{fx + 2}" y2="806" stroke="#fbf5ea" stroke-width="1" stroke-linecap="round" opacity=".8"/>'
            )
        pilasters.append(
            f'<g><rect x="{x - 8}" y="286" width="66" height="16" fill="url(#stoneLight)" stroke="#d3c2a8" stroke-width=".6"/>'
            f'<rect x="{x - 4}" y="302" width="58" height="8" fill="#e9dcc7"/>'
            f'<rect x="{x}" y="310" width="50" height="510" fill="url(#stoneLight)"/>{flutes}'
            f'<rect x="{x - 6}" y="820" width="62" height="14" fill="url(#stoneLight)" stroke="#d3c2a8" stroke-width=".6"/>'
            f'<rect x="{x - 10}" y="834" width="70" height="14" fill="#e6d8c2" stroke="#d3c2a8" stroke-width=".6"/></g>'
        )

    voussoirs = ""
    for k in range(15):
        a = math.pi * (1.06 + (k / 14) * 0.88)
        x1, y1 = 300 + math.cos(a) * 192, 380 + math.sin(a) * 192
        x2, y2 = 300 + math.cos(a) * 220, 380 + math.sin(a) * 220
        voussoirs += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                      f'stroke="#d9c8ad" stroke-width=".8" opacity=".8"/>')

    keystone = ""
    for k in range(6):
        a = (k / 6) * math.pi * 2
        cx, cy = 300 + math.cos(a) * 12, 168 + math.sin(a) * 12
        keystone += (f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="2.6" ry="5" '
                     f'transform="rotate({math.degrees(a) + 90:.2f} {cx:.2f} {cy:.2f})"/>')

    wall = "".join(
        f'<g opacity=".75"><rect x="{x}" y="180" width="36" height="640" fill="none" stroke="#d3c2a8"/>'
        f'<rect x="{x + 6}" y="186" width="24" height="628" fill="none" stroke="#fbf5ea" stroke-width="1.5"/></g>'
        for x in (4, 560)
    )

    return f'''<svg class="surround__svg" viewBox="0 0 600 900" preserveAspectRatio="xMidYMid slice" fill="none" aria-hidden="true">
<defs>
<linearGradient id="wallFace" x1="0" y1="0" x2="0.25" y2="1">
<stop offset="0%" stop-color="#e8dccb"/><stop offset="55%" stop-color="#f1e7d8"/><stop offset="100%" stop-color="#e2d4c0"/>
</linearGradient>
<linearGradient id="stoneLight" x1="0" y1="0" x2="1" y2="0.2">
<stop offset="0%" stop-color="#faf3e7"/><stop offset="100%" stop-color="#e5d7c0"/>
</linearGradient>
<linearGradient id="goldTrim" x1="0" y1="0" x2="0.7" y2="1">
<stop offset="0%" stop-color="#dcc491"/><stop offset="55%" stop-color="#bb9c66"/><stop offset="100%" stop-color="#96784a"/>
</linearGradient>
<linearGradient id="floorFace" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#e9dcc9"/><stop offset="100%" stop-color="#d9c9b2"/>
</linearGradient>
<radialGradient id="roomLight" cx="42%" cy="12%" r="86%">
<stop offset="0%" stop-color="#fff6e6" stop-opacity=".85"/><stop offset="55%" stop-color="#f6e9d4" stop-opacity=".18"/>
<stop offset="100%" stop-color="#8d7c66" stop-opacity="0"/>
</radialGradient>
</defs>
<rect x="0" y="0" width="600" height="900" fill="url(#wallFace)"/>
{wall}
<rect x="0" y="44" width="600" height="26" fill="url(#stoneLight)"/>
<rect x="0" y="70" width="600" height="8" fill="#dccbb0"/>
{dentils}
<rect x="0" y="95" width="600" height="7" fill="url(#stoneLight)"/>
{beads}
<rect x="0" y="118" width="600" height="4" fill="url(#goldTrim)" opacity=".55"/>
{''.join(pilasters)}
<path d="M78 380 A222 222 0 0 1 522 380 V400 A202 202 0 0 0 98 400 Z" fill="url(#stoneLight)" stroke="#d3c2a8" stroke-width=".8"/>
<path d="M92 380 A208 208 0 0 1 508 380" fill="none" stroke="url(#goldTrim)" stroke-width="1.6" opacity=".7"/>
<path d="M108 380 A192 192 0 0 1 492 380" fill="none" stroke="#cdb693" stroke-width="1"/>
{voussoirs}
<path d="M274 186 H326 L334 148 H266 Z" fill="url(#stoneLight)" stroke="#cdb693" stroke-width=".9"/>
<g fill="url(#goldTrim)" opacity=".85"><circle cx="300" cy="168" r="8"/>{keystone}</g>
<path d="M118 200 C160 206 186 232 196 268 C166 264 134 240 118 200 Z" fill="none" stroke="url(#goldTrim)" stroke-width="1.2" opacity=".55"/>
<path d="M482 200 C440 206 414 232 404 268 C434 264 466 240 482 200 Z" fill="none" stroke="url(#goldTrim)" stroke-width="1.2" opacity=".55"/>
<rect x="0" y="848" width="600" height="52" fill="url(#floorFace)"/>
<rect x="0" y="848" width="600" height="3" fill="#fbf5ea" opacity=".8"/>
<ellipse cx="300" cy="876" rx="210" ry="16" fill="#fff8ec" opacity=".35"/>
<rect x="0" y="0" width="600" height="900" fill="url(#roomLight)" style="mix-blend-mode:screen"/>
</svg>'''


def garland():
    """Blossom garland over the arch and down both jambs, deterministically."""
    tones = ['#f0d6d1', '#e6c2bd', '#f7ece5', '#dfb0ab', '#fbf5ee', '#ecd3cd', '#f4e3da']

    state = [20260918 & 0xFFFFFFFF]

    def rnd():
        x = state[0]
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        state[0] = x & 0xFFFFFFFF
        return state[0] / 4294967296

    blossoms = []

    arch_count = 300
    for k in range(arch_count):
        t = k / (arch_count - 1)
        ang = math.pi * (1.02 + t * 0.96)
        spread = 26 + math.sin(t * math.pi) * 22
        r = 208 + (rnd() - 0.5) * spread
        blossoms.append((300 + math.cos(ang) * r, 380 + math.sin(ang) * r * 0.98,
                         1.3 + rnd() * 3.6, int(rnd() * len(tones)), t * 700 + rnd() * 260))

    def cascade(x, count, spread, offset):
        for k in range(count):
            t = k / (count - 1)
            blossoms.append((x + (rnd() - 0.5) * spread + math.sin(t * 5 + offset) * 14,
                             380 + t * 430,
                             1.4 + rnd() * 4.2 * (1 - t * 0.3),
                             int(rnd() * len(tones)),
                             500 + t * 620 + rnd() * 220))

    cascade(92, 175, 58, 0)
    cascade(508, 110, 46, 2.1)

    parts = []
    for x, y, r, tone, delay in blossoms:
        parts.append(
            f'<g class="garland__blossom" style="--d:{delay:.0f}ms">'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{tones[tone]}" opacity="{0.55 + (tone % 4) * 0.15:.2f}"/>'
            f'<circle cx="{x - r * 0.25:.1f}" cy="{y - r * 0.3:.1f}" r="{r * 0.55:.2f}" fill="url(#blossomSheen)"/>'
            f'</g>'
        )

    return ('<svg class="garland" viewBox="0 0 600 900" fill="none" aria-hidden="true">'
            '<defs><radialGradient id="blossomSheen" cx="35%" cy="30%" r="75%">'
            '<stop offset="0%" stop-color="#fff" stop-opacity=".85"/>'
            '<stop offset="100%" stop-color="#fff" stop-opacity="0"/>'
            '</radialGradient></defs>' + "".join(parts) + '</svg>')


w('<!-- LEAF-LEFT -->')
w(leaf('left'))
w('<!-- LEAF-RIGHT -->')
w(leaf('right'))
w('<!-- SURROUND -->')
w(surround())
w('<!-- GARLAND -->')
w(garland())

sys.stdout.reconfigure(encoding='utf-8')
print("\n".join(out))
