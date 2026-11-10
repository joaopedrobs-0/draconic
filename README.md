# Draconic

Sistema operacional para PC baseado no **Fedora Kinoite** (Fedora Atomic com KDE Plasma 6). A ideia é ter a ergonomia do macOS — barra superior com menu global, dock, busca com Meta+Espaço, atalhos consistentes — com identidade própria e sem visual genérico.

> Status: **fase de design.** As telas estão prontas como protótipo; a imagem do sistema ainda não foi construída.

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `assets/logo/` | `draconic-logo.svg` (logo completo, para boot, login e "Sobre") e `draconic-mark.svg` (marca reduzida em uma cor, para 32 px ou menos) |
| `docs/design-system.md` | Regras visuais: cores por função, tipografia, espaçamento, componentes e o que o sistema não faz |
| `docs/prompt-construcao.md` | Prompt para uma IA construir a imagem com BlueBuild, fase por fase |

## Decisões principais

- **Base:** Fedora Kinoite, imagem construída com BlueBuild e instalada com `rpm-ostree rebase`.
- **Arquiteturas:** x86_64 (com variante NVIDIA) e aarch64 (máquinas virtuais em Mac com chip Apple).
- **Fontes:** IBM Plex Sans e IBM Plex Mono na interface; Michroma só no nome "DRACONIC".
- **Ícones:** Phosphor, peso regular, sem misturar com outras famílias.
- **Cor de destaque:** âmbar queimado (`#C8873A` no claro, `#D99A4E` no escuro).
- **Temas:** claro e escuro, a partir dos mesmos tokens.

## Protótipo das telas

Área de trabalho, instalador (4 etapas), Busca, Configurações, boot, login, folha de componentes e site de download estão no canvas de design do projeto (privado).

## Aviso

Draconic é um projeto independente baseado no Fedora. Não é um produto oficial do Projeto Fedora.
