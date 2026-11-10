# Sistema de design do Draconic

A qualidade visual sai de poucas regras aplicadas sempre, não de enfeite. Nenhum app inventa cor, tamanho, espaço ou ícone próprio: tudo vem daqui. Referências visuais: `design/telas/Componentes.png` e `design/telas/Componentes-escuro.png`.

## Princípios

- **Não "parecer Apple"**: ter a ergonomia do macOS (menu global, dock, busca, atalhos consistentes) com identidade própria.
- Ordem para criar hierarquia: **posição → espaço → tipografia → forma → cor → efeito**. Quanto antes o problema se resolve nessa ordem, menos decorada fica a tela.
- Conteúdo real: tabelas com dados de verdade, saídas de comando de verdade. Nada de números inventados para enfeitar.
- Desktop não é celular grande: menus, atalhos, hover, seleção múltipla, arrastar e soltar, menu de contexto, desfazer.
- Os apps do sistema (Arquivos, Configurações, Terminal, Editor, Música) são o teste do sistema de design.

## Cores (tokens por função)

| Token | Claro | Escuro | Uso |
|---|---|---|---|
| `wallpaper` | `#B7B9BC` | `#3A3B3D` | papel de parede padrão (liso; o usuário troca) |
| `text.primary` | `#1A1A1A` | `#EDEDED` | texto principal |
| `text.secondary` | `#55555A` | `#A6A6AB` | datas, tamanhos, rótulos |
| `surface.window` | `#FFFFFF` | `#1E1E1F` | fundo do conteúdo |
| `surface.chrome` | `#F6F6F5` | `#262628` | barras de ferramentas e laterais |
| `surface.menubar` | `#F3F3F2` | `#262628` | barra superior |
| `surface.elevated` | `#FFFFFF` | `#2E2E30` | menus e popovers |
| `fill` | `#E9E9EA` | `#333336` | controles segmentados, trilhos |
| `border.separator` | `#E2E2E3` | `#38383B` | divisões |
| `border.window` | `#C4C4C7` | `#4A4A4E` | borda de janela |
| `border.menubar` | `#CFCFD1` | `#38383B` | linha embaixo da barra superior |
| `control.border` | `#B8B8BC` | `#55555A` | borda de campos e botões |
| `accent` | `#C8873A` | `#D99A4E` | botão principal, seleção, foco, prompt do terminal |
| `on-accent` | `#1A1A1A` | `#1A1A1A` | texto sobre o destaque |
| `selection.active` | `#C8873A` sólido, texto `#1A1A1A` | `#D99A4E` sólido, texto `#1A1A1A` | linha/item selecionado em listas e menus |
| `focus.ring` | âmbar 55% | âmbar 60% | anel de foco de 3 px |
| `status.success` | `#2F6B3A` | `#6FBF7A` | sucesso |
| `status.warning` | `#8A5320` | `#E0A867` | aviso |
| `status.error` | `#B3261E` | `#F2867E` | erro e ações destrutivas |
| terminal | `#161616` fundo, `#D6D6D9` texto | igual | o terminal é escuro nos dois temas |

Texto com contraste de pelo menos 4,5:1. Estado nunca é indicado só por cor.

**Seleção hoje × meta.** A cor de seleção do esquema é o âmbar sólido com texto escuro, igual ao botão principal. Como ela aparece depende de quem desenha:

- **Listas do Kirigami** (barra lateral das Configurações, apps QML): âmbar sólido com texto `#1A1A1A`.
- **Widgets Qt com o estilo Breeze** (listas e grade do Dolphin, menus): o Breeze desenha a seleção e o destaque do menu como âmbar translúcido com borda âmbar. É comportamento fixo do Breeze, e já fica perto da meta.

A meta é a linha de lista em âmbar 20% (claro) / 26% (escuro), como em `Main.png`, e o item de menu em âmbar sólido, como em `Componentes.png`. O controle exato fica para quando houver um tema Kvantum ou um estilo de widgets próprio.

## Tipografia

| Estilo | Fonte | Tamanho / peso |
|---|---|---|
| display | Michroma | 22–28 — **só** o nome "DRACONIC" e títulos do instalador |
| title | IBM Plex Sans | 22 / 600 |
| heading | IBM Plex Sans | 15 / 600 |
| body | IBM Plex Sans | 13 / 400 (padrão da interface) |
| label | IBM Plex Sans | 12 / 500 |
| caption | IBM Plex Sans | 11 / 400 |
| mono | IBM Plex Mono | 12–13 / 400 |

IBM Plex e Michroma são livres (OFL). Michroma substitui a Nasalization, que exige licença paga para ser embutida.

## Espaço e forma

- Espaçamento só em **4, 8, 12, 16, 24, 32, 48** px.
- Cantos (meta): **6** controles · **8** menus, painéis e grupos · **12** janelas · **16** dock e Busca.
  - **Hoje vale o raio do Breeze.** O Plasma não permite configurar o raio dos cantos dos controles nem das janelas. Os valores acima são a meta, para quando houver um tema Kvantum ou um estilo próprio. Painéis e dock (Plasma) podem seguir a meta antes, porque usam o tema do Plasma.
- Altura de controles: 24 (compacto), 28 (barra de ferramentas), 32 (padrão), 40 (instalador).
- Barra superior: 28 px. Barra de título/ferramentas: 48 px. Barra de status: 28 px.

## Componentes

Todo controle tem os estados desenhados: normal, hover, pressionado, foco, desabilitado e, quando couber, selecionado, carregando, erro.

- **Botões**: um principal por tela (fundo âmbar, texto escuro), à direita, com verbo. "Voltar"/"Cancelar" à esquerda dele.
- **Destrutivo**: nunca é o principal. Texto vermelho em botão padrão ("Apagar disco e instalar", "Esvaziar", "Encerrar…"). Em diálogo de confirmação, o principal/padrão é **Cancelar**.
- "…" no fim do rótulo quando o botão abre outra tela ou pede mais dados.
- Ajuda: botão redondo "?" no canto oposto aos botões de confirmar.
- Botões só com ícone sempre têm nome acessível.
- Controles de janela (minimizar, maximizar, fechar) ficam **à direita**, ícones de traço, sem bolinhas coloridas.

## Ícones

**Phosphor**, peso regular, grade de 256, uma família só. Nunca misturar com outra. Tamanhos: 12, 14, 16 (interface), 24–28 (dock), 48 (grade de arquivos).

## Logo

- `assets/logo/draconic-logo.svg` — completo, com o cinza. Boot, login, "Sobre", instalador.
- `assets/logo/draconic-mark.svg` — reduzido, uma cor, sem olho/narina. Para 32 px ou menos (barra superior, abas).
- No fundo escuro: círculo claro (`#EDEDED`), crescente `#5A5A5F`.

## Efeitos

Todo efeito responde "o que esta camada significa?".

- **Vidro** (desfoque + transparência): só no que flutua sobre as janelas — dock, Busca, central de controle, menus e notificações. Nunca vidro sobre vidro. Barra superior e janelas são sólidas.
  - Dock (valores de `design/prototipo/Main.dc.html`): fundo `#F4F4F5` a 55% (claro) / `#28282A` a 60% (escuro), contorno de 1 px branco a 70% (claro) / 12% (escuro), cantos de 16 px, margem de 8 px até a borda da tela, botões de 48×52 px com ícone de 28 px.
- **Sombra**: janela acima de janela. Janela ativa com sombra maior que a inativa.
- **Escurecimento (scrim)**: só quando a atenção está bloqueada (diálogo sobre uma janela, visão geral).
- "Reduzir transparência" troca todo vidro por cor sólida.

## Movimento

Cada animação mostra de onde algo veio e para onde foi. Nenhuma passa de 250 ms, todas podem ser interrompidas, nenhuma bloqueia teclado ou mouse. Referência: `design/telas/Movimento.png`.

| Momento | O que se mexe | Duração | Curva | Com "Reduzir movimento" |
|---|---|---|---|---|
| Abrir janela | cresce de 96% para 100% e aparece | 180 ms | desacelera | só aparece, 120 ms |
| Fechar janela | encolhe para 96% e some | 140 ms | acelera | só some, 100 ms |
| Minimizar | encolhe em direção ao ícone no dock | 220 ms | suave | some no lugar |
| Trocar de área de trabalho | tudo desliza para o lado | 250 ms | suave | fade, 100 ms |
| Abrir Busca / central | desce 8 px do topo e aparece | 160 ms | desacelera | só aparece |
| Notificação | entra 16 px pela direita | 200 ms | desacelera | só aparece |
| Menu | só opacidade | 80 ms | linear | igual |
| Visão geral | cada janela vai do seu lugar para a grade | 250 ms | suave | grade com fade |

Curvas: desacelera `cubic-bezier(0.2, 0, 0, 1)`, acelera `cubic-bezier(0.4, 0, 1, 1)`, suave `cubic-bezier(0.4, 0, 0.2, 1)`. Sem efeito elástico nem quique.

## Atalhos

A tecla **Meta** (a do logo do Windows) é a base de tudo.

| Ação | Atalho |
|---|---|
| Busca | Meta+Espaço |
| Visão geral das janelas | Meta+Tab |
| Central de controle | Meta+A |
| Captura de uma área | Meta+Shift+S |
| Bloquear a tela | Meta+L |
| Fechar janela | Meta+W |
| Fechar o app | Meta+Q |
| Encaixar à esquerda / direita | Meta+← / Meta+→ |
| Maximizar | Meta+↑ |
| Minimizar | Meta+M |
| Ir para a área 1 a 9 | Meta+1…9 |
| Levar a janela para a área | Meta+Shift+1…9 |
| Terminal | Meta+Enter |
| Arquivos | Meta+E |
| Pré-visualizar arquivo selecionado | Espaço (no Arquivos) |

**Hoje no sistema** (`files/system/etc/skel/.config/kglobalshortcutsrc`, só para usuários novos):
- A captura de área era `Meta+Shift+4`, o que conflitava com "Levar a janela para a área 4". Decisão do dono (10/11/2026): `Meta+Shift+4` leva a janela para a área 4 e a captura passou para `Meta+Shift+S` (`Meta+Shift+Print` também funciona).
- `Meta+Q` fecha a janela (o KDE não tem "fechar o app" genérico).
- `Meta+A` está livre até existir a Central de controle (Fase 7).
- Espaço no Arquivos (pré-visualizar) ainda não existe.
- Atalhos com Shift + número usam o símbolo (`Meta+$`); a área 6 usa `Meta+^`, porque no ABNT2 o Shift+6 é tecla morta.

## O que o Draconic não faz

- Esferas, brilhos e anéis decorativos; letras gigantes vazadas no fundo.
- Rótulos em MAIÚSCULAS ESPAÇADAS.
- Números inventados — só dado real.
- Gradientes coloridos, neon, emoji na interface.
- Frases de efeito — botões dizem o que fazem.
- Animação sem uma ação do usuário por trás.
- Temas que imitam o macOS (WhiteSur e similares) e ícones "bala de goma".
