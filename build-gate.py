# -*- coding: utf-8 -*-
"""
Renders the gate as static SVG: a pair of arched church doors in a stone
surround, dressed with a blossom garland.

This invitation is a single HTML file with no build step, so the loops that
would produce the planks, studs, fluting, dentils, voussoirs and blossoms are
unrolled here once and the result pasted in.

    python build-gate.py > gate-fragment.html

Geometry: a leaf is drawn in a 190 x 670 space that maps onto the left half of
the arched opening, and the surround in 600 x 900. The right-hand leaf is the
left one mirrored in CSS, so ids are namespaced per side to avoid collisions.
"""

import math
import sys

out = []
w = out.append


def leaf(side):
    """
    One leaf of a church door.

    Heavy timber laid in vertical boards, banded by two iron straps with
    hammered studs, and struck with a cross in the head of the arch. Where the
    earlier neoclassical leaf was pale and carved, this one is dark and plain:
    a church door is joinery and ironwork, not cabinetmaking.
    """
    i = lambda n: f"door-{side}-{n}"

    # ── Boards. Nine of them, each seam a dark score with a lit edge beside
    #    it, which is what reads as a plank rather than a stripe.
    boards = []
    board_w = 190 / 9
    # Each board a shade off its neighbour, the way a batch of sawn timber is.
    tints = [(None, 0), ('#1a0f06', .13), ('#ffe6c4', .06), ('#0d0703', .12),
             ('#ffe6c4', .09), (None, 0), ('#1a0f06', .09), ('#ffe0b8', .05),
             ('#0d0703', .08)]
    for k, (colour, alpha) in enumerate(tints):
        if not colour:
            continue
        boards.append(
            f'<rect x="{k * board_w:.2f}" y="0" width="{board_w:.2f}" height="670" '
            f'fill="{colour}" opacity="{alpha}"/>'
        )
    for k in range(1, 9):
        x = k * board_w
        boards.append(
            f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="670" stroke="#1d1108" stroke-width="2.2" opacity=".62"/>'
            f'<line x1="{x + 1.6:.1f}" y1="0" x2="{x + 1.6:.1f}" y2="670" stroke="#b08a5c" stroke-width="1.1" opacity=".3"/>'
        )

    # ── Iron straps. Two bands with a spade end, studded along their length.
    def strap(y, h):
        studs = "".join(
            f'<circle cx="{sx}" cy="{y + h / 2:.1f}" r="3.1" fill="#4a4038"/>'
            f'<circle cx="{sx - 0.7}" cy="{y + h / 2 - 0.8:.1f}" r="1.5" fill="#8d8176" opacity=".8"/>'
            for sx in range(18, 176, 22)
        )
        return (
            f'<rect x="0" y="{y}" width="190" height="{h}" fill="url(#{i("iron")})"/>'
            f'<rect x="0" y="{y}" width="190" height="1.4" fill="#8d8176" opacity=".35"/>'
            f'<rect x="0" y="{y + h - 1.4:.1f}" width="190" height="1.4" fill="#14100c" opacity=".5"/>'
            f'{studs}'
        )

    # ── Studs marching around the arched head, following the clip curve.
    head_studs = []
    for k in range(9):
        a = math.pi * (1.0 + (k / 8) * 0.5)      # 180° round to 270°
        cx = 190 + math.cos(a) * 168
        cy = 190 + math.sin(a) * 168
        head_studs.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="#4a4038"/>'
            f'<circle cx="{cx - 0.7:.1f}" cy="{cy - 0.8:.1f}" r="1.4" fill="#8d8176" opacity=".8"/>'
        )

    return f'''<svg class="door__svg" viewBox="0 0 190 670" preserveAspectRatio="none" fill="none" aria-hidden="true">
<defs>
<clipPath id="{i('clip')}"><path d="M0 670 V190 A190 190 0 0 1 190 0 V670 Z"/></clipPath>
<linearGradient id="{i('wood')}" x1="0" y1="0" x2="1" y2="0.3">
<stop offset="0%" stop-color="#9a7145"/><stop offset="42%" stop-color="#7d5a34"/><stop offset="100%" stop-color="#553c22"/>
</linearGradient>
<linearGradient id="{i('iron')}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#5b5049"/><stop offset="45%" stop-color="#3a322c"/><stop offset="100%" stop-color="#241e19"/>
</linearGradient>
<linearGradient id="{i('gold')}" x1="0" y1="0" x2="0.6" y2="1">
<stop offset="0%" stop-color="#eed7a0"/><stop offset="50%" stop-color="#c9a768"/><stop offset="100%" stop-color="#8f7240"/>
</linearGradient>
<filter id="{i('grain')}" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency="0.85 0.014" numOctaves="4" seed="{7 if side == 'left' else 19}"/>
<feColorMatrix type="saturate" values="0"/>
</filter>
<linearGradient id="{i('fall')}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#fff2d8" stop-opacity=".16"/>
<stop offset="42%" stop-color="#000000" stop-opacity="0"/>
<stop offset="100%" stop-color="#100a04" stop-opacity=".42"/>
</linearGradient>
<linearGradient id="{i('shade')}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="#120c07" stop-opacity=".3"/><stop offset="16%" stop-color="#120c07" stop-opacity="0"/>
<stop offset="80%" stop-color="#120c07" stop-opacity="0"/><stop offset="100%" stop-color="#120c07" stop-opacity=".5"/>
</linearGradient>
</defs>
<g clip-path="url(#{i('clip')})">
<rect x="0" y="0" width="190" height="670" fill="url(#{i('wood')})"/>
{''.join(boards)}
<!-- Grain: high frequency across the boards, low along them, which is the
     direction wood actually runs. -->
<rect x="0" y="0" width="190" height="670" filter="url(#{i('grain')})" opacity=".42" style="mix-blend-mode:multiply"/>
<!-- The light comes from the head of the arch; the foot sits in shadow. -->
<rect x="0" y="0" width="190" height="670" fill="url(#{i('fall')})"/>

<!-- The arched frame the boards are set into. -->
<path d="M10 670 V192 A180 180 0 0 1 190 12" stroke="#2b1d12" stroke-width="7" fill="none" opacity=".65"/>
<path d="M14 670 V194 A176 176 0 0 1 190 18" stroke="#916f47" stroke-width="1.4" fill="none" opacity=".45"/>
{''.join(head_studs)}

<!-- The cross, struck in gold in the field between the straps — the
     classic place on a church door, and it leaves the head of the arch
     clear for the monogram. -->
<g fill="url(#{i('gold')})" opacity=".95">
<rect x="89" y="330" width="12" height="118" rx="2"/>
<rect x="61" y="364" width="68" height="12" rx="2"/>
</g>
<g fill="#f6ecd6" opacity=".26">
<rect x="89" y="330" width="3.5" height="118" rx="2"/>
<rect x="61" y="364" width="68" height="3.5" rx="2"/>
</g>

{strap(292, 26)}
{strap(486, 26)}

<!-- The ring handle, hanging from a boss on the meeting stile. -->
<g>
<circle cx="163" cy="382" r="9" fill="url(#{i('iron')})"/>
<circle cx="163" cy="382" r="4" fill="#14100c" opacity=".6"/>
<ellipse cx="163" cy="404" rx="16" ry="18" fill="none" stroke="url(#{i('iron')})" stroke-width="5"/>
<ellipse cx="163" cy="403" rx="16" ry="18" fill="none" stroke="#8d8176" stroke-width="1" opacity=".4"/>
</g>

<!-- Depth at the meeting stile, so the pair reads as two solid slabs. -->
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

    # A cross on the keystone, in place of the earlier rosette.
    keystone_cross = (
        '<rect x="296" y="152" width="8" height="34" rx="1"/>'
        '<rect x="288" y="163" width="24" height="8" rx="1"/>'
    )

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
<g fill="url(#goldTrim)" opacity=".9">{keystone_cross}</g>
<path d="M118 200 C160 206 186 232 196 268 C166 264 134 240 118 200 Z" fill="none" stroke="url(#goldTrim)" stroke-width="1.2" opacity=".55"/>
<path d="M482 200 C440 206 414 232 404 268 C434 264 466 240 482 200 Z" fill="none" stroke="url(#goldTrim)" stroke-width="1.2" opacity=".55"/>
<rect x="0" y="848" width="600" height="52" fill="url(#floorFace)"/>
<rect x="0" y="848" width="600" height="3" fill="#fbf5ea" opacity=".8"/>
<ellipse cx="300" cy="876" rx="210" ry="16" fill="#fff8ec" opacity=".35"/>
<rect x="0" y="0" width="600" height="900" fill="url(#roomLight)" style="mix-blend-mode:screen"/>
</svg>'''


def garland():
    """Blossom garland over the arch and down both jambs, deterministically."""
    # Blush with the lilac of the reference's wisteria running through it.
    tones = ['#f0d6d1', '#cbb2d8', '#f7ece5', '#dfb0ab', '#b9a3ce', '#ecd3cd', '#e0cbe4']
    state = [20260920 & 0xFFFFFFFF]

    def rnd():
        x = state[0]
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        state[0] = x & 0xFFFFFFFF
        return state[0] / 4294967296

    # Fitted to the photographed doorway, not to a drawn one. In the 600 x 900
    # stage the opening spans x 123..477, y 115..785, and its arch is a true
    # semicircle springing at y 292.5 with radius 177 -- so the garland rides
    # just outside that, at 196.
    ARCH_CX, ARCH_CY, ARCH_R = 300.0, 292.5, 196.0
    JAMB_L, JAMB_R, JAMB_TOP, JAMB_RUN = 118.0, 482.0, 292.0, 490.0

    blossoms = []
    arch_count = 300
    for k in range(arch_count):
        t = k / (arch_count - 1)
        ang = math.pi * (1.02 + t * 0.96)
        spread = 26 + math.sin(t * math.pi) * 22
        r = ARCH_R + (rnd() - 0.5) * spread
        blossoms.append((ARCH_CX + math.cos(ang) * r, ARCH_CY + math.sin(ang) * r * 0.98,
                         1.3 + rnd() * 3.6, int(rnd() * len(tones)), t * 700 + rnd() * 260))

    def cascade(x, count, spread, offset):
        for k in range(count):
            t = k / (count - 1)
            blossoms.append((x + (rnd() - 0.5) * spread + math.sin(t * 5 + offset) * 14,
                             JAMB_TOP + t * JAMB_RUN,
                             1.4 + rnd() * 4.2 * (1 - t * 0.3),
                             int(rnd() * len(tones)),
                             500 + t * 620 + rnd() * 220))

    cascade(JAMB_L, 175, 58, 0)
    cascade(JAMB_R, 110, 46, 2.1)

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
