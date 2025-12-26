# Decisions: Bugfix libGL Import Error

## Decision Log

### 2025-12-26 - Nutzung von packages.txt vs. opencv-python-headless

**Kontext**: Der Import von `cv2` schlägt auf Streamlit Cloud fehl, da `libGL.so.1` fehlt.

**Optionen**:
1. Option A: `packages.txt` mit `libgl1` hinzufügen.
2. Option B: In `requirements.txt` auf `opencv-python-headless` umstellen.

**Entscheidung**: Option A

**Begründung**: `packages.txt` ist der Standard-Weg in Streamlit Cloud, um fehlende System-Abhängigkeiten nachzuinstallieren. Es ist weniger invasiv als die Python-Abhängigkeiten zu ändern, falls an anderer Stelle doch GUI-Features (z.B. Font-Rendering in OpenCV) genutzt werden, die in Headless eventuell fehlen könnten. Zudem wurden `libgl1` und `libglib2.0-0` hinzugefügt, um gängige OpenCV-Abhängigkeiten abzudecken.

**Konsequenzen**: Streamlit Cloud wird beim nächsten Deployment diese Pakete via APT installieren.
