#!/usr/bin/env bash
# Gera os caches de fontes e ícones dentro da imagem.
# No Fedora Atomic o /usr é somente leitura no sistema instalado, então o
# cache do sistema precisa ser criado aqui, na construção.
set -euo pipefail

# Fontes: IBM Plex (pacotes) e Michroma (files/system/usr/share/fonts/michroma).
fc-cache --system-only --force
echo "---- fontes do Draconic ----"
fc-list : family | grep -E "IBM Plex (Sans|Mono)$|Michroma" | sort -u
fc-list : family | grep -qx "IBM Plex Sans"
fc-list : family | grep -qx "Michroma"

# Ícones: o KDE não precisa deste cache, mas apps GTK usam se existir.
if command -v gtk-update-icon-cache >/dev/null; then
    gtk-update-icon-cache --force --quiet /usr/share/icons/Draconic
else
    echo "gtk-update-icon-cache não está na imagem; pulando (o KDE não precisa)"
fi
