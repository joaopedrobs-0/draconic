# Catálogo de telas

Cada tela tem imagem em `design/telas/` e código de referência em `design/prototipo/` (mesmo nome). As versões `-escuro` mostram o tema escuro.

A coluna **Como fazer no Plasma** é um ponto de partida, não uma certeza: confira a documentação atual do KDE antes de implementar. **Viável agora** = dá para fazer com o que o Plasma 6 já oferece + configuração/tema; **Precisa de código** = widget QML, script do KWin ou app próprio; **Meta** = objetivo de longo prazo.

## Sistema

| Tela | Imagem | Como fazer no Plasma | Status |
|---|---|---|---|
| Área de trabalho | `Main.png`, `Main-escuro.png` | Painel superior (widget de menu global + bandeja + relógio); painel inferior flutuante com gerenciador de tarefas só ícones; esquema de cores; decoração de janela com botões à direita | Viável agora |
| Busca (Meta+Espaço) | `Busca.png`, `Busca-escuro.png` | KRunner centralizado; resultados agrupados por tipo | Viável agora (aparência fina pode precisar de tema) |
| Central de controle | `Central.png` | Não existe pronta no Plasma: widget QML próprio reunindo Wi-Fi, Bluetooth, Não perturbe, brilho, som e mídia | Precisa de código |
| Notificações | `Central.png` | Notificações do Plasma com estilo do tema; botão de ação âmbar | Viável agora |
| Visão geral (Meta+Tab) | `Visao-geral.png` | Efeito Overview do KWin com faixa de áreas de trabalho; remapear atalho | Viável agora |
| Menu da barra | `Menus.png` | Menu global + estilo de menu do tema | Viável agora |
| Diálogo destrutivo | `Dialogo.png` | Regra para os apps próprios; nos apps KDE, segue o padrão deles | Parcial |
| Boot | `Boot.png` | Tema Plymouth (script) com logo completo e pedido de senha do LUKS | Viável agora |
| Login | `Login.png` | Tema SDDM em QML | Viável agora |
| Bloqueio | `Bloqueio.png` | Tema da tela de bloqueio do Plasma (QML) | Viável agora |
| Movimento | `Movimento.png` | Durações dos efeitos do KWin; curvas customizadas podem exigir script/efeito próprio | Parcial |

## Configurações

| Tela | Imagem | Como fazer | Status |
|---|---|---|---|
| Aparência | `Configuracoes.png`, `Configuracoes-escuro.png` | System Settings do KDE com o tema aplicado; o layout exato é meta | Parcial |
| Teclado e atalhos | `Config-Teclado.png` | Atalhos pré-configurados via arquivos em `/etc/skel` (kglobalshortcutsrc) | Viável agora |
| Wi-Fi | `Config-WiFi.png` | Módulo de rede do Plasma com o tema | Parcial |
| Sobre | `Config-Sobre.png` | `os-release`, logo e "Sobre este sistema" do KDE (kcm-about-distro) | Viável agora |

## Apps

| App | Imagem | Como fazer | Status |
|---|---|---|---|
| Arquivos | `Main.png`, `Arquivos-previa.png` | Dolphin com tema, colunas e barra lateral configuradas; pré-visualização com Espaço depende de ferramenta extra | Parcial |
| Terminal | `Terminal.png` | Konsole com perfil (IBM Plex Mono, cores do terminal, prompt âmbar) | Viável agora |
| Editor de texto | `Editor.png`, `Editor-escuro.png` | Kate/KWrite com esquema de cores; o layout exato é meta | Parcial |
| Música | `Musica.png`, `Musica-escuro.png` | Elisa (KDE) com tema, ou app próprio | Parcial |
| Monitor do sistema | `Monitor.png`, `Monitor-escuro.png` | Plasma System Monitor com página customizada | Parcial |

## Instalação e primeiro uso

| Tela | Imagem | Como fazer | Status |
|---|---|---|---|
| Instalador (4 etapas) | `Instalador-01.png` … `Instalador-04.png` | O Fedora usa o Anaconda; dá para trocar marca e textos. O layout desenhado exige instalador próprio (avaliar Calamares, que aceita tema em QML) | Meta |
| Primeiro boot | `Primeiro-boot.png` | Assistente de configuração inicial do KDE, se disponível na versão do Plasma, ou o do Anaconda | Parcial |

## Base

| Tela | Imagem | Uso |
|---|---|---|
| Tokens e componentes | `Componentes.png`, `Componentes-escuro.png` | Fonte da verdade para cores, tipos, espaços e estados |
| Site de download | `Site.png` | Página do projeto (fora do sistema) |
