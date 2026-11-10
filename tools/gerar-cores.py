#!/usr/bin/env python3
"""Gera os esquemas de cor do Draconic a partir de docs/design-system.md.

O documento é a fonte da verdade: este script lê a tabela "Cores (tokens por
função)" e escreve:

  files/system/usr/share/color-schemes/DraconicClaro.colors
  files/system/usr/share/color-schemes/DraconicEscuro.colors
  files/system/etc/xdg/kdeglobals   (padrões do sistema: fontes, ícones, tema
                                     global e as cores do tema claro)
  files/system/usr/share/wallpapers/Draconic/   papel de parede liso (token
                                     "wallpaper"), com versão clara e escura

Uso (na raiz do repositório):
    python3 tools/gerar-cores.py

Rode de novo sempre que mudar uma cor no documento e commite os arquivos gerados.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOC = RAIZ / "docs" / "design-system.md"
SAIDA_CORES = RAIZ / "files/system/usr/share/color-schemes"
SAIDA_KDEGLOBALS = RAIZ / "files/system/etc/xdg/kdeglobals"
SAIDA_PAPEL = RAIZ / "files/system/usr/share/wallpapers/Draconic"

# Tokens que precisam existir no documento.
OBRIGATORIOS = [
    "wallpaper", "text.primary", "text.secondary", "surface.window", "surface.chrome",
    "surface.elevated", "fill", "border.separator", "accent", "on-accent",
    "status.success", "status.warning", "status.error",
]

HEX = re.compile(r"#([0-9A-Fa-f]{6})")


def ler_tokens() -> tuple[dict[str, str], dict[str, str]]:
    """Lê a tabela de cores e devolve (claro, escuro) como {token: 'RRGGBB'}."""
    claro: dict[str, str] = {}
    escuro: dict[str, str] = {}
    dentro = False
    for linha in DOC.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            dentro = linha.startswith("## Cores")
            continue
        if not dentro or not linha.startswith("| `"):
            continue
        colunas = [c.strip() for c in linha.strip("|").split("|")]
        if len(colunas) < 3:
            continue
        token = colunas[0].strip("`")
        hc, he = HEX.search(colunas[1]), HEX.search(colunas[2])
        if hc and he:  # linhas como "focus.ring | âmbar 55%" ficam de fora
            claro[token] = hc.group(1).upper()
            escuro[token] = he.group(1).upper()
    faltando = [t for t in OBRIGATORIOS if t not in claro]
    if faltando:
        sys.exit(f"Tokens não encontrados em {DOC}: {', '.join(faltando)}")
    return claro, escuro


def rgb(hexa: str) -> str:
    """'C8873A' -> '200,135,58' (formato dos arquivos .colors do KDE)."""
    return ",".join(str(int(hexa[i:i + 2], 16)) for i in (0, 2, 4))


def grupo(t: dict[str, str], fundo: str, fundo_alt: str) -> dict[str, str]:
    """Um grupo [Colors:*] com as cores de texto e de estado do tema."""
    return {
        "BackgroundAlternate": rgb(fundo_alt),
        "BackgroundNormal": rgb(fundo),
        "DecorationFocus": rgb(t["accent"]),
        "DecorationHover": rgb(t["accent"]),
        "ForegroundActive": rgb(t["accent"]),
        "ForegroundInactive": rgb(t["text.secondary"]),
        # Os protótipos não definem cor de link: links herdam a cor do texto.
        "ForegroundLink": rgb(t["text.primary"]),
        "ForegroundNegative": rgb(t["status.error"]),
        "ForegroundNeutral": rgb(t["status.warning"]),
        "ForegroundNormal": rgb(t["text.primary"]),
        "ForegroundPositive": rgb(t["status.success"]),
        "ForegroundVisited": rgb(t["text.secondary"]),
    }


def esquema(t: dict[str, str], oposto: dict[str, str]) -> dict[str, dict[str, str]]:
    """Monta todos os grupos de um esquema (claro ou escuro)."""
    g: dict[str, dict[str, str]] = {}
    g["Colors:Window"] = grupo(t, t["surface.chrome"], t["fill"])
    g["Colors:View"] = grupo(t, t["surface.window"], t["surface.chrome"])
    g["Colors:Button"] = grupo(t, t["surface.window"], t["fill"])
    g["Colors:Header"] = grupo(t, t["surface.chrome"], t["surface.chrome"])
    g["Colors:Header][Inactive"] = grupo(t, t["surface.chrome"], t["surface.chrome"])
    g["Colors:Tooltip"] = grupo(t, t["surface.elevated"], t["surface.chrome"])
    # Áreas "complementares" (OSD, alguns painéis): usam o tema oposto.
    g["Colors:Complementary"] = grupo(oposto, oposto["surface.window"], oposto["surface.chrome"])

    # Seleção: âmbar sólido com texto escuro (on-accent), em listas e menus.
    sel = grupo(t, t["accent"], t["accent"])
    sel.update({
        "ForegroundActive": rgb(t["on-accent"]),
        "ForegroundInactive": rgb(t["on-accent"]),
        "ForegroundLink": rgb(t["on-accent"]),
        "ForegroundNormal": rgb(t["on-accent"]),
        "ForegroundVisited": rgb(t["on-accent"]),
    })
    g["Colors:Selection"] = sel

    # Efeitos de desabilitado/inativo: os mesmos valores do Breeze.
    g["ColorEffects:Disabled"] = {
        "Color": "56,56,56", "ColorAmount": "0", "ColorEffect": "0",
        "ContrastAmount": "0.65", "ContrastEffect": "1",
        "IntensityAmount": "0.1", "IntensityEffect": "2",
    }
    g["ColorEffects:Inactive"] = {
        "ChangeSelectionColor": "true", "Color": "112,111,110",
        "ColorAmount": "0.025", "ColorEffect": "2", "ContrastAmount": "0.1",
        "ContrastEffect": "2", "Enable": "false",
        "IntensityAmount": "0", "IntensityEffect": "0",
    }
    g["WM"] = {
        "activeBackground": rgb(t["surface.chrome"]),
        "activeBlend": rgb(t["surface.chrome"]),
        "activeForeground": rgb(t["text.primary"]),
        "inactiveBackground": rgb(t["surface.chrome"]),
        "inactiveBlend": rgb(t["surface.chrome"]),
        "inactiveForeground": rgb(t["text.secondary"]),
    }
    return g


def escrever_ini(grupos: dict[str, dict[str, str]]) -> str:
    partes = []
    for nome, chaves in grupos.items():
        partes.append(f"[{nome}]")
        partes.extend(f"{k}={v}" for k, v in chaves.items())
        partes.append("")
    return "\n".join(partes)


CABECALHO = "# Gerado por tools/gerar-cores.py a partir de docs/design-system.md.\n# Não edite à mão: mude o documento e rode o script de novo.\n\n"

FONTE = "IBM Plex Sans,{tam},-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
FONTE_MONO = "IBM Plex Mono,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"


def main() -> None:
    claro, escuro = ler_tokens()
    SAIDA_CORES.mkdir(parents=True, exist_ok=True)

    for id_, nome, t, o in [
        ("DraconicClaro", "Draconic Claro", claro, escuro),
        ("DraconicEscuro", "Draconic Escuro", escuro, claro),
    ]:
        g = esquema(t, o)
        g["General"] = {"ColorScheme": id_, "Name": nome, "shadeSortColumn": "true"}
        g["KDE"] = {"contrast": "4"}
        (SAIDA_CORES / f"{id_}.colors").write_text(CABECALHO + escrever_ini(g), encoding="utf-8")
        print(f"escrito: {SAIDA_CORES.relative_to(RAIZ)}/{id_}.colors")

    # Padrões do sistema. /etc/xdg vem antes dos padrões do Fedora no
    # XDG_CONFIG_DIRS, então estes valores ganham, inclusive para usuários
    # que já existem (enquanto não mudarem a configuração por conta própria).
    padroes: dict[str, dict[str, str]] = {
        "General": {
            "ColorScheme": "DraconicClaro",
            # 10 pt ≈ 13 px (body); 8 pt ≈ 11 px (caption)
            "font": FONTE.format(tam=10),
            "menuFont": FONTE.format(tam=10),
            "toolBarFont": FONTE.format(tam=10),
            "smallestReadableFont": FONTE.format(tam=8),
            "fixed": FONTE_MONO,
        },
        "WM": {"activeFont": FONTE.format(tam=10)},
        "Icons": {"Theme": "Draconic"},
        "KDE": {
            "LookAndFeelPackage": "org.draconic.claro.desktop",
            "DefaultLightLookAndFeel": "org.draconic.claro.desktop",
            "DefaultDarkLookAndFeel": "org.draconic.escuro.desktop",
            "widgetStyle": "Breeze",
            "SingleClick": "false",
        },
    }
    g = esquema(claro, escuro)
    padroes["WM"].update(g.pop("WM"))
    padroes.update(g)
    SAIDA_KDEGLOBALS.parent.mkdir(parents=True, exist_ok=True)
    SAIDA_KDEGLOBALS.write_text(CABECALHO + escrever_ini(padroes), encoding="utf-8")
    print(f"escrito: {SAIDA_KDEGLOBALS.relative_to(RAIZ)}")
    papel_de_parede(claro, escuro)


def papel_de_parede(claro: dict[str, str], escuro: dict[str, str]) -> None:
    """Pacote de papel de parede liso: images/ (claro) e images_dark/ (escuro).

    O Plasma troca sozinho para images_dark/ quando o tema escuro está ativo.
    """
    import json
    import struct
    import zlib

    def png_liso(hexa: str, largura: int, altura: int) -> bytes:
        cor = bytes(int(hexa[i:i + 2], 16) for i in (0, 2, 4))
        linha = b"\x00" + cor * largura
        dados = zlib.compress(linha * altura, 9)

        def bloco(tipo: bytes, conteudo: bytes) -> bytes:
            return (struct.pack(">I", len(conteudo)) + tipo + conteudo
                    + struct.pack(">I", zlib.crc32(tipo + conteudo) & 0xFFFFFFFF))

        return (b"\x89PNG\r\n\x1a\n"
                + bloco(b"IHDR", struct.pack(">IIBBBBB", largura, altura, 8, 2, 0, 0, 0))
                + bloco(b"IDAT", dados) + bloco(b"IEND", b""))

    meta = {
        "KPackageStructure": "Wallpaper/Images",
        "KPlugin": {
            "Authors": [{"Name": "Projeto Draconic"}],
            "Id": "Draconic",
            "License": "CC0-1.0",
            "Name": "Draconic",
        },
    }
    for pasta, t in (("images", claro), ("images_dark", escuro)):
        destino = SAIDA_PAPEL / "contents" / pasta
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "3840x2160.png").write_bytes(png_liso(t["wallpaper"], 3840, 2160))
    (SAIDA_PAPEL / "metadata.json").write_text(json.dumps(meta, indent=4) + "\n", encoding="utf-8")
    print(f"escrito: {SAIDA_PAPEL.relative_to(RAIZ)} (claro #{claro['wallpaper']}, escuro #{escuro['wallpaper']})")


if __name__ == "__main__":
    main()
