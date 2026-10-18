"""Builds dark_mode.svg and light_mode.svg: a fastfetch-style profile card.

Edit INFO below, then run:  python3 make_cards.py
"""

from html import escape

INFO = [
    ("header", "arttuaarnio@github"),
    ("tagline", "i code, sometimes. claude codes more."),
    ("blank", ""),
    ("row", "Web", "arttuaarnio.com"),
    ("row", "OS", "macOS, tiled by AeroSpace"),
    ("row", "Shell", "zsh + powerlevel10k"),
    ("row", "Terminal", "WezTerm"),
    ("row", "Editor", "VS Code, Claude Code CLI, Neovim"),
    ("row", "Theme", "Catppuccin Macchiato"),
    ("row", "Languages", "TypeScript/JavaScript, Python, Go"),
    ("blank", ""),
    ("section", "Interests"),
    ("row", "Music", "hip-hop, r&b, jazz"),
    ("row", "Food", "cooking, coffee and eating, mostly eating"),
    ("row", "Billiards", "always one more rack"),
    ("row", "Fashion", "streetwear"),
    ("blank", ""),
    ("swatches", ""),
]

# fastfetch's macOS logo
APPLE = r'''                     ..'
                 ,xNMM.
               .OMMMMo
               lMM"
     .;loddo:.  .olloddol;.
   cKMMMMMMMMMMNWMMMMMMMMMM0:
 .KMMMMMMMMMMMMMMMMMMMMMMMWd.
 XMMMMMMMMMMMMMMMMMMMMMMMX.
;MMMMMMMMMMMMMMMMMMMMMMMM:
:MMMMMMMMMMMMMMMMMMMMMMMM:
.MMMMMMMMMMMMMMMMMMMMMMMMX.
 kMMMMMMMMMMMMMMMMMMMMMMMMWd.
 'XMMMMMMMMMMMMMMMMMMMMMMMMMMk
  'XMMMMMMMMMMMMMMMMMMMMMMMMK.
    kMMMMMMMMMMMMMMMMMMMMMMd
     ;KMMMMMMMWXXWMMMMMMMk.
       "cooc*"    "*coo'"'''.split("\n")
LEAF_ROWS = 4  # first rows are the leaf

# Catppuccin Macchiato (dark) and Latte (light)
THEMES = {
    "dark_mode.svg": dict(
        bg="#24273a", border="#363a4f", text="#cad3f5", dim="#6e738d", ball="#a5adcb",
        leaf="#a6da95", key="#f5a97f", accent="#8aadf4",
        swatches=["#ed8796", "#f5a97f", "#eed49f", "#a6da95", "#8bd5ca", "#8aadf4", "#c6a0f6", "#f5bde6"],
    ),
    "light_mode.svg": dict(
        bg="#eff1f5", border="#ccd0da", text="#4c4f69", dim="#9ca0b0", ball="#4c4f69",
        leaf="#40a02b", key="#fe640b", accent="#1e66f5",
        swatches=["#d20f39", "#fe640b", "#df8e1d", "#40a02b", "#179299", "#1e66f5", "#8839ef", "#ea76cb"],
    ),
}

W, H = 920, 420
FONT = "Menlo, Consolas, 'DejaVu Sans Mono', monospace"
# logo grid
LX, LY, LCW, LLH = 30, 62, 8.2, 17   # left x, first baseline, char width, line height
# info column
IX, IY, ILH = 330, 48, 20
LABEL_WIDTH = 22  # label + dot leader, in characters


def text(x, y, s, fill, size=13, weight="normal", length=None):
    extra = f' textLength="{length:.1f}" lengthAdjust="spacing"' if length else ""
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}"'
            f' xml:space="preserve"{extra}>{escape(s)}</text>')


def logo(t):
    out = []
    for row, line in enumerate(APPLE):
        color = t["leaf"] if row < LEAF_ROWS else t["ball"]
        # textLength keeps every row on the same character grid whatever monospace font the viewer has
        out.append(text(LX, LY + row * LLH, line.rstrip(), color, size=14, length=len(line.rstrip()) * LCW))
    return out


def info(t):
    out, y = [], IY
    for kind, *parts in INFO:
        if kind == "header":
            out.append(f'<text x="{IX}" y="{y}" font-size="14" xml:space="preserve">'
                       f'<tspan fill="{t["accent"]}" font-weight="bold">{escape(parts[0])} </tspan>'
                       f'<tspan fill="{t["dim"]}">{"─" * (62 - len(parts[0]))}</tspan></text>')
        elif kind == "tagline":
            out.append(text(IX, y, parts[0], t["text"], size=14, weight="bold"))
        elif kind == "section":
            out.append(f'<text x="{IX}" y="{y}" font-size="13" xml:space="preserve">'
                       f'<tspan fill="{t["accent"]}" font-weight="bold">{escape(parts[0])} </tspan>'
                       f'<tspan fill="{t["dim"]}">{"─" * (66 - len(parts[0]))}</tspan></text>')
        elif kind == "row":
            label, value = parts
            dots = " " + "." * (LABEL_WIDTH - len(label) - 3) + " "
            out.append(f'<text x="{IX}" y="{y}" font-size="13" xml:space="preserve">'
                       f'<tspan fill="{t["key"]}">{escape(label)}:</tspan>'
                       f'<tspan fill="{t["dim"]}">{dots}</tspan>'
                       f'<tspan fill="{t["text"]}">{escape(value)}</tspan></text>')
        elif kind == "swatches":
            for i, c in enumerate(t["swatches"]):
                out.append(f'<rect x="{IX + i * 30}" y="{y - 13}" width="26" height="16" rx="3" fill="{c}"/>')
        y += ILH
    return out


for name, t in THEMES.items():
    body = "\n".join(logo(t) + info(t))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">\n'
           f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>\n'
           f'{body}\n</svg>\n')
    with open(name, "w") as f:
        f.write(svg)
    print("wrote", name)
