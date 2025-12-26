# PNG to SVG Converter - Anleitung

## Schnellstart

### Streamlit Web-App (Empfohlen)

```bash
# Abhängigkeiten installieren
uv pip install -r requirements.txt

# App starten
streamlit run png_to_svg_converter.py
```

Die App öffnet sich im Browser auf `http://localhost:8501`

### Kommandozeile

```bash
# Basis-Konvertierung (Tracing)
python3 png2svg_cli.py input.png output.svg

# Mit Base64-Einbettung
python3 png2svg_cli.py input.png output.svg -m embed

# Mit angepassten Parametern
python3 png2svg_cli.py logo.png logo.svg -t 100 -s 3
```

## Parameter

### Streamlit App

- **Konvertierungsmethode**: Wähle zwischen Vektorisierung und Einbettung
- **Schwellenwert** (0-255): Steuert die Schwarz-Weiß-Trennung
  - Niedrige Werte (50-100): Mehr dunkle Bereiche werden erfasst
  - Hohe Werte (150-200): Nur sehr helle Bereiche werden als weiß betrachtet
- **Vereinfachung** (1-10): Reduziert die Komplexität der Pfade
  - Niedrige Werte (1-3): Mehr Details
  - Hohe Werte (5-10): Glattere, einfachere Pfade

### CLI

```
-m, --method        Konvertierungsmethode (trace | embed)
-t, --threshold     Schwellenwert für Tracing (0-255)
-s, --simplify      Vereinfachungslevel (1-10)
--no-auto-invert    Deaktiviert automatische Invertierung
```

## Anwendungsbeispiele

### Logo-Konvertierung

Für klare Logos mit wenigen Farben:

```bash
# Web-App: Verwende Vektorisierung mit Schwellenwert 100-150
streamlit run png_to_svg_converter.py

# CLI
python3 png2svg_cli.py logo.png logo.svg -t 120 -s 2
```

### Komplexe Grafiken

Für detaillierte Bilder oder Fotos:

```bash
# Verwende Einbettung
python3 png2svg_cli.py photo.jpg photo.svg -m embed
```

### Icon-Optimierung

Für kleine Icons:

```bash
# Hohe Vereinfachung für minimale Dateigröße
python3 png2svg_cli.py icon.png icon.svg -t 128 -s 5
```

## Tipps

1. **Dunkle Bilder**: Die Auto-Invertierung erkennt dunkle Bilder automatisch
2. **Dateigröße**: Vektorisierung ist kleiner für einfache Grafiken, Einbettung für komplexe
3. **Editierbarkeit**: Nur vektorisierte SVGs können in Grafikprogrammen bearbeitet werden
4. **Qualität**: Bei Anti-Aliasing funktioniert Einbettung besser

## Unterstützte Formate

**Input**: PNG, JPG, JPEG, WEBP, BMP  
**Output**: SVG (XML)

## Technische Details

### Vektorisierung
- Verwendet OpenCV's Contour-Tracing
- Konvertiert Pixel in Vektorpfade
- Unterstützt Farbextraktion
- Simplifizierung mit Douglas-Peucker-Algorithmus

### Einbettung
- Base64-Kodierung des Originalbilds
- Einbettung in SVG <image> Element
- 1:1 Qualität des Originals
- Größere Dateigröße

## Fehlerbehebung

**Problem**: Keine Konturen gefunden  
**Lösung**: Passe den Schwellenwert an (versuch 50-100 für dunkle Bilder)

**Problem**: Zu viele Details  
**Lösung**: Erhöhe die Vereinfachung auf 4-7

**Problem**: SVG ist riesig  
**Lösung**: Verwende Vektorisierung statt Einbettung

## Weitere Informationen

Für detaillierte Dokumentation siehe README.md
