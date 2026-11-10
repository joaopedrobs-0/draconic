# Prompt para começar a construir

Abra o Claude Code dentro da pasta deste repositório (depois de `git clone`) e cole o texto abaixo.

---

Você vai construir o **Draconic**, meu sistema operacional baseado no Fedora Kinoite (KDE Plasma 6). Este repositório já tem todo o design pronto.

Antes de qualquer código:
1. Leia o `CLAUDE.md` inteiro e siga as regras dele.
2. Leia `docs/design-system.md` e `docs/telas.md`.
3. Abra as imagens em `design/telas/` (comece por `Main.png`, `Componentes.png` e `Busca.png`) para entender como o sistema tem que ficar.
4. Confira a documentação atual do BlueBuild, do Fedora Atomic e do KDE Plasma 6 para o que for usar. Não confie de memória em nomes de pacotes, opções ou formato de arquivos.

Depois me mostre, em português e curto:
- A estrutura de pastas que você propõe para o repositório (recipe do BlueBuild, `files/`, temas, scripts).
- O plano da **Fase 1** (imagem base): o que vai criar, quais comandos eu vou rodar e como eu sei que funcionou.
- O que eu preciso fazer manualmente (por exemplo: gerar a chave do cosign e colocar nos *secrets* do GitHub, criar a VM).

Meu computador é Ubuntu x86_64 (i3, 16 GB de RAM, RTX 3050). Não mexa no sistema dele: os testes são numa VM com Fedora Kinoite, onde eu faço `rpm-ostree rebase` para a imagem do Draconic.

Espere meu ok antes de começar a Fase 1. Depois de cada fase, pare e me diga como testar.
