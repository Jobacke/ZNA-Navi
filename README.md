# ZNA-Navi

Ein Tipp – Waze navigiert zur Notaufnahme.

PWA für iPhone: Ziele (z. B. ZNA-Liste aus what3words inkl. Koordinaten) importieren und per Waze-Deeplink direkt die Navigation starten. Optional Sortierung nach Entfernung.

**Installation:** https://zna.vjbackhaus.de/ in Safari öffnen → Teilen → „Zum Home-Bildschirm“.

Die Zielliste steht in `zna.json` – ändern per Stift-Symbol auf GitHub, die Handys bieten das Update beim nächsten Öffnen an. Adresssuche über OpenStreetMap (Photon/Nominatim).

**Leitstellen:** Knopf „Leitstellen“ zeigt die am Standort zuständige ILS (nach Landkreis, AVBayRDG Anlage 1) und alle 25 ILS Bayerns nach Entfernung. Solange die App offen ist, meldet sie einen Leitstellenwechsel (abschaltbar in den Einstellungen). Daten und Funkgruppen stehen in `leitstellen.json` – ändern in der App (Leitstelle antippen → „Bearbeiten“, mit GitHub-Schlüssel automatisch auf den Server) oder per Stift-Symbol auf GitHub, kein Code nötig.

**Siri „Aktuelle Leitstelle“:** Kurzbefehl in `kurzbefehl/` – sagt die zuständige ILS mit Landkreis und Kurzwahlen an. Am Mac signieren: `bash kurzbefehl/signieren.sh`, dann `Aktuelle Leitstelle.shortcut` doppelklicken. Kurzwahlen liest er live aus `leitstellen.json`; die Zuordnung Landkreis → ILS steht in `leitstellen-index.json` (erzeugt von `python3 kurzbefehl/gen_kurzbefehl.py` – nur nötig, wenn sich Landkreise ändern).

## Versionen

Die Version steht an drei Stellen und wird bei jeder Änderung gemeinsam hochgezählt:
- `index.html` → `APP_VERSION` / `APP_DATE`
- `version.json` → `version` (löst auf den Handys den Hinweis „Neue App-Version verfügbar“ aus)
- `sw.js` → `CACHE`

| Version | Datum | Änderungen |
|---|---|---|
| 1.16.0 | 2026-11-16 | Leitstellen in der App bearbeiten (Name, Sitz, Ort, Funkgruppen, Landkreise): gilt sofort auf dem Handy, mit GitHub-Schlüssel Hochladen von `leitstellen.json` + `leitstellen-index.json` (Siri); RD_Betten_M Kurzwahl 2511 |
| 1.15.0 | 2026-11-16 | Siri-Kurzbefehl „Aktuelle Leitstelle“ (Ansage ILS, Landkreis, Kurzwahlen Rettungsdienst/Bettenkanal) mit `leitstellen-index.json` und Generator in `kurzbefehl/`; Anleitung in den Einstellungen unter „Leitstellen“ |
| 1.14.0 | 2026-11-16 | Neue Rubrik „Leitstellen“ (aus Wissen RD 1.11.0): zuständige ILS am Standort per Landkreis (Nominatim), alle 25 ILS Bayerns nach Luftlinie, Detail mit Sitz/Landkreisen/Funkgruppen, Meldung bei Leitstellenwechsel (Einstellung, Standard an); Daten in `leitstellen.json` |
| 1.13.0 | 2026-11-15 | Mehrere Gruppen gleichzeitig auswählen: Gruppen-Knöpfe schalten an/aus, „Alle“ setzt zurück |
| 1.12.0 | 2026-11-15 | Gruppen-Knöpfe umsortieren: lange drücken, dann nach links/rechts schieben; Reihenfolge wird über den Server auf alle Handys verteilt |
| 1.11.1 | 2026-11-15 | Knopf für Farbschema oben (Auto → Hell → Dunkel), Zahnrad-Symbol für Einstellungen |
| 1.11.0 | 2026-11-15 | Farbschema Hell / Dunkel / Automatisch; Rastersymbol vor der 3-Wort-Adresse |
| 1.10.1 | 2026-11-15 | Kachel-Feinschliff: kleiner Pfeil, what3words bündig darunter, Gruppe bündig unter km |
| 1.10.0 | 2026-11-15 | Einheitliche Kacheln (feste Höhe; Name max. 2 Zeilen, Entfernung rechts oben, Gruppe + Adresse unten) |
| 1.9.2 | 2026-11-15 | Gruppen-Etikett in jeder Zielkachel |
| 1.9.1 | 2026-11-15 | Gruppen-Reiter unter „Fahrt beenden“, „Alle“ vorne, seitlich wischbar mit Verlauf als Hinweis |
| 1.9.0 | 2026-11-15 | Gruppe im Editor als Auswahlliste, „Neue Gruppe“ mit Prüfung auf gleiche/ähnliche Namen |
| 1.8.1 | 2026-11-15 | Knopf „Fahrt beenden“ oben im Kopfbereich, standardmäßig an |
| 1.8.0 | 2026-11-15 | zna.json enthält zusätzlich `index` (Name/eindeutige Wortanfänge → Waze-Link) für den Kurzbefehl „Meine Route“ |
| 1.7.3 | 2026-11-15 | Siri-Kurzbefehl heißt „Meine Route“ |
| 1.7.2 | 2026-11-15 | Siri-Kurzbefehl heißt jetzt „Route“, Frage „Welches Ziel?“ (Anleitung in der App angepasst) |
| 1.7.1 | 2026-11-12 | Mikrofon-Modus Siri-Kurzbefehl; Home-Bildschirm-App überspringt die (von Apple gesperrte) Spracherkennung |
| 1.7.0 | 2026-11-12 | Mikrofon: Live-Text im Suchfeld, Auto-Stopp nach Sprechpause, automatischer Wechsel zum Tastatur-Diktat |
| 1.6.5 | 2026-11-12 | „Extra Abstand“ vergrößert (unter den iOS-Statusleisten-Schleier) |
| 1.6.4 | 2026-11-12 | Kopfbereich und Statusleiste einheitlich schwarz (kein Rand oben) |
| 1.6.3 | 2026-11-12 | Responsive für schmale Displays/Display-Zoom, kein seitliches Überstehen |
| 1.6.2 | 2026-11-12 | Einstellung „Abstand oben“: Automatisch / Extra |
| 1.6.1 | 2026-11-12 | Layout: Kopf steht fest, nur die Liste scrollt (keine Überlappung); Statusleiste deckend; Standort bei jedem Start/Rückkehr |
| 1.6.0 | 2026-11-12 | Knopf „Fahrt beenden“ (Kurzbefehl „Blitzer Ruhe“ → Ruhemodus) |
| 1.5.2 | 2026-11-12 | Navi-Umschalter mit Doppelfunktion: gewählte App erneut antippen öffnet sie |
| 1.5.1 | 2026-11-12 | Blitzer.de-Autostart einstellbar (jedes Öffnen / 30 Min. / 3 Std.), Rückkehr aus Navi-Apps zählt nicht |
| 1.5.0 | 2026-11-12 | Option: Blitzer.de PRO beim ersten Öffnen (nach 3 h Pause) per Kurzbefehl „Warnmodus starten“ |
| 1.4.2 | 2026-11-12 | Icon-Dateien umbenannt (iOS-Cache umgehen) |
| 1.4.1 | 2026-11-12 | Neues App-Icon „Neon-Puls“ |
| 1.4.0 | 2026-11-12 | Umschalter Waze / Google Maps / Apple Karten; Hochladen in die Serverliste per GitHub-Schlüssel mit Abgleich ohne Datenverlust |
| 1.3.1 | 2026-11-12 | Kopfzeile bleibt beim Scrollen fest oben (auch unter Uhrzeit/Dynamic Island) |
| 1.3.0 | 2026-11-12 | „Zurück zur Liste“ bei Adresssuche; nach Speichern und nach Rückkehr aus Waze automatisch zur Liste; gespeicherte Adressen landen in Gruppe „Eigene“ |
| 1.2.1 | 2026-11-12 | Updates kommen sofort an (Cache-Prüfung im Service Worker) |
| 1.2.0 | 2026-11-12 | Versionsnummer in der App, Update-Hinweis bei neuer Version |
| 1.1.0 | 2026-11-12 | Serverliste `zna.json`, Adresssuche mit Sprache, Siri-Parameter `?q=` |
| 1.0.0 | 2026-11-12 | Erste Version: Ziele, Import aus what3words, Waze-Start, Entfernung |
