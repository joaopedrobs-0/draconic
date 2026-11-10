# Prompt para construir o Draconic

Cole o texto abaixo em uma IA de programação junto com este repositório.

---

Você vai me ajudar a construir o **Draconic**, uma distribuição Linux baseada no Fedora. Eu entendo o básico; escreva os arquivos completos, explique cada passo em português e diga exatamente quais comandos rodar.

## Base técnica
- Fedora Kinoite (KDE Plasma 6), versão estável mais recente.
- Imagem construída com BlueBuild (`recipe.yml` + GitHub Actions), publicada no GitHub Container Registry e instalada com `rpm-ostree rebase`. Depois, gerar a ISO instalável.
- Arquiteturas: x86_64 (com variante que já traz o driver NVIDIA) e aarch64 (para testar em VM no VMware Fusion num Mac M2). Diga quais limitações existem em cada uma.
- Toda customização fica versionada neste repositório; nada de "clique aqui nas configurações".

## Regras visuais
Siga `docs/design-system.md` à risca: tokens de cor, tipografia (IBM Plex Sans/Mono, Michroma só no nome), escala de espaço, ícones Phosphor e a lista do que o sistema não faz. Logo em `assets/logo/`.

## Comportamento (estilo macOS)
- Barra superior fina com menu global, bandeja e relógio.
- Dock inferior centralizada, sem rótulos, com indicador de app aberto.
- Busca centralizada em Meta+Espaço (KRunner) com resultados agrupados.
- Atalhos: Meta+Espaço busca, Meta+Q fecha app, Meta+W fecha janela, Meta+Tab alterna apps, Meta+setas encaixam janelas, Meta+1..9 áreas de trabalho, Meta+Enter terminal, Meta+E arquivos, Meta+Shift+4 captura de área, Meta+L bloqueia. Verifique conflitos com o Plasma.
- Animações do KWin de 150–250 ms, sem efeito elástico; tudo respeita "Reduzir movimento".
- Tema Plymouth com o logo completo e o pedido de senha do disco; tela de login (SDDM) com relógio, usuário e botões Suspender/Reiniciar/Desligar.

## Como trabalhar comigo
1. Antes do código, mostre a estrutura de pastas e as decisões principais. Espere eu aprovar.
2. Construa em fases, cada uma testável na VM:
   1. Imagem base funcionando (boot + rebase).
   2. Tema, fontes, ícones, layout (barra + dock).
   3. Atalhos e busca.
   4. Animações.
   5. Plymouth, SDDM, logo e ISO.
3. Em cada fase: arquivos completos, comandos exatos e como verificar.
4. Se algo não for possível ou você não tiver certeza de que um pacote ou extensão existe, diga em vez de inventar.
