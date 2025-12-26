# Feature: Multi-Format Image to SVG Converter Enhancement

> Erstellt: 2025-12-26
> Status: 🟡 In Planung

## Ziel
Die bestehende PNG-zu-SVG-Anwendung soll verbessert werden, um alle gängigen Bildformate optimal zu unterstützen, die Benutzerfreundlichkeit zu erhöhen und die Konvertierungsqualität zu verbessern.

## Anforderungen

### Funktionale Anforderungen
- [x] **Bereits implementiert**: Unterstützung für PNG, JPG, JPEG, WebP, BMP
- [ ] **NEU**: Optimiertes Handling für Bilder mit Transparenz (Alpha-Kanal)
- [ ] **NEU**: Batch-Verarbeitung mehrerer Bilder gleichzeitig
- [ ] **NEU**: Verbesserte Drag-and-Drop UI mit Feedback
- [ ] **NEU**: Automatische Format-Erkennung und Vorschlag der besten Konvertierungsmethode
- [ ] **VERBESSERUNG**: Bessere Farberhaltung bei Multi-Color-Bildern
- [ ] **VERBESSERUNG**: Preview-Qualität optimieren

### Nicht-funktionale Anforderungen
- [ ] Performance: Verarbeitung von Bildern bis 5000x5000px ohne Verzögerung
- [ ] UX: Klares visuelles Feedback während Verarbeitung
- [ ] Error Handling: Aussagekräftige Fehlermeldungen
- [ ] Code-Qualität: Modularer, wartbarer Code

## Scope

**In Scope:**
- Alpha-Kanal-Handling für PNG und WebP
- Batch-Upload und -Verarbeitung
- Verbesserte UI mit Drag-and-Drop Feedback
- Automatische Methoden-Empfehlung basierend auf Bildtyp
- Erweiterte Farberhaltung
- Progress-Anzeige
- Datei-Validierung
- Export mehrerer SVGs als ZIP

**Out of Scope:**
- KI-basierte Vektorisierung
- Erweiterte SVG-Editierfunktionen
- Cloud-Speicherung
- User-Accounts
- Weitere Ausgabeformate (PDF, EPS, etc.)

## Technischer Ansatz

### 1. Alpha-Kanal-Handling
```python
# Strategie:
- Transparenz-Erkennung vor Konvertierung
- Option: Weißer/Farbiger Hintergrund für JPG-Konvertierung
- SVG-Opacity für semi-transparente Bereiche
```

### 2. Batch-Verarbeitung
```python
# Implementierung:
- st.file_uploader mit accept_multiple_files=True
- Parallele Verarbeitung mit ThreadPoolExecutor
- Progress-Bar mit st.progress()
- ZIP-Export mit zipfile-Modul
```

### 3. UI-Verbesserungen
```python
# Features:
- Drag-and-Drop Zone mit visueller Hervorhebung
- Thumbnail-Grid für mehrere Uploads
- Live-Fortschrittsanzeige
- Download-Button pro Bild + "Alle herunterladen"
```

### 4. Automatische Methoden-Empfehlung
```python
# Logik:
- Analyse: Farbanzahl, Komplexität, Transparenz
- Empfehlung: 
  - Wenige Farben + Transparenz → Vektorisierung
  - Viele Farben + Foto → Einbettung
  - Logo/Icon → Vektorisierung
```

### 5. Verbesserte Farberhaltung
```python
# Optimierungen:
- K-Means Clustering für dominante Farben
- Color Quantization vor Vektorisierung
- Separate Pfade für verschiedene Farbbereiche
```

## Betroffene Dateien

### Neu zu erstellen:
- `utils/image_analyzer.py` - Bildanalyse-Funktionen
- `utils/batch_processor.py` - Batch-Verarbeitung
- `utils/svg_optimizer.py` - SVG-Optimierung

### Zu modifizieren:
- [png_to_svg_converter.py](file:///C:/Users/ameri/Documents/Programming/PNG_SVG_Konvertierungstool/png_to_svg_converter.py) - Hauptanwendung
  - Refactoring: Funktionen in Module auslagern
  - UI-Erweiterung für Batch-Upload
  - Integration neuer Features

- [requirements.txt](file:///C:/Users/ameri/Documents/Programming/PNG_SVG_Konvertierungstool/requirements.txt)
  - Hinzufügen: `scikit-learn` (für K-Means)
  - Hinzufügen: `scipy` (für erweiterte Bildverarbeitung)

- [README.md](file:///C:/Users/ameri/Documents/Programming/PNG_SVG_Konvertierungstool/README.md)
  - Dokumentation neuer Features
  - Anwendungsbeispiele erweitern

## Abhängigkeiten

**Externe:**
- Keine neuen System-Abhängigkeiten
- Python-Packages: scikit-learn, scipy (bereits weit verbreitet)

**Interne:**
- Bestehender Code muss refactored werden
- Modularisierung vor Feature-Erweiterung

## Architektur-Entscheidungen

### Modularisierung
**Problem**: Aktuell ist alle Logik in einer Datei (208 Zeilen)  
**Lösung**: Aufteilen in Module für bessere Wartbarkeit

```
png_to_svg_converter/
├── main.py                  # Streamlit UI
├── utils/
│   ├── __init__.py
│   ├── image_analyzer.py    # Bildanalyse
│   ├── svg_converter.py     # Konvertierungsfunktionen
│   ├── batch_processor.py   # Batch-Verarbeitung
│   └── svg_optimizer.py     # SVG-Optimierung
└── requirements.txt
```

### Batch-Verarbeitung: Threading vs. Multiprocessing
**Entscheidung**: Threading mit ThreadPoolExecutor  
**Begründung**:
- Streamlit läuft bereits in Threads
- I/O-bound Operations (Bildladen)
- Einfachere Integration
- Geringerer Memory-Overhead

### Alpha-Kanal: Strategie
**Entscheidung**: Optionale Hintergrund-Farbe + SVG-Opacity  
**Begründung**:
- User behält Kontrolle
- SVG unterstützt Transparenz nativ
- Flexibler für verschiedene Use-Cases

## Offene Fragen

- [ ] **Performance**: Maximale Anzahl gleichzeitiger Uploads? (Vorschlag: 20)
- [ ] **UI**: Soll alte Datei-Namen beibehalten oder umbenennen? (Vorschlag: Original beibehalten)
- [ ] **Export**: ZIP-Format oder einzelne Downloads? (Vorschlag: Beides als Option)
- [ ] **Qualität**: Standard-Schwellenwerte für Auto-Modus? (Vorschlag: Adaptiv basierend auf Bildanalyse)

## Implementierungs-Reihenfolge

### Phase 1: Code-Refactoring (Foundation)
1. Projekt-Struktur erstellen
2. Bestehende Funktionen in Module auslagern
3. Tests für bestehende Funktionalität

### Phase 2: Core Features
4. Alpha-Kanal-Handling implementieren
5. Bildanalyse-Modul erstellen
6. Automatische Methoden-Empfehlung

### Phase 3: Batch & UI
7. Batch-Upload implementieren
8. UI-Verbesserungen (Drag-n-Drop Feedback)
9. Progress-Bar und Download-Optionen

### Phase 4: Optimierung
10. Farberhaltung verbessern
11. Performance-Optimierung
12. Error-Handling erweitern

## Verification Plan

### Automated Tests
- Unit-Tests für alle neuen Module
- Integration-Tests für Batch-Verarbeitung
- Performance-Tests mit verschiedenen Bildgrößen

### Manual Verification
1. **Format-Tests**: PNG, JPG, WebP, BMP mit verschiedenen Eigenschaften
2. **Batch-Test**: 10+ Bilder gleichzeitig hochladen und konvertieren
3. **Alpha-Test**: PNG mit Transparenz in verschiedenen Modi
4. **UI-Test**: Drag-and-Drop, Progress-Feedback, Downloads
5. **Edge-Cases**: 
   - Sehr große Bilder (>4000px)
   - Sehr kleine Bilder (<50px)
   - Monochrome Bilder
   - Hochkomplexe Fotos

## Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Performance bei großen Batches | Mittel | Hoch | Limit auf 20 Dateien, Threading |
| Speicher bei großen Bildern | Mittel | Mittel | Image-Resize vor Verarbeitung |
| Breaking Changes im Refactoring | Niedrig | Hoch | Tests vor Änderungen schreiben |
| Komplexität K-Means | Niedrig | Niedrig | Optional, deaktivierbar |

## Success Criteria

✅ **MVP erreicht wenn:**
- Batch-Upload funktioniert (min. 10 Bilder)
- Alpha-Kanal wird korrekt behandelt
- UI gibt klares Feedback
- Code ist modular strukturiert

✅ **Feature komplett wenn:**
- Alle geplanten Features implementiert
- Tests bestehen
- Dokumentation aktualisiert
- Performance-Ziele erreicht (<2s pro Bild)
