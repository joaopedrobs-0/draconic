# Sistema de design do Draconic

A qualidade visual tem que sair de poucas regras aplicadas sempre, não de enfeite. Nenhum app inventa cor, tamanho, espaço ou ícone próprio: tudo vem daqui.

## Ordem para criar hierarquia

posição → espaço → tipografia → forma → cor → efeito

Quanto mais cedo nessa ordem o problema se resolve, menos decorada fica a tela.

## Cores (tokens por função)

| Token | Claro | Escuro | Uso |
|---|---|---|---|
| `text.primary` | `#1A1A1A` | `#EDEDED` | texto principal |
| `text.secondary` | `#55555A` | `#A6A6AB` | datas, tamanhos, rótulos |
| `surface.window` | `#FFFFFF` | `#1E1E1F` | fundo do conteúdo |
| `surface.chrome` | `#F3F3F2` | `#262628` | barras e laterais |
| `surface.elevated` | `#FFFFFF` | `#2E2E30` | menus e popovers |
| `border.separator` | `#E2E2E3` | `#38383B` | divisões |
| `control.border` | `#B8B8BC` | `#55555A` | borda de campos e botões |
| `accent` | `#C8873A` | `#D99A4E` | botão principal, seleção, foco |
| `on-accent` | `#1A1A1A` | `#1A1A1A` | texto sobre o destaque |
| `selection.active` | âmbar 20% | âmbar 26% | linha selecionada |
| `status.success` | `#2F6B3A` | `#6FBF7A` | sucesso |
| `status.warning` | `#8A5320` | `#E0A867` | aviso |
| `status.error` | `#B3261E` | `#F2867E` | erro e ações destrutivas |

Texto sempre com contraste de pelo menos 4,5:1. Estado nunca é indicado só por cor.

## Tipografia

| Estilo | Fonte | Tamanho/peso |
|---|---|---|
| display | Michroma | 22 — só o nome do sistema e títulos do instalador |
| title | IBM Plex Sans | 22 / 600 |
| heading | IBM Plex Sans | 15 / 600 |
| body | IBM Plex Sans | 13 / 400 |
| label | IBM Plex Sans | 12 / 500 |
| caption | IBM Plex Sans | 11 / 400 |
| mono | IBM Plex Mono | 12 / 400 |

## Espaço e cantos

Espaçamento só nestes valores: 4, 8, 12, 16, 24, 32, 48 px.
Cantos: 6 px controles, 8 px menus e painéis, 12 px janelas.

## Componentes

Todo controle tem os estados desenhados: normal, hover, pressionado, foco, desabilitado (e, quando couber, selecionado, carregando, erro).

- Um botão principal por tela, à direita, com verbo no rótulo. "Voltar"/"Cancelar" à esquerda dele.
- Ação destrutiva nunca é o botão principal: texto vermelho, estilo padrão.
- "…" no fim do rótulo quando o botão abre outra tela.
- Botão de ajuda redondo "?" no canto oposto aos botões de confirmar.
- Todo botão só com ícone tem nome acessível.

## Efeitos

Todo efeito precisa responder "o que esta camada significa?".

- Vidro (desfoque): só no que flutua sobre o conteúdo — dock e Busca. Nunca vidro sobre vidro.
- Sombra: janela acima de janela.
- Movimento: explica de onde algo veio e para onde foi; curto (150–250 ms), pode ser interrompido e respeita "Reduzir movimento".

## Ícones

Phosphor, peso regular, em grade de 256. Nenhuma outra família.

## O que o Draconic não faz

- Esferas, brilhos e anéis decorativos; letras gigantes vazadas no fundo.
- Rótulos em MAIÚSCULAS ESPAÇADAS.
- Números inventados — só dado real.
- Gradientes coloridos, neon, emoji na interface.
- Frases de efeito — botões dizem o que fazem.
- Animação sem uma ação do usuário por trás.
