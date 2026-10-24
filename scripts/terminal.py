"""Gera terminal.svg: janela de terminal que digita os comandos. Só stdlib.

Edite LINES e rode: python scripts/terminal.py
"""
import os
from html import escape

BG, BAR, FG, DIM, ACCENT = "#0d1117", "#161b22", "#c9d1d9", "#6e7681", "#3fb950"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SIZE, CW, LH = 16, 9.6, 30  # fonte, largura de 1 caractere (textLength força), altura da linha

# ("cmd", texto) é digitado; ("out", [(texto, cor), ...]) aparece de uma vez; ("gap",) pula meia linha
LINES = [
    ("cmd", "whoami"),
    ("out", [("Jefferson Morais", FG), ("  ·  ", DIM), ("Dev C#/.NET", ACCENT), ("  ·  ", DIM), ("Brasil", FG)]),
    ("gap",),
    ("cmd", "cat stack.txt"),
    ("out", [("C#", "#a179dc"), ("  .NET", "#8f7cf7"), ("  WPF", "#58a6ff"), ("  ASP.NET Core", "#b392f0"),
             ("  SignalR", "#f0883e"), ("  TypeScript", "#3178c6"), ("  Angular", "#f85149"), ("  SQL", "#e3b341")]),
    ("gap",),
    ("cmd", "cat sobre.txt"),
    ("out", [("Construo coisas que eu mesmo uso: apps de desktop pro Windows,", FG)]),
    ("out", [("sistemas web e jogos que rodam no navegador.", FG)]),
    ("gap",),
]

W = 820


def render():
    body, y, t = [], 74, 0.6
    for line in LINES:
        if line[0] == "gap":
            y += LH // 2
            continue
        if line[0] == "cmd":
            text = line[1]
            n, x = len(text), 52
            dur = 0.06 * n
            body.append(f'<text x="28" y="{y}" style="fill:{ACCENT}">❯</text>'
                        f'<text x="{x}" y="{y}" textLength="{n * CW}" lengthAdjust="spacing">{escape(text)}</text>'
                        # cobre o texto e anda um caractere por passo: efeito de digitação
                        f'<rect x="{x}" y="{y - SIZE}" width="{n * CW + 2}" height="{SIZE + 6}" fill="{BG}" '
                        f'style="animation:type {dur:.2f}s steps({n}) {t:.2f}s forwards"/>')
            t += dur + 0.35
        else:
            spans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in line[1])
            n = sum(len(s) for s, _ in line[1])
            body.append(f'<text class="o" x="52" y="{y}" textLength="{n * CW}" lengthAdjust="spacing" '
                        f'style="animation-delay:{t:.2f}s">{spans}</text>')
            t += 0.25
        y += LH
    body.append(f'<text class="o" x="28" y="{y}" style="fill:{ACCENT};animation-delay:{t:.2f}s">❯</text>'
                f'<rect class="k" x="52" y="{y - SIZE + 1}" width="{CW}" height="{SIZE + 3}" fill="{FG}" '
                f'style="animation-delay:{t:.2f}s"/>')
    h = y + 30
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">',
        f"""<style>
text{{font-family:{FONT};font-size:{SIZE}px;fill:{FG};white-space:pre}}
.o{{opacity:0;animation:in .25s forwards}}
.k{{opacity:0;animation:in .1s forwards,blink 1s steps(1) infinite}}
@keyframes in{{to{{opacity:1}}}}
@keyframes type{{to{{transform:translateX(100%)}}}}
@keyframes blink{{50%{{fill:transparent}}}}
rect{{transform-box:fill-box}}
</style>""",
        f'<rect width="{W}" height="{h}" rx="12" fill="{BG}" stroke="#30363d"/>',
        f'<path d="M0.5 12A11.5 11.5 0 0 1 12 .5h{W - 24}A11.5 11.5 0 0 1 {W - .5} 12v26H.5z" fill="{BAR}"/>',
        *(f'<circle cx="{22 + i * 20}" cy="19" r="6" fill="{c}"/>' for i, c in enumerate(("#ff5f56", "#ffbd2e", "#27c93f"))),
        f'<text x="{W / 2}" y="24" text-anchor="middle" style="font-size:13px;fill:{DIM}">jefferson@github: ~</text>',
        *body,
        "</svg>",
    ])


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "terminal.svg"), "w", encoding="utf-8") as f:
        f.write(render())
