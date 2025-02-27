# Air-Tag-Simulator

## Anleitung zur Nutzung des Projekts

Das Projekt kann über Docker lokal gestartet werden. Hier ist eine Schritt-für-Schritt-Anleitung, wie du das Air-Tag-Simulator-Projekt auf deinem System zum Laufen bringst.

### Voraussetzungen
Bevor du startest, stelle sicher, dass die folgenden Voraussetzungen erfüllt sind:

- **Docker** ist auf deinem System installiert und läuft.
- Das **Docker Compose** Plugin ist installiert.
- Du hast Zugriff auf das Root-Verzeichnis des Projekts.

---

### Schritt 1: Docker starten
Stelle sicher, dass Docker auf deinem Rechner läuft. Starte Docker, falls es nicht bereits läuft.

- **Windows/Mac**: Docker Desktop öffnen.
- **Linux**: Docker im Terminal starten (falls es nicht automatisch läuft).

---

### Schritt 2: Terminal öffnen
Öffne das Terminal (bzw. die Eingabeaufforderung oder das Command Line Interface (CLI)) deines Betriebssystems.

---

### Schritt 3: Ins Root-Verzeichnis des Projekts wechseln
Navigiere im Terminal in das Root-Verzeichnis deines Projekts.

```bash
cd /pfad/zu/deinem/projekt
```

## Schritt 4: Docker Compose ausführen

Sobald du dich im Root-Verzeichnis des Projekts befindest, kannst du die Anwendung mithilfe von Docker Compose starten. Um dies zu tun, öffne dein Terminal und gib den folgenden Befehl ein:

```bash
docker-compose up
```
### Schritt 5: Frontend aufrufen

Nachdem die Container erfolgreich gestartet wurden, kannst du auf das Frontend der Anwendung zugreifen. Öffne deinen bevorzugten Webbrowser und rufe die folgende URL auf:

```text
http://localhost:7999
```
Dies ist die lokale URL, unter der die Anwendung läuft. Hier kannst du die Benutzeroberfläche des Air-Tag-Simulators nutzen.
