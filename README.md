# Datenanalyse-Homepage

Kostenlose statische Portfolio-Website mit eingebettetem, serverlosem Bokeh-Dashboard.

## Lokal testen

```bash
python -m http.server 8000
```

Dann http://localhost:8000 öffnen. Zum Neu-Erzeugen des Dashboards:

```bash
pip install -r requirements.txt
python scripts/build_dashboard.py
```

## Veröffentlichen

1. `index.html` öffnen und `DEINE-EMAIL@BEISPIEL.DE` ersetzen.
2. `impressum.html` und `datenschutz.html` durch vollständige, passende Rechtstexte ersetzen.
3. Auf GitHub ein öffentliches Repository `BENUTZERNAME.github.io` anlegen.
4. Dateien und Ordner aus diesem Paket in das Repository hochladen (nicht nur den übergeordneten Ordner).
5. Unter Settings → Pages → Build and deployment → Deploy from a branch → main / (root) wählen.
6. Nach der Veröffentlichung `https://BENUTZERNAME.github.io` aufrufen.

Das Dashboard verwendet vollständig synthetische Daten und enthält BokehJS inline, sodass kein Python-Server benötigt wird. Bei öffentlichen geschäftlichen Angeboten die geltenden Nutzungsbedingungen von GitHub Pages sowie die rechtlichen Pflichten prüfen.
