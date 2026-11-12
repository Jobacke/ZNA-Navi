# ZNA-Navi

Ein Tipp – Waze navigiert zur Notaufnahme.

PWA für iPhone: Ziele (z. B. ZNA-Liste aus what3words inkl. Koordinaten) importieren und per Waze-Deeplink direkt die Navigation starten. Optional Sortierung nach Entfernung.

**Installation:** https://zna.vjbackhaus.de/ in Safari öffnen → Teilen → „Zum Home-Bildschirm“.

Die Zielliste steht in `zna.json` – ändern per Stift-Symbol auf GitHub, die Handys bieten das Update beim nächsten Öffnen an. Adresssuche über OpenStreetMap (Photon/Nominatim).

## Versionen

Die Version steht an drei Stellen und wird bei jeder Änderung gemeinsam hochgezählt:
- `index.html` → `APP_VERSION` / `APP_DATE`
- `version.json` → `version` (löst auf den Handys den Hinweis „Neue App-Version verfügbar“ aus)
- `sw.js` → `CACHE`

| Version | Datum | Änderungen |
|---|---|---|
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
