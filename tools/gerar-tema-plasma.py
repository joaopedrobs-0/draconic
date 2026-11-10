#!/usr/bin/env python3
"""Gera os temas do Plasma "draconic-claro" e "draconic-escuro".

O tema do Plasma desenha o fundo dos painéis e alguns ícones da bandeja.
Este script escreve, para cada variante, em files/system/usr/share/plasma/desktoptheme/<id>/:

  metadata.json, plasmarc
  widgets/panel-background.svg       barra superior sólida e, com o prefixo
                                     "south-", a dock de vidro (cantos de 16 px)
  translucent/ e solid/widgets/...   o mesmo desenho (o Plasma escolhe a pasta
                                     conforme o modo de opacidade do painel)
  widgets/tasks.svg                  indicador de app aberto na dock (tracinho)
O que não estiver aqui vem do tema padrão (Breeze).

Ícones da bandeja: no Plasma 6.8 os widgets da bandeja (rede, som, brilho,
bateria, notificações) usam o TEMA DE ÍCONES, não o tema do Plasma. Por isso eles
estão em tools/icones-mapa.tsv, e não aqui.

Valores tirados de design/prototipo/Main.dc.html (barra superior e .dock) e de
docs/design-system.md (border.menubar, dock).

Uso (na raiz do repositório):
    python3 tools/gerar-tema-plasma.py
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "files/system/usr/share/plasma/desktoptheme"

VARIANTES = {
    "draconic-claro": {
        "nome": "Draconic Claro",
        "menubar": "#F3F3F2", "linha": "#CFCFD1",
        "dock": ("#F4F4F5", 0.55), "dock_borda": ("#FFFFFF", 0.7),
        "texto": "#1A1A1A", "texto2": "#55555A", "destaque": "#C8873A",
    },
    "draconic-escuro": {
        "nome": "Draconic Escuro",
        "menubar": "#262628", "linha": "#38383B",
        "dock": ("#28282A", 0.6), "dock_borda": ("#FFFFFF", 0.12),
        "texto": "#EDEDED", "texto2": "#A6A6AB", "destaque": "#D99A4E",
    },
}

RAIO_DOCK = 16          # docs/design-system.md: 16 dock e Busca
MARGEM_DOCK = (4, 8)    # protótipo: padding 4px 8px (vertical, horizontal)


# ---------------------------------------------------------------- fundo do painel
def elementos(prefixo: str, oy: int, raio: int, centro: int, fill: str, fill_op: float,
              borda: str | None, borda_op: float, linha_base: str | None,
              margens: tuple[int, int], com_mascara: bool) -> tuple[list[str], int]:
    """Partes de uma moldura de 9 partes (cantos, lados, centro), a partir de y=oy.

    Devolve (lista de elementos SVG, altura ocupada). Os ids recebem 'prefixo'
    (ex.: "north-" para o painel de cima). raio=0 dá cantos retos; linha_base
    desenha só a borda de baixo (linha divisória da barra superior).

    O Plasma desenha cada parte pelo id, isoladamente; por isso o contorno e a
    linha de baixo ficam DENTRO de cada parte, e não num desenho à parte.
    """
    r = max(raio, 1)
    c = centro
    w = 2 * r + c

    def retangulo(x, y, lw, lh, cor, op):
        return f'<rect x="{x}" y="{y}" width="{lw}" height="{lh}" fill="{cor}" fill-opacity="{op}"/>'

    def lado(id_, x, y, lw, lh, cor, op, contorno=None):
        partes = [retangulo(x, y, lw, lh, cor, op)]
        if contorno and borda:
            partes.append(retangulo(*contorno, borda, borda_op))
        return f'<g id="{id_}">{"".join(partes)}</g>'

    def canto(id_, cx, cy, ox, oy_, cor, op, com_contorno=True):
        if raio == 0:
            return f'<g id="{id_}">{retangulo(ox, oy_, r, r, cor, op)}</g>'
        hx = ox if cx > ox else ox + r
        vy = oy_ if cy > oy_ else oy_ + r
        varre = 1 if (cx > ox) == (cy > oy_) else 0
        partes = [f'<rect x="{ox}" y="{oy_}" width="{r}" height="{r}" fill="none"/>',
                  f'<path d="M{cx},{cy} L{hx},{cy} A{r},{r} 0 0 {varre} {cx},{vy} Z" fill="{cor}" fill-opacity="{op}"/>']
        if borda and com_contorno:
            # contorno de 1 px como ANEL preenchido (um traço aumentaria a área
            # do canto em meio pixel e o Plasma encolheria a peça, deixando uma linha)
            sx = -1 if cx > ox else 1
            sy = -1 if cy > oy_ else 1
            ri = r - 1
            partes.append(
                f'<path d="M{cx + sx * r},{cy} A{r},{r} 0 0 {varre} {cx},{cy + sy * r} '
                f'L{cx},{cy + sy * ri} A{ri},{ri} 0 0 {1 - varre} {cx + sx * ri},{cy} Z" '
                f'fill="{borda}" fill-opacity="{borda_op}"/>')
        return f'<g id="{id_}">{"".join(partes)}</g>'

    def conjunto(p, cor, op, dx=0, contorno=True):
        b = contorno
        y0 = oy
        return [
            canto(f"{p}topleft", dx + r, y0 + r, dx, y0, cor, op, b),
            lado(f"{p}top", dx + r, y0, c, r, cor, op, (dx + r, y0, c, 1) if b else None),
            canto(f"{p}topright", dx + r + c, y0 + r, dx + r + c, y0, cor, op, b),
            lado(f"{p}left", dx, y0 + r, r, c, cor, op, (dx, y0 + r, 1, c) if b else None),
            lado(f"{p}center", dx + r, y0 + r, c, c, cor, op),
            lado(f"{p}right", dx + r + c, y0 + r, r, c, cor, op, (dx + w - 1, y0 + r, 1, c) if b else None),
            canto(f"{p}bottomleft", dx + r, y0 + r + c, dx, y0 + r + c, cor, op, b),
            lado(f"{p}bottom", dx + r, y0 + r + c, c, r, cor, op, (dx + r, y0 + w - 1, c, 1) if b else None),
            canto(f"{p}bottomright", dx + r + c, y0 + r + c, dx + r + c, y0 + r + c, cor, op, b),
        ]

    els = conjunto(prefixo, fill, fill_op)
    if linha_base:
        fora = {f"{prefixo}bottom", f"{prefixo}bottomleft", f"{prefixo}bottomright"}
        els = [e for e in els if re.match(r'<g id="([^"]+)"', e).group(1) not in fora]
        els += [f'<g id="{prefixo}{n}">{retangulo(x, oy + r + c, lw, r, linha_base, 1)}</g>'
                for n, x, lw in [("bottomleft", 0, r), ("bottom", r, c), ("bottomright", r + c, r)]]
    if com_mascara:  # área do desfoque: mesma forma, opaca, ao lado do desenho
        els += conjunto(f"mask-{prefixo}", "#000000", 1, dx=w + 10, contorno=False)

    mv, mh = margens
    hy = oy + w + 4
    els += [
        f'<rect id="{prefixo}hint-top-margin" x="0" y="{hy}" width="4" height="{max(mv, 0.01)}" fill="none"/>',
        f'<rect id="{prefixo}hint-bottom-margin" x="8" y="{hy}" width="4" height="{max(mv, 0.01)}" fill="none"/>',
        f'<rect id="{prefixo}hint-left-margin" x="16" y="{hy}" width="{max(mh, 0.01)}" height="4" fill="none"/>',
        f'<rect id="{prefixo}hint-right-margin" x="28" y="{hy}" width="{max(mh, 0.01)}" height="4" fill="none"/>',
    ]
    return els, w + 4 + max(mv, 4) + 8


def fundo_painel(v: dict) -> str:
    """widgets/panel-background: barra superior sólida (padrão) + dock de vidro ("south-").

    O Plasma pede o fundo com o prefixo da posição do painel ("north" em cima,
    "south" embaixo) e usa as partes sem prefixo quando o prefixo não existe.
    A altura mínima de qualquer painel é calculada pelas partes sem prefixo, por
    isso elas são as da barra (finas, 28 px possíveis); a dock, com cantos de
    16 px, fica no prefixo "south-". A máscara do desfoque segue o padrão do
    KSvg: "mask-" + prefixo ("mask-south-center"...).
    """
    barra, h1 = elementos("", 0, 0, 10, v["menubar"], 1, None, 0, v["linha"], (0, 12), False)
    dock, h2 = elementos("south-", h1, RAIO_DOCK, 10, v["dock"][0], v["dock"][1],
                         v["dock_borda"][0], v["dock_borda"][1], None, MARGEM_DOCK, True)
    largura = 2 * (2 * RAIO_DOCK + 10) + 20
    altura = h1 + h2
    # Repetir (e não esticar) centro e lados evita linhas nas junções das partes.
    dicas = [f'<rect id="hint-tile-center" x="{largura - 6}" y="0" width="4" height="4" fill="none"/>']
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}">\n'
            + "\n".join(barra + dock + dicas) + "\n</svg>\n")


# ---------------------------------------------------------------- indicador de app aberto
def indicador_tarefas(v: dict) -> str:
    """widgets/tasks: como a dock marca os apps.

    Protótipo: tracinho de 12x2 px, 2 px acima da base do botão, na cor do texto
    (app aberto). O Plasma desenha esse indicador como moldura de 9 partes que
    estica: com cantos transparentes de 18 px, num botão de 48 px sobra uma
    linha de 12 px no meio. Minimizado: cor secundária. Pedindo atenção e barra
    de progresso: âmbar. Passar o mouse: fundo suave com cantos de 8 px.
    """
    LARG, ALT, LINHA, FOLGA = 18, 4, 2, 2   # canto, altura da faixa de baixo, espessura, folga até a base
    C = 4                                   # tamanho das peças do meio
    els: list[str] = []
    y = 0

    def faixa(prefixo: str, cor: str | None, op: float = 1.0):
        nonlocal y
        w = 2 * LARG + C
        h = 2 * ALT + C
        nada = 'fill="none"'
        def r(id_, x, yy, lw, lh, extra=""):
            return f'<g id="{prefixo}-{id_}"><rect x="{x}" y="{yy}" width="{lw}" height="{lh}" {nada}/>{extra}</g>'
        linha = ""
        if cor:
            linha = (f'<rect x="{LARG}" y="{y + ALT + C + ALT - FOLGA - LINHA}" width="{C}" height="{LINHA}" '
                     f'fill="{cor}" fill-opacity="{op}"/>')
        els.extend([
            r("topleft", 0, y, LARG, ALT), r("top", LARG, y, C, ALT), r("topright", LARG + C, y, LARG, ALT),
            r("left", 0, y + ALT, LARG, C), r("center", LARG, y + ALT, C, C), r("right", LARG + C, y + ALT, LARG, C),
            r("bottomleft", 0, y + ALT + C, LARG, ALT), r("bottom", LARG, y + ALT + C, C, ALT, linha),
            r("bottomright", LARG + C, y + ALT + C, LARG, ALT),
        ])
        y += h + 4

    def realce(prefixo: str, cor: str, op: float):
        """Fundo arredondado (8 px) para o mouse por cima."""
        nonlocal y
        R, Cc = 8, 4
        w = 2 * R + Cc
        def peca(id_, x, yy, lw, lh, forma):
            return f'<g id="{prefixo}-{id_}"><rect x="{x}" y="{yy}" width="{lw}" height="{lh}" fill="none"/>{forma}</g>'
        def ret(x, yy, lw, lh):
            return f'<rect x="{x}" y="{yy}" width="{lw}" height="{lh}" fill="{cor}" fill-opacity="{op}"/>'
        def setor(cx, cy, hx, vy, varre):
            return f'<path d="M{cx},{cy} L{hx},{cy} A{R},{R} 0 0 {varre} {cx},{vy} Z" fill="{cor}" fill-opacity="{op}"/>'
        y0 = y
        els.extend([
            peca("topleft", 0, y0, R, R, setor(R, y0 + R, 0, y0, 1)),
            peca("top", R, y0, Cc, R, ret(R, y0, Cc, R)),
            peca("topright", R + Cc, y0, R, R, setor(R + Cc, y0 + R, w, y0, 0)),
            peca("left", 0, y0 + R, R, Cc, ret(0, y0 + R, R, Cc)),
            peca("center", R, y0 + R, Cc, Cc, ret(R, y0 + R, Cc, Cc)),
            peca("right", R + Cc, y0 + R, R, Cc, ret(R + Cc, y0 + R, R, Cc)),
            peca("bottomleft", 0, y0 + R + Cc, R, R, setor(R, y0 + R + Cc, 0, y0 + w, 0)),
            peca("bottom", R, y0 + R + Cc, Cc, R, ret(R, y0 + R + Cc, Cc, R)),
            peca("bottomright", R + Cc, y0 + R + Cc, R, R, setor(R + Cc, y0 + R + Cc, w, y0 + w, 1)),
        ])
        y += w + 4

    faixa("normal", v["texto"])
    faixa("focus", v["texto"])
    faixa("minimized", v["texto2"])
    faixa("attention", v["destaque"])
    faixa("progress", v["destaque"])
    realce("hover", v["texto"], 0.08)
    # margens do botão (espaço entre a moldura e o ícone)
    for lado, (lw, lh) in {"top": (4, 2), "bottom": (4, 2), "left": (2, 4), "right": (2, 4)}.items():
        els.append(f'<rect id="normal-hint-{lado}-margin" x="0" y="{y}" width="{lw}" height="{lh}" fill="none"/>')
    y += 8
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="{y}" viewBox="0 0 64 {y}">\n'
            + "\n".join(els) + "\n</svg>\n")


def main() -> None:
    for id_, v in VARIANTES.items():
        base = SAIDA / id_
        if base.exists():
            shutil.rmtree(base)
        (base / "widgets").mkdir(parents=True)
        (base / "solid/widgets").mkdir(parents=True)
        (base / "translucent/widgets").mkdir(parents=True)

        meta = {
            "KPackageStructure": "Plasma/Theme",
            "KPlugin": {
                "Authors": [{"Name": "Projeto Draconic"}],
                "Description": f"Tema do Plasma {v['nome']}",
                "Id": id_,
                "License": "GPL-2.0-or-later",
                "Name": v["nome"],
                "Version": "1.0",
                "Website": "https://github.com/joaopedrobs-0/draconic",
            },
            "X-Plasma-API-Minimum-Version": "6.0",
        }
        (base / "metadata.json").write_text(json.dumps(meta, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
        (base / "plasmarc").write_text(
            "# Desfoque e contraste atrás da dock (vidro). A barra superior é sólida.\n"
            "[ContrastEffect]\nenabled=true\ncontrast=1\nintensity=1\nsaturation=1.6\n\n"
            "[BlurBehindEffect]\nenabled=true\n\n"
            "[AdaptiveTransparency]\nenabled=false\n", encoding="utf-8")

        fundo = fundo_painel(v)
        for pasta in ("widgets", "translucent/widgets", "solid/widgets"):
            (base / pasta / "panel-background.svg").write_text(fundo, encoding="utf-8")
        (base / "widgets/tasks.svg").write_text(indicador_tarefas(v), encoding="utf-8")

        print(f"tema do Plasma gerado: {base.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
