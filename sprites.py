"""
Pixel-art sprites for Commit Critter, rendered as small animated SVGs. Stdlib only.

Bodies are drawn as fill-only grids ('.' = empty); the dark outline is added automatically
around every shape. Faces and mood effects are stamped on top, so each species needs just
one body plus a few coordinates.
"""

from html import escape

W, H = 40, 28          # canvas, in art pixels
GROUND = 23            # first row of ground; sprites stand on it
SCALE = 8              # screen pixels per art pixel

OUTLINE = "#2d2433"
SHARED = {
    "K": OUTLINE, "W": "#ffffff", "P": "#ff8fa3", "R": "#e8506b",
    "Y": "#ffd23f", "y": "#fff3b0", "H": "#ff5d8f", "U": "#8fd3ff", "V": "#3b8fd9",
    "Z": "#7c8199", "G": "#c9ccd6", "g": "#9a9eae",
}

MOOD_STYLE = {
    "light": {
        #            card bg    ground     grass
        "ecstatic": ("#fff4c9", "#f1d98a", "#d9b95a"),
        "happy":    ("#e3f6e5", "#b9e2bf", "#8fc99a"),
        "meh":      ("#eceff4", "#d3d8e2", "#b4bbc9"),
        "hungry":   ("#ffe9da", "#f3cbb0", "#dba98a"),
        "starving": ("#e6e4ea", "#cbc8d1", "#aaa6b2"),
    },
    # One Dark-ish, to sit with the usual dark README widgets (stats cards, 3D graphs).
    "dark": {
        "ecstatic": ("#3b3527", "#4d4430", "#6b5d3a"),
        "happy":    ("#263329", "#2f4234", "#46604c"),
        "meh":      ("#2c313a", "#363c47", "#4b5263"),
        "hungry":   ("#3a2d27", "#4a3830", "#664c40"),
        "starving": ("#2e2b33", "#38343e", "#4e4957"),
    },
}

# Face pieces. Lowercase 'l' = the species' shade colour (eyelids, cheeks).
EYES = {
    "ecstatic": [".K.", "K.K"],
    "happy":    ["KK", "WK", "KK"],
    "meh":      ["ll", "KK"],
    "hungry":   ["KK", "KK", "UU"],
    "starving": ["K.K", ".K.", "K.K"],
}
SHUT = ["..", "KK"]
MOUTHS = {
    "ecstatic": ["KKKK", "KRRK", ".KK."],
    "happy":    ["K..K", ".KK."],
    "meh":      ["KKK"],
    "hungry":   [".KK.", "K..K"],
    "starving": ["K.K.", ".K.K"],
}

SPARKLE = ["..Y..", ".yYy.", "YYWYY", ".yYy.", "..Y.."]
HEART = [".HH.HH.", "HHWHHHH", "HHHHHHH", ".HHHHH.", "..HHH..", "...H..."]
DROP = [".V.", "VUV", "VUW", ".V."]
ZZ = ["ZZZZ", "..Z.", ".Z..", "ZZZZ"]
CLOUD = ["..GGG....", ".GGGGGGG.", "GGGGGGGGG", ".ggggggg.", "..U...U..", "....U...."]

SPECIES = {
    "snail": {
        "palette": {"A": "#b89cf2", "B": "#7d5ccc", "C": "#e6dbff",
                    "S": "#ffe2a6", "T": "#efbe72", "D": "#ff8fa3"},
        "shade": "T",
        "body": [
            ".................DD...DD..",
            ".................DD...DD..",
            "..................T...T...",
            "......AAAAA.......T...T...",
            "....AAAAAAAAA....SSSSSSSS.",
            "...AACCAAAAAAA..SSSSSSSSSS",
            "..AACBBBBBBBAAA.SSSSSSSSSS",
            "..ACBAAAAAAABAA.SSSSSSSSSS",
            ".AACBAABBBBABAA.SSSSSSSSSS",
            ".AACBABAAABABAA.SSSSSSSSSS",
            ".AAABABBA.BABAA.SSSSSSSSSS",
            ".AAABAAAAABAAAA.SSSSSSSSSS",
            "..AAABBBBBAAAA...SSSSSSSS.",
            "...AAAAAAAAAA..SSSSSSSSSS.",
            "SSSSSSSSSSSSSSSSSSSSSSSSS.",
            ".TTTTTTTTTTTTTTTTTTTTTTT..",
        ],
        "eyes": ((17, 7), (23, 7)),
        "mouth": (21, 10),
        "blush": ((16, 9), (24, 9)),
    },
    "crab": {
        "palette": {"A": "#ff7563", "B": "#d9473b", "C": "#ffc2b5"},
        "shade": "B",
        "body": [
            ".AA.AA..............AA.AA.",
            ".AA.AA..............AA.AA.",
            ".AAAAA..............AAAAA.",
            "..AAA................AAA..",
            "...A.......CCAA.......A...",
            "...A.....AACCAAAAA....A...",
            "...AA..AAAAAAAAAAAAA.AA...",
            "....AAAAAAAAAAAAAAAAAA....",
            "......AAAAAAAAAAAAAA......",
            "......AAAAAAAAAAAAAA......",
            "......AAAAAAAAAAAAAA......",
            ".......BBBBBBBBBBBB.......",
            "......B.B.B....B.B.B......",
            ".....B.B.B......B.B.B.....",
        ],
        "eyes": ((9, 7), (15, 7)),
        "mouth": (13, 10),
        "blush": ((7, 10), (18, 10)),
    },
    "cat": {
        "palette": {"A": "#f6a65e", "B": "#d97a2b", "C": "#fff0da", "D": "#ffb3c1"},
        "shade": "B",
        "body": [
            "..A..........A......",
            "..AA........AA......",
            "..ADA..BB..ADA......",
            "..ADDAABBAADDA......",
            ".AAAAAAAAAAAAAA.....",
            ".AAAAAAAAAAAAAA.....",
            "BAAAAAAAAAAAAAAB....",
            ".AAAAAAAAAAAAAA.....",
            "BAAACCCCCCCCAAAB....",
            ".AACCCCCCCCCCAA.....",
            "..AACCCCCCCCAA......",
            "..AAACCCCCCAAA...AA.",
            ".AAAACCCCCCAAAA..AA.",
            ".ABAACCCCCCAABA..BA.",
            ".AAAACCCCCCAAAA.AA..",
            ".ABAACCCCCCAABAAA...",
            ".AAAAAAAAAAAAAAAA...",
            "..CCC.AAAAAA.CCC....",
        ],
        "eyes": ((4, 6), (10, 6)),
        "mouth": (8, 9),
        "blush": ((2, 9), (12, 9)),
    },
    "slime": {
        "palette": {"A": "#72d8c9", "B": "#3ea596", "C": "#e6fffa",
                    "D": "#8ad46f", "E": "#4f9e47"},
        "shade": "B",
        "body": [
            "..........DD........",
            ".........DDE.EE.....",
            "..........E.DD......",
            ".......AAAAAA.......",
            ".....AAAAAAAAAA.....",
            "....ACCAAAAAAAAA....",
            "...ACCAAAAAAAAAAA...",
            "...ACAAAAAAAAAAAA...",
            "..AAAAAAAAAAAAAAAA..",
            "..AAAAAAAAAAAAAAAA..",
            ".AAAAAAAAAAAAAAAAAA.",
            ".AAAAAAAAAAAAAAAAAA.",
            "AAAAAAAAAAAAAAAAAAAA",
            "BBBBBBBBBBBBBBBBBBBB",
            ".BBBBBBBBBBBBBBBBBB.",
        ],
        "eyes": ((6, 8), (12, 8)),
        "mouth": (10, 11),
        "blush": ((4, 11), (14, 11)),
    },
}

ANIM = {
    "ecstatic": ".bob{animation:hop .6s steps(1) infinite}@keyframes hop{50%{transform:translateY(-2px)}}",
    "happy":    ".bob{animation:bob 1.2s steps(1) infinite}@keyframes bob{50%{transform:translateY(-1px)}}",
    "meh":      ".bob{animation:bob 2.4s steps(1) infinite}@keyframes bob{50%{transform:translateY(-1px)}}",
    "hungry":   ".bob{animation:rumble 3s steps(1) infinite}@keyframes rumble"
                "{80%{transform:translateX(-1px)}84%{transform:translateX(1px)}88%{transform:translateX(-1px)}92%{transform:none}}",
    "starving": "",
}
BLINK = (".open{animation:open 4s steps(1) infinite}@keyframes open{92%{opacity:0}97%{opacity:1}}"
         ".shut{opacity:0;animation:shut 4s steps(1) infinite}@keyframes shut{92%{opacity:1}97%{opacity:0}}")
TWINKLE = ".tw{animation:tw 1s steps(1) infinite}.tw2{animation-delay:-.5s}@keyframes tw{50%{opacity:.25}}"


# ---------------------------------------------------------------- stats panel
# Drawn at half scale (2 font pixels per art pixel), in a tiny pixel font.

# Card layout, in art pixels: | margin | scene window | gap | stats text | margin |
MARGIN, GAP, TEXT_W = 2, 3, 49
CARD_W, CARD_H = MARGIN + W + GAP + TEXT_W + MARGIN, MARGIN + H + MARGIN
FONT = {
    "A": [".#.", "#.#", "###", "#.#", "#.#"], "B": ["##.", "#.#", "##.", "#.#", "##."],
    "C": [".##", "#..", "#..", "#..", ".##"], "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"], "F": ["###", "#..", "##.", "#..", "#.."],
    "G": [".##", "#..", "#.#", "#.#", ".##"], "H": ["#.#", "#.#", "###", "#.#", "#.#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"], "J": ["..#", "..#", "..#", "#.#", ".#."],
    "K": ["#.#", "#.#", "##.", "#.#", "#.#"], "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#...#", "##.##", "#.#.#", "#...#", "#...#"], "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "O": [".#.", "#.#", "#.#", "#.#", ".#."], "P": ["##.", "#.#", "##.", "#..", "#.."],
    "Q": [".#.", "#.#", "#.#", "##.", ".##"], "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": [".##", "#..", ".#.", "..#", "##."], "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"], "V": ["#.#", "#.#", "#.#", ".#.", ".#."],
    "W": ["#...#", "#...#", "#.#.#", "##.##", "#...#"], "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "Y": ["#.#", "#.#", ".#.", ".#.", ".#."], "Z": ["###", "..#", ".#.", "#..", "###"],
    "0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["##.", "..#", ".#.", "#..", "###"], "3": ["##.", "..#", ".#.", "..#", "##."],
    "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "##.", "..#", "##."],
    "6": [".##", "#..", "###", "#.#", "###"], "7": ["###", "..#", ".#.", ".#.", ".#."],
    "8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "##."],
    " ": ["..", "..", "..", "..", ".."], ".": [".", ".", ".", ".", "#"], "!": ["#", "#", "#", ".", "#"],
    "?": ["##.", "..#", ".#.", "...", ".#."], "-": ["...", "...", "###", "...", "..."],
    "'": ["#", "#", ".", ".", "."], ":": [".", "#", ".", "#", "."], "/": ["..#", "..#", ".#.", "#..", "#.."],
}
PANEL = {
    "light": {"K": OUTLINE, "k": "#7a7287", "H": "#ff5d8f", "h": "#ddd7e3", "F": "#fdfbff", "f": "#e2dce8"},
    "dark":  {"K": "#e6e1ec", "k": "#9da5b4", "H": "#ff6b9a", "h": "#454b57", "F": "#21252b", "f": "#3a3f4b"},
}
MOOD_INK = {
    "light": {"ecstatic": "#c98a00", "happy": "#2f9a52", "meh": "#6b7285", "hungry": "#d9662b", "starving": "#8a5aa8"},
    "dark":  {"ecstatic": "#e5c07b", "happy": "#98c379", "meh": "#abb2bf", "hungry": "#e8935c", "starving": "#c678dd"},
}
THEMES = tuple(PANEL)
HEART_ICON = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]


def _text_width(text):
    return sum(len(FONT.get(c, FONT["?"])[0]) + 1 for c in text) - 1


def _text(layer, x, y, text, ink):
    for c in text:
        glyph = FONT.get(c, FONT["?"])
        _stamp(layer, [r.replace("#", ink) for r in glyph], x, y)
        x += len(glyph[0]) + 1
    return x


def _panel(stats, mood, theme):
    """Stats text pixels, in half-scale units, and the colours they use."""
    px = {}
    x0, inner = (MARGIN + W + GAP) * 2, (TEXT_W - 1) * 2
    top = (CARD_H * 2 - 42) // 2         # the text block is 42 half-pixels tall

    name, species = stats["name"].upper(), f"THE {stats['species'].upper()}"
    while _text_width(f"{name} {species}") > inner and len(name) > 1:
        name = name[:-1].rstrip()
    _text(px, _text(px, x0, top, name, "K") + 3, top, species, "k")
    _text(px, x0, top + 8, mood.upper(), "M")
    for x in range(x0, x0 + inner, 2):   # dotted divider
        px[(x, top + 16)] = "h"

    full = 10 - stats["hunger"]          # 0..10, shown as five hearts that can be half full
    x = _text(px, x0, top + 21, "FULL", "k") + 3
    for i in range(5):
        filled = min(max(full - 2 * i, 0), 2)
        cut = {0: 0, 1: 4, 2: 7}[filled]
        _stamp(px, [r[:cut].replace("#", "H") + r[cut:].replace("#", "h") for r in HEART_ICON], x, top + 20)
        x += 8

    def line(y, *pairs):
        x = x0
        for label, value in pairs:
            x = _text(px, _text(px, x, y, label, "k") + 2, y, value, "K") + 6

    line(top + 29, ("STREAK", f"{stats['streak']}D"), ("BEST", f"{stats['best']}D"))
    line(top + 37, ("AGE", f"{stats['age']}D"), ("ATE TODAY", str(stats["food_today"])))
    return px, {**PANEL[theme], "M": MOOD_INK[theme][mood]}


def _grey(hex_colour, amount):
    """Blend a colour towards its own grey by `amount` (0 = unchanged, 1 = fully grey)."""
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    y = 0.3 * r + 0.59 * g + 0.11 * b
    return "#%02x%02x%02x" % tuple(round(c + (y - c) * amount) for c in (r, g, b))


def _stamp(layer, art, x, y):
    for dy, row in enumerate(art):
        for dx, ch in enumerate(row):
            if ch != ".":
                layer[(x + dx, y + dy)] = ch


def _outline(pixels):
    out = {}
    for (x, y) in pixels:
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (nx, ny) not in pixels:
                out[(nx, ny)] = "O"
    return out


def _rects(pixels, colours):
    """Merge horizontal runs of the same colour into one <rect> each."""
    out = []
    for y in sorted({y for _, y in pixels}):
        xs = sorted(x for x, yy in pixels if yy == y)
        run_start = prev = None
        for x in xs + [None]:
            if run_start is not None and (x != prev + 1 or pixels[(x, y)] != pixels[(run_start, y)]):
                out.append(f'<rect x="{run_start}" y="{y}" width="{prev - run_start + 1}" height="1" '
                           f'fill="{colours[pixels[(run_start, y)]]}"/>')
                run_start = None
            if x is not None and run_start is None:
                run_start = x
            prev = x
    return "".join(out)


def svg(species, mood, title="", stats=None, theme="light"):
    sp = SPECIES[species]
    body = sp["body"]
    w, h = max(map(len, body)), len(body)
    ox, oy = (W - w) // 2, GROUND - h  # top-left of the sprite on the canvas

    colours = {**SHARED, **sp["palette"], "O": OUTLINE, "l": sp["palette"][sp["shade"]]}
    grey = {"hungry": 0.25, "starving": 0.75}.get(mood, 0)
    if grey:
        colours = {k: v if k in "OK" else _grey(v, grey) for k, v in colours.items()}

    fill = {}
    _stamp(fill, body, ox, oy)
    sprite = {**_outline(fill), **fill}

    (lx, ly), (rx, ry) = sp["eyes"]
    face = {}
    if mood in ("ecstatic", "happy"):
        for bx, by in sp["blush"]:
            _stamp(face, ["PP"], ox + bx, oy + by)
    mouth = MOUTHS[mood]
    mx, my = sp["mouth"]
    _stamp(face, mouth, ox + mx - len(mouth[0]) // 2, oy + my)

    eye = EYES[mood]
    ew = len(eye[0])
    open_eyes, shut_eyes = {}, {}
    # Wider eye glyphs are centred on the 2px eye slot; the right eye's highlight is mirrored.
    _stamp(open_eyes, eye, ox + lx - (ew - 2) // 2, oy + ly)
    _stamp(open_eyes, [r[::-1] for r in eye], ox + rx - (ew - 2) // 2, oy + ry)
    for ex, ey in sp["eyes"]:
        _stamp(shut_eyes, SHUT, ox + ex, oy + ey)

    # Effects float around the sprite, outside the bobbing group so they don't jitter with it.
    fx, fx2 = {}, {}
    if mood == "ecstatic":
        _stamp(fx, HEART, max(ox - 8, 1), oy - 1)
        _stamp(fx2, SPARKLE, ox + w + 2, oy - 3)
        _stamp(fx, SPARKLE, ox + w + 4, oy + 6)
    elif mood == "meh":
        _stamp(fx, ZZ, ox + w + 1, oy)
        _stamp(fx2, ZZ, ox + w + 4, oy - 4)
    elif mood == "hungry":
        _stamp(fx, DROP, ox + w + 1, oy + 2)
    elif mood == "starving":
        _stamp(fx, CLOUD, ox + w - 4, max(oy - 7, 0))

    bg, ground, grass = MOOD_STYLE[theme][mood]
    shadow_w = w - 4
    css = ANIM[mood] + (BLINK if mood in ("happy", "meh", "hungry") else "")
    css += TWINKLE if fx else ""
    css += "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

    def group(pixels, cls="", palette=colours):
        if not pixels:
            return ""
        attr = f' class="{cls}"' if cls else ""
        return f"<g{attr}>{_rects(pixels, palette)}</g>"

    blinks = mood in ("happy", "meh", "hungry")
    eyes = group(open_eyes, "open" if blinks else "") + (group(shut_eyes, "shut") if blinks else "")
    tufts = "".join(f'<rect x="{x}" y="{GROUND - 1}" width="1" height="1" fill="{grass}"/>'
                    f'<rect x="{x + 1}" y="{GROUND - 2}" width="1" height="2" fill="{grass}"/>'
                    for x in (3, 12, 30, 35))

    scene = (
        f'<rect width="{W}" height="{H}" rx="2" fill="{bg}"/>'
        f'<rect y="{GROUND}" width="{W}" height="{H - GROUND}" fill="{ground}"/>'
        f"{tufts}"
        f'<rect x="{ox + 2}" y="{GROUND}" width="{shadow_w}" height="1" fill="{OUTLINE}" opacity=".18"/>'
        f'<g class="bob">{group(sprite)}{group(face)}{eyes}</g>'
        f'{group(fx, "tw")}{group(fx2, "tw tw2")}'
    )
    width, height, body = W, H, scene
    if stats:
        width, height = CARD_W, CARD_H
        panel_px, panel_colours = _panel(stats, mood, theme)
        body = (
            f'<rect x=".2" y=".2" width="{width - .4}" height="{height - .4}" rx="3" '
            f'fill="{panel_colours["F"]}" stroke="{panel_colours["f"]}" stroke-width=".4"/>'
            f'<clipPath id="scene"><rect width="{W}" height="{H}" rx="2"/></clipPath>'
            f'<g transform="translate({MARGIN} {MARGIN})" clip-path="url(#scene)">{scene}</g>'
            f'<g transform="scale(.5)">{_rects(panel_px, panel_colours)}</g>'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width * SCALE}" height="{height * SCALE}" shape-rendering="crispEdges">'
        + (f"<title>{escape(title)}</title>" if title else "")
        + f"<style>{css}</style>{body}</svg>\n"
    )
