#!/usr/bin/env bash
# Dá a identidade do Draconic ao sistema, editando /usr/lib/os-release.
#
# O que muda: nome, nome completo, variante, logo, links e nome padrão do computador.
# O que NÃO muda de propósito: ID=fedora e VERSION_ID. Ferramentas do Fedora
# (rpm-ostree, dnf, flatpak, toolbox) usam esses dois para saber a versão base.
set -euo pipefail

ARQUIVO=/usr/lib/os-release

# No Kinoite, /usr/lib/os-release é um link para os-release.kinoite.
# Copiamos o conteúdo real e gravamos um arquivo comum no lugar do link.
ORIGINAL="$(readlink -f "$ARQUIVO")"
TEMP="$(mktemp)"
cp "$ORIGINAL" "$TEMP"

VERSION_ID="$(. "$TEMP" && echo "$VERSION_ID")"
REPO="https://github.com/joaopedrobs-0/draconic"

# Troca a linha CHAVE=... se existir; se não existir, acrescenta no fim.
definir() {
    local chave="$1" valor="$2"
    if grep -q "^${chave}=" "$TEMP"; then
        sed -i "s|^${chave}=.*|${chave}=${valor}|" "$TEMP"
    else
        echo "${chave}=${valor}" >> "$TEMP"
    fi
}

definir NAME              '"Draconic"'
definir PRETTY_NAME       "\"Draconic (baseado no Fedora Linux ${VERSION_ID})\""
definir VERSION           "\"${VERSION_ID}\""
definir VARIANT           '"Draconic"'
definir VARIANT_ID        'draconic'
definir LOGO              'draconic-logo'
definir ANSI_COLOR        '"0;38;2;200;135;58"'
definir DEFAULT_HOSTNAME  '"draconic-pc"'
definir HOME_URL          "\"${REPO}\""
definir DOCUMENTATION_URL "\"${REPO}\""
definir SUPPORT_URL       "\"${REPO}/issues\""
definir BUG_REPORT_URL    "\"${REPO}/issues\""

rm -f "$ARQUIVO"
install -m 0644 "$TEMP" "$ARQUIVO"
rm -f "$TEMP"

# Confere o resultado no log do build.
echo "---- /usr/lib/os-release do Draconic ----"
cat "$ARQUIVO"
grep -q '^NAME="Draconic"$' "$ARQUIVO"
grep -q '^ID=fedora$' "$ARQUIVO"
