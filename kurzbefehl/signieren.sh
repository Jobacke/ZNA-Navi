#!/bin/bash
# Signiert den Kurzbefehl „Aktuelle Leitstelle“ auf dem Mac, damit er importiert werden kann.
# Aufruf im Terminal:  cd ~/ZNA-Navi && bash kurzbefehl/signieren.sh
set -e
cd "$(dirname "$0")"
n="Aktuelle Leitstelle"
rm -f "$n.shortcut"
shortcuts sign --mode anyone --input "$n.unsigned.shortcut" --output "$n.shortcut"
echo "✅ $n.shortcut signiert"
open -R "$n.shortcut"
echo "Im Finder doppelt auf „$n.shortcut“ klicken → „Kurzbefehl hinzufügen“."
