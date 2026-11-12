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
| 1.3.1 | 2026-11-12 | Kopfzeile bleibt beim Scrollen fest oben (auch unter Uhrzeit/Dynamic Island) |
| 1.3.0 | 2026-11-12 | „Zurück zur Liste“ bei Adresssuche; nach Speichern und nach Rückkehr aus Waze automatisch zur Liste; gespeicherte Adressen landen in Gruppe „Eigene“ |
| 1.2.1 | 2026-11-12 | Updates kommen sofort an (Cache-Prüfung im Service Worker) |
| 1.2.0 | 2026-11-12 | Versionsnummer in der App, Update-Hinweis bei neuer Version |
| 1.1.0 | 2026-11-12 | Serverliste `zna.json`, Adresssuche mit Sprache, Siri-Parameter `?q=` |
| 1.0.0 | 2026-11-12 | Erste Version: Ziele, Import aus what3words, Waze-Start, Entfernung |
