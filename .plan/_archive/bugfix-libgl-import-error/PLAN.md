# Feature: Bugfix libGL Import Error

> Erstellt: 2025-12-26
> Status: 🟡 In Planung

## Ziel
Behebung des `ImportError: libGL.so.1: cannot open shared object file` Fehlers beim Deployment auf Streamlit Cloud.

## Anforderungen
- [ ] Erstellung einer `packages.txt` Datei für Streamlit Cloud.
- [ ] Hinzufügen von `libgl1` zur Liste der APT-Pakete.

## Scope
**In Scope:**
- System-Abhängigkeiten für OpenCV in Streamlit Cloud.

**Out of Scope:**
- Änderungen an der Bildverarbeitungslogik selbst.

## Technischer Ansatz
Streamlit Cloud benötigt eine `packages.txt` Datei im Root-Verzeichnis, um Systembibliotheken (via `apt-get`) zu installieren. Da `opencv-python` gegen libGL linkt, muss `libgl1` (oder alternativ `libgl1-mesa-glx`) installiert sein.

## Betroffene Dateien
- `packages.txt` (neu zu erstellen)

## Abhängigkeiten
- Keine.

## Offene Fragen
- Keine.
