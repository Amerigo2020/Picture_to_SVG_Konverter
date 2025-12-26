# PNG zu SVG Konverter

Ein interaktives Tool zur Umwandlung von PNG-Bildern in SVG-Vektorgrafiken.

## Features

- **Multi-Format Support**: PNG, JPG, JPEG, WebP, BMP
- **Batch-Verarbeitung**: Bis zu 20 Bilder gleichzeitig konvertieren
- **Auto-Empfehlung**: KI-gestützte Methodenauswahl basierend auf Bildanalyse
- **Transparenz-Handling**: Intelligente Alpha-Kanal-Verarbeitung
- **Vektorisierung**: Erstellt echte SVG-Pfade mittels Contour-Tracing
- **Einbettung**: Bettet Bilder als Base64 in SVG ein
- **Interaktive Parameter**: Schwellenwert und Vereinfachung anpassbar
- **Live-Vorschau**: Sofortige Anzeige des Ergebnisses
- **ZIP-Export**: Alle konvertierten Dateien auf einmal herunterladen
- **Bildanalyse**: Detaillierte Informationen zu jedem Bild

## Installation

```bash
# Mit uv (empfohlen)
uv pip install -r requirements.txt

# Oder mit pip
pip install -r requirements.txt

# Installiert: streamlit, opencv-python, pillow, numpy, scikit-learn
```

## Verwendung

```bash
streamlit run png_to_svg_converter.py
```

Das Tool öffnet sich im Browser auf `http://localhost:8501`

## Methoden

### Vektorisierung (Tracing)
- Wandelt Pixel in Vektorpfade um
- Ideal für: Logos, Icons, einfache Grafiken
- Vorteile: Kleine Dateigröße, editierbar, skalierbar
- Nachteile: Verliert Details bei komplexen Bildern

### Einbettung (Base64)
- Bettet PNG-Daten in SVG ein
- Ideal für: Fotos, komplexe Grafiken
- Vorteile: Behält alle Details
- Nachteile: Größere Dateigröße, nicht editierbar

## Parameter

- **Schwellenwert** (0-255): Steuert Schwarz-Weiß-Trennung bei Vektorisierung
- **Vereinfachung** (1-10): Reduziert Pfadkomplexität

## Beispiele

1. Logo konvertieren: Verwende Vektorisierung mit niedrigem Schwellenwert (100-150)
2. Foto in SVG einbetten: Verwende Einbettung
3. Icon optimieren: Verwende Vektorisierung mit hoher Vereinfachung

## Batch-Modus

Aktiviere den Batch-Modus in der Sidebar, um mehrere Bilder gleichzeitig zu konvertieren:
- Bis zu 20 Bilder auf einmal
- Parallele Verarbeitung für schnelle Konvertierung
- Einzelne Downloads oder alle als ZIP
- Fortschrittsanzeige während der Verarbeitung

## Auto-Empfehlung

Die KI analysiert jedes Bild und empfiehlt die beste Konvertierungsmethode:
- **Bildanalyse**: Farben, Komplexität, Transparenz
- **Konfidenz-Score**: Wie sicher die Empfehlung ist
- **Begründung**: Warum diese Methode empfohlen wird

Analysierte Eigenschaften:
- Farbanzahl und -komplexität
- Transparenz (Alpha-Kanal)
- Bildgröße und Auflösung
- Foto vs. Grafik Erkennung

## Technologie

- **Streamlit**: Web-Interface
- **OpenCV**: Bildverarbeitung und Contour-Tracing
- **Pillow**: Bildmanipulation
- **NumPy**: Array-Operationen
- **scikit-learn**: Bildanalyse (geplant: K-Means für Farboptimierung)
