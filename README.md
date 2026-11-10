# Draconic &nbsp; [![build](https://github.com/joaopedrobs-0/draconic/actions/workflows/build.yml/badge.svg)](https://github.com/joaopedrobs-0/draconic/actions/workflows/build.yml)

Sistema operacional para PC baseado no **Fedora Kinoite** (Fedora Atomic com KDE Plasma 6). A ergonomia do macOS — barra superior com menu global, dock, busca com Meta+Espaço, atalhos consistentes — com identidade própria e sem visual genérico.

![Área de trabalho do Draconic](design/telas/Main.png)

> Status: **Fase 1 — imagem base.** A imagem já é construída e assinada, mas ainda tem o visual padrão do Kinoite. O visual do Draconic chega nas próximas fases.

## Como instalar (em quem já usa Fedora Kinoite)

> [!WARNING]
> Projeto em construção. Teste numa máquina virtual, não no seu computador principal.

1. Primeiro, rebase para a imagem **sem verificação**. Esse passo instala as chaves e as regras de assinatura do Draconic:
   ```bash
   rpm-ostree rebase ostree-unverified-registry:ghcr.io/joaopedrobs-0/draconic:latest
   ```
2. Reinicie:
   ```bash
   systemctl reboot
   ```
3. Agora rebase para a imagem **assinada**:
   ```bash
   rpm-ostree rebase ostree-image-signed:docker://ghcr.io/joaopedrobs-0/draconic:latest
   ```
4. Reinicie de novo:
   ```bash
   systemctl reboot
   ```

A tag `latest` sempre aponta para o build mais recente. A versão do Fedora fica fixa na receita (`recipes/recipe.yml`), então o sistema nunca pula para um Fedora novo sem querer.

Para voltar ao Kinoite original: `rpm-ostree rollback` volta para a versão anterior instalada.

## Verificar a assinatura

As imagens são assinadas com o [cosign](https://github.com/sigstore/cosign). Com o arquivo `cosign.pub` deste repositório:

```bash
cosign verify --key cosign.pub ghcr.io/joaopedrobs-0/draconic
```

## O que tem aqui

| Caminho | Conteúdo |
|---|---|
| `recipes/recipe.yml` | Receita da imagem (BlueBuild): base, módulos e passos de construção |
| `files/system/` | Arquivos copiados para a raiz (`/`) da imagem |
| `files/scripts/` | Scripts que rodam durante a construção (ex.: `os-release.sh`) |
| `.github/workflows/build.yml` | Build automático no GitHub Actions, todo push e todo dia |
| `cosign.pub` | Chave pública para verificar a assinatura |
| `CLAUDE.md` | Instruções para o agente de programação: ambiente, regras e fases |
| `docs/prompt-construcao.md` | O prompt para colar no Claude Code e começar |
| `docs/design-system.md` | Cores (claro e escuro), tipografia, espaço, componentes, movimento, atalhos e o que o sistema não faz |
| `docs/telas.md` | Catálogo de todas as telas, como cada uma vira Plasma e o que é viável agora |
| `design/telas/` | Imagens de referência de todas as telas |
| `design/prototipo/` | Código das telas (HTML) para tirar valores exatos |
| `assets/logo/` | Logo completo e marca reduzida, em SVG |

## Decisões principais

- **Base:** Fedora Kinoite 45 oficial (`quay.io/fedora/fedora-kinoite`), imagem construída com BlueBuild e instalada com `rpm-ostree rebase`.
- **Arquiteturas:** x86_64 (com variante NVIDIA) e aarch64 (máquinas virtuais em Mac com chip Apple). Por enquanto só x86_64 é construída.
- **Fontes:** IBM Plex Sans e IBM Plex Mono; Michroma só no nome "DRACONIC".
- **Ícones:** Phosphor, peso regular, sem misturar.
- **Cor de destaque:** âmbar queimado (`#C8873A` claro, `#D99A4E` escuro).
- **Temas:** claro e escuro, dos mesmos tokens.

## Algumas telas

| | |
|---|---|
| ![Busca](design/telas/Busca.png) | ![Configurações](design/telas/Configuracoes-escuro.png) |
| ![Central de controle](design/telas/Central.png) | ![Instalador](design/telas/Instalador-01.png) |

## Aviso

Draconic é um projeto independente baseado no Fedora. Não é um produto oficial do Projeto Fedora.
