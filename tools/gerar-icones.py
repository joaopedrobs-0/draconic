#!/usr/bin/env python3
"""Gera o tema de ícones "Draconic" a partir do Phosphor (peso regular, licença MIT).

Lê tools/icones-mapa.tsv (nome freedesktop/KDE -> ícone Phosphor) e escreve em
files/system/usr/share/icons/Draconic/:

  index.theme                      herda do Breeze o que não estiver no mapa
  scalable/<contexto>/<nome>.svg   e <nome>-symbolic.svg
  LICENSE-Phosphor.txt

Os SVGs ganham a folha de estilo "current-color-scheme" do KDE, então seguem a
cor do texto do tema (claro ou escuro), como os ícones do Breeze.

Uso (na raiz do repositório):
    python3 tools/gerar-icones.py

O pacote do Phosphor é baixado do npm na versão fixa abaixo e conferido pelo
SHA-256 antes de usar. Fica guardado em tools/.cache/ (fora do git).
"""
from __future__ import annotations

import hashlib
import re
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

PHOSPHOR_VERSAO = "2.1.1"
PHOSPHOR_URL = f"https://registry.npmjs.org/@phosphor-icons/core/-/core-{PHOSPHOR_VERSAO}.tgz"
PHOSPHOR_SHA256 = "313332be6190b724da24107addd781799b48bf76b13963f24501112ffe1baadd"

RAIZ = Path(__file__).resolve().parent.parent
MAPA = RAIZ / "tools" / "icones-mapa.tsv"
CACHE = RAIZ / "tools" / ".cache" / f"phosphor-core-{PHOSPHOR_VERSAO}.tgz"
SAIDA = RAIZ / "files/system/usr/share/icons/Draconic"

CONTEXTOS = {
    "actions": "Actions", "apps": "Applications", "categories": "Categories",
    "devices": "Devices", "emblems": "Emblems", "mimetypes": "MimeTypes",
    "places": "Places", "status": "Status",
}

# Cor usada só quando o app não aplica o esquema de cores (o KDE troca pela cor do tema).
COR_PADRAO = "#1A1A1A"

MODELO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" width="16" height="16">
<style id="current-color-scheme" type="text/css">.ColorScheme-Text {{ color:{cor}; }}</style>
<g class="ColorScheme-Text" fill="currentColor">{conteudo}</g>
</svg>
"""
VIEWBOX_PHOSPHOR = "0 0 256 256"

# Ícones próprios do Draconic: no mapa, a coluna do Phosphor começa com "@".
# "@marca" = assets/logo/draconic-mark.svg (marca reduzida, uma cor).
PROPRIOS = {"@marca": RAIZ / "assets" / "logo" / "draconic-mark.svg"}


def ler_proprio(chave: str) -> tuple[str, str]:
    """Devolve (viewBox quadrado, conteúdo) de um SVG próprio de uma cor só."""
    texto = PROPRIOS[chave].read_text(encoding="utf-8")
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', texto).group(1).split()]
    lado = max(vb[2], vb[3])
    x = vb[0] - (lado - vb[2]) / 2
    y = vb[1] - (lado - vb[3]) / 2
    interno = re.search(r"<svg[^>]*>(.*)</svg>", texto, re.S).group(1).strip()
    interno = re.sub(r'\sfill="[^"]*"', "", interno)  # a cor vem do tema
    return f"{x:g} {y:g} {lado:g} {lado:g}", interno


def baixar_phosphor() -> bytes:
    if CACHE.exists():
        dados = CACHE.read_bytes()
    else:
        print(f"baixando {PHOSPHOR_URL}")
        with urllib.request.urlopen(PHOSPHOR_URL) as r:
            dados = r.read()
    soma = hashlib.sha256(dados).hexdigest()
    if soma != PHOSPHOR_SHA256:
        sys.exit(f"SHA-256 do Phosphor não confere: {soma} (esperado {PHOSPHOR_SHA256})")
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_bytes(dados)
    return dados


def ler_svgs(dados: bytes) -> tuple[dict[str, str], str]:
    """Devolve {nome: conteúdo interno do SVG} do peso regular e o texto da licença."""
    import io
    svgs: dict[str, str] = {}
    licenca = ""
    with tarfile.open(fileobj=io.BytesIO(dados), mode="r:gz") as tar:
        for m in tar.getmembers():
            if m.name == "package/LICENSE":
                licenca = tar.extractfile(m).read().decode()
            elif m.name.startswith("package/assets/regular/") and m.name.endswith(".svg"):
                texto = tar.extractfile(m).read().decode()
                interno = re.search(r"<svg[^>]*>(.*)</svg>", texto, re.S)
                if not interno:
                    sys.exit(f"SVG inesperado: {m.name}")
                svgs[Path(m.name).stem] = interno.group(1).strip()
    return svgs, licenca


def ler_mapa() -> list[tuple[str, str, str]]:
    entradas = []
    vistos = set()
    for n, linha in enumerate(MAPA.read_text(encoding="utf-8").splitlines(), 1):
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        partes = linha.split("\t")
        if len(partes) != 3:
            sys.exit(f"{MAPA.name}:{n}: precisa de 3 colunas separadas por TAB")
        nome, phosphor, ctx = (p.strip() for p in partes)
        if ctx not in CONTEXTOS:
            sys.exit(f"{MAPA.name}:{n}: contexto desconhecido '{ctx}'")
        if nome in vistos:
            sys.exit(f"{MAPA.name}:{n}: nome repetido '{nome}'")
        vistos.add(nome)
        entradas.append((nome, phosphor, ctx))
    return entradas


def main() -> None:
    svgs, licenca = ler_svgs(baixar_phosphor())
    entradas = ler_mapa()
    faltando = sorted({p for _, p, _ in entradas
                       if p not in svgs and p not in PROPRIOS})
    if faltando:
        sys.exit("Ícones que não existem no Phosphor nem em PROPRIOS: " + ", ".join(faltando))

    if SAIDA.exists():
        shutil.rmtree(SAIDA)
    usados = set()
    for nome, phosphor, ctx in entradas:
        pasta = SAIDA / "scalable" / ctx
        pasta.mkdir(parents=True, exist_ok=True)
        if phosphor in PROPRIOS:
            viewbox, conteudo = ler_proprio(phosphor)
        else:
            viewbox, conteudo = VIEWBOX_PHOSPHOR, svgs[phosphor]
        svg = MODELO.format(viewbox=viewbox, cor=COR_PADRAO, conteudo=conteudo)
        for arquivo in (f"{nome}.svg", f"{nome}-symbolic.svg"):
            if nome.endswith("-symbolic") and arquivo.endswith("-symbolic-symbolic.svg"):
                continue
            (pasta / arquivo).write_text(svg, encoding="utf-8")
        usados.add(ctx)

    dirs = [f"scalable/{c}" for c in sorted(usados)]
    linhas = [
        "[Icon Theme]",
        "Name=Draconic",
        f"Comment=Ícones do Draconic, a partir do Phosphor {PHOSPHOR_VERSAO} (MIT)",
        "Inherits=breeze,hicolor",
        "Example=folder",
        "FollowsColorScheme=true",
        "Directories=" + ",".join(dirs),
        "",
    ]
    for d in dirs:
        linhas += [f"[{d}]", "Size=16", "MinSize=8", "MaxSize=512",
                   "Type=Scalable", f"Context={CONTEXTOS[d.split('/')[1]]}", ""]
    (SAIDA / "index.theme").write_text("\n".join(linhas), encoding="utf-8")
    (SAIDA / "LICENSE-Phosphor.txt").write_text(licenca, encoding="utf-8")

    total = sum(1 for _ in SAIDA.rglob("*.svg"))
    print(f"tema gerado em {SAIDA.relative_to(RAIZ)}: {len(entradas)} nomes, {total} arquivos SVG")


if __name__ == "__main__":
    main()
