# Draconic — instruções para o agente

Este repositório é o **Draconic**, um sistema operacional baseado no **Fedora Kinoite** (Fedora Atomic + KDE Plasma 6). O design já está pronto; o trabalho agora é transformar o design em um sistema que liga, instala e se parece com as telas.

Leia, nesta ordem, antes de escrever qualquer coisa:

1. `docs/design-system.md` — as regras visuais. São obrigatórias.
2. `docs/telas.md` — o que cada tela é, como mapeia para o KDE Plasma e o que é viável agora.
3. `design/telas/*.png` — as imagens de referência de todas as telas (claro e escuro).
4. `design/prototipo/*.dc.html` — o código das telas. Use para tirar **valores exatos** (cores, tamanhos, espaçamentos, textos). Não é código para rodar no sistema.

## Quem é o dono e como falar com ele

- O dono entende o básico de programação e trabalha com vibe coding. Explique em **português do Brasil**, direto, sem jargão desnecessário.
- Sempre diga **exatamente** quais comandos rodar e o que ele deve ver se deu certo.
- Escreva arquivos **completos**, nunca "o resto continua igual".
- Se algo não for possível no Plasma/Fedora, ou você não tiver certeza de que um pacote, opção ou API existe, **diga isso** em vez de inventar. Confira a documentação atual (Fedora, KDE, BlueBuild) antes de afirmar.

## Ambiente

- Máquina de desenvolvimento: **Ubuntu, x86_64**, Intel Core i3, 16 GB de RAM, NVIDIA RTX 3050 6 GB. É o computador do dia a dia — **nunca** instale o Draconic por cima dele, nunca mexa em partições, bootloader ou drivers do host.
- Testes: em **máquina virtual** (QEMU/KVM com virt-manager ou GNOME Boxes no Ubuntu). Instale o Fedora Kinoite na VM e faça `rpm-ostree rebase` para a imagem do Draconic.
- Também existe um MacBook Air M2 (VMware Fusion) para testar a versão aarch64 depois.
- Construção da imagem: **BlueBuild** + **GitHub Actions**, publicando em `ghcr.io/<dono>/draconic`. Cosign para assinar. Para testar rápido localmente, `podman` no Ubuntu é aceitável.

## Regras de trabalho

- Trabalhe **em fases**, cada uma testável na VM, e pare ao fim de cada fase para o dono testar.
- Antes de cada fase, mostre o plano curto: arquivos que vai criar/alterar e por quê. Espere um "ok".
- Commits pequenos, mensagem em português dizendo o que mudou.
- Nenhuma customização "clique aqui nas configurações": tudo versionado no repositório (`/etc/skel`, pacotes de look-and-feel, configs em `files/`).
- Ações destrutivas (apagar arquivos, reescrever histórico, `git push --force`, qualquer coisa no host fora do repositório): **pergunte antes**.

## Fases

1. **Imagem base** — recipe do BlueBuild a partir do Kinoite, workflow do GitHub Actions, assinatura, `os-release` com `NAME="Draconic"`. Teste: VM liga depois do rebase e `rpm-ostree status` mostra a imagem do Draconic.
2. **Fundação visual** — fontes (IBM Plex Sans/Mono; Michroma só para o nome), esquema de cores claro e escuro a partir dos tokens, cor de destaque âmbar, cantos e espaçamentos. Tema de ícones a partir do **Phosphor** (MIT) mapeado para os nomes freedesktop, herdando do Breeze o que faltar.
3. **Layout** — barra superior com menu global (painel do Plasma + widget de menu global), dock inferior flutuante só com ícones, papel de parede liso.
4. **Busca e atalhos** — KRunner centralizado em Meta+Espaço; toda a tabela de atalhos de `docs/design-system.md`. Verifique conflitos com os atalhos padrão do Plasma.
5. **Movimento** — efeitos do KWin com as durações e curvas da especificação; tudo respeitando "Reduzir movimento".
6. **Boot e login** — tema Plymouth (logo completo + pedido de senha do LUKS) e tema SDDM (relógio, usuário, senha, Suspender/Reiniciar/Desligar).
7. **Apps e telas restantes** — central de controle, Configurações e o que mais for viável, na ordem de `docs/telas.md`.
8. **ISO** — gerar a ISO instalável. O instalador desenhado é a meta; a primeira ISO pode usar o instalador padrão com a marca do Draconic. Explique as opções antes de decidir.

## O que nunca fazer

- Usar logos ou marcas do Fedora, do KDE ou da Apple como se fossem nossas. Crédito em texto ("Baseado no Fedora") é ok.
- Copiar temas prontos que imitam o macOS (WhiteSur e similares).
- Adicionar enfeite que não está no design: gradientes coloridos, neon, brilhos, vidro fora dos lugares permitidos, emoji na interface.
- Inventar números, versões ou nomes de pacote.
