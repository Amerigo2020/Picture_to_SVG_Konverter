"""
Enhanced Image to SVG Converter with Batch Processing
Supports: PNG, JPG, JPEG, WebP, BMP with transparency handling
"""
import streamlit as st
import numpy as np
from PIL import Image
import io
from pathlib import Path

# Import utility modules
from utils.svg_converter import png_to_svg_trace, png_to_svg_embed
from utils.image_analyzer import analyze_image, recommend_method
from utils.batch_processor import process_batch, create_zip_archive


def main():
    st.set_page_config(
        page_title="Image -> SVG Converter",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Bild zu SVG Konverter")
    st.markdown("Wandle Bilder aller Art in SVG-Vektorgrafiken um")
    
    # Sidebar settings
    st.sidebar.header("Einstellungen")
    
    # Batch mode toggle
    batch_mode = st.sidebar.checkbox(
        "Batch-Modus (mehrere Dateien)",
        value=False,
        help="Aktiviere dies um mehrere Bilder gleichzeitig zu konvertieren"
    )
    
    # Conversion method selection
    use_auto_recommend = st.sidebar.checkbox(
        "Auto-Empfehlung",
        value=True,
        help="Automatisch beste Methode basierend auf Bildanalyse empfehlen"
    )
    
    if not use_auto_recommend:
        conversion_method = st.sidebar.radio(
            "Konvertierungsmethode",
            ["Vektorisierung (Tracing)", "Einbettung (Base64)"],
            help="Vektorisierung erstellt echte Vektorpfade, Einbettung bettet das Bild ein"
        )
    else:
        conversion_method = None  # Will be determined per image
    
    # Method-specific settings
    st.sidebar.markdown("---")
    st.sidebar.subheader("Vektorisierungs-Parameter")
    
    threshold = st.sidebar.slider(
        "Schwellenwert",
        0, 255, 128,
        help="Schwarz-Weiß Trennung (niedrigere Werte = mehr Schwarz)"
    )
    simplify = st.sidebar.slider(
        "Vereinfachung",
        1, 10, 2,
        help="Höhere Werte = weniger Details, kleinere Datei"
    )
    
    # Alpha channel handling
    st.sidebar.markdown("---")
    st.sidebar.subheader("Transparenz-Handling")
    
    bg_option = st.sidebar.selectbox(
        "Hintergrund für transparente Bilder",
        ["Weiß", "Schwarz", "Benutzerdefiniert"],
        help="Hintergrundfarbe für Bilder mit Transparenz bei Vektorisierung"
    )
    
    if bg_option == "Benutzerdefiniert":
        background_color = st.sidebar.color_picker("Wähle Hintergrundfarbe", "#FFFFFF")
    elif bg_option == "Schwarz":
        background_color = "#000000"
    else:
        background_color = "#FFFFFF"
    
    # File upload
    max_files = 20 if batch_mode else 1
    
    uploaded_files = st.file_uploader(
        f"{'Bilddateien' if batch_mode else 'Bilddatei'} hochladen",
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp'],
        accept_multiple_files=batch_mode,
        help=f"Wähle {'bis zu 20 Bilddateien' if batch_mode else 'eine Bilddatei'} zum Konvertieren"
    )
    
    # Convert to list if single file
    if uploaded_files and not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]
    
    if uploaded_files:
        num_files = len(uploaded_files)
        
        # Limit check
        if num_files > max_files:
            st.error(f"Fehler: Maximal {max_files} Dateien erlaubt. Du hast {num_files} ausgewählt.")
            return
        
        st.success(f"{num_files} Datei(en) hochgeladen")
        
        # Process images
        if batch_mode and num_files > 1:
            process_batch_mode(
                uploaded_files,
                conversion_method,
                use_auto_recommend,
                threshold,
                simplify,
                background_color
            )
        else:
            # Single file mode
            process_single_mode(
                uploaded_files[0],
                conversion_method,
                use_auto_recommend,
                threshold,
                simplify,
                background_color
            )
    
    else:
        # Show info when no file uploaded
        show_info_section()


def process_single_mode(
    uploaded_file,
    conversion_method,
    use_auto_recommend,
    threshold,
    simplify,
    background_color
):
    """Process and display a single image"""
    
    # Load image
    image = Image.open(uploaded_file)
    image_array = np.array(image)
    
    # Analyze image
    analysis = analyze_image(image_array)
    
    # Get recommendation if auto mode
    if use_auto_recommend:
        recommendation = recommend_method(analysis)
        actual_method = recommendation['method']
    else:
        actual_method = 'trace' if conversion_method == "Vektorisierung (Tracing)" else 'embed'
        recommendation = None
    
    # Display in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original")
        st.image(image, use_container_width=True)
        
        # Show image info
        with st.expander("Bild-Analyse", expanded=False):
            st.write(f"**Größe:** {analysis['width']} × {analysis['height']} px")
            st.write(f"**Farben:** ~{analysis['num_colors']}")
            st.write(f"**Komplexität:** {analysis['complexity']}")
            st.write(f"**Graustufen:** {'Ja' if analysis['is_grayscale'] else 'Nein'}")
            st.write(f"**Transparenz:** {'Ja' if analysis['has_transparency'] else 'Nein'}")
            st.write(f"**Foto-Typ:** {'Ja' if analysis['is_photo'] else 'Nein'}")
    
    with col2:
        st.subheader("SVG Vorschau")
        
        # Show recommendation
        if recommendation:
            confidence_emoji = "" if recommendation['confidence'] > 0.7 else "" if recommendation['confidence'] > 0.5 else ""
            st.info(f"{confidence_emoji} **Empfehlung:** {'Vektorisierung' if actual_method == 'trace' else 'Einbettung'} "
                   f"(Konfidenz: {recommendation['confidence']:.0%})\n\n{recommendation['reason']}")
        
        # Convert based on method
        with st.spinner("Konvertiere..."):
            if actual_method == 'trace':
                svg_content, num_contours = png_to_svg_trace(
                    image_array,
                    threshold=threshold,
                    simplify=simplify,
                    background_color=background_color if analysis['has_transparency'] else None
                )
                st.caption(f"Gefundene Konturen: {num_contours}")
            else:
                svg_content = png_to_svg_embed(image_array)
                st.caption("Bild eingebettet als Base64")
        
        # Display SVG
        st.markdown(svg_content, unsafe_allow_html=True)
        
        # File size info
        svg_size = len(svg_content.encode('utf-8'))
        original_size = len(uploaded_file.getvalue())
        st.caption(f"SVG: {svg_size / 1024:.1f} KB | Original: {original_size / 1024:.1f} KB | "
                  f"{'Kleiner' if svg_size < original_size else 'Größer'}")
    
    # Download button
    st.download_button(
        label="SVG herunterladen",
        data=svg_content,
        file_name=Path(uploaded_file.name).stem + '.svg',
        mime="image/svg+xml",
        use_container_width=True
    )
    
    # Show SVG code
    with st.expander("SVG Code anzeigen"):
        st.code(svg_content, language="xml")


def process_batch_mode(
    uploaded_files,
    conversion_method,
    use_auto_recommend,
    threshold,
    simplify,
    background_color
):
    """Process multiple images in batch"""
    
    st.subheader(f"Batch-Verarbeitung ({len(uploaded_files)} Dateien)")
    
    # Prepare image data
    images_data = []
    for uploaded_file in uploaded_files:
        try:
            image = Image.open(uploaded_file)
            image_array = np.array(image)
            images_data.append((uploaded_file.name, image_array))
        except Exception as e:
            st.warning(f"Fehler beim Laden von {uploaded_file.name}: {e}")
    
    if not images_data:
        st.error("Keine Bilder konnten geladen werden")
        return
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def update_progress(current, total):
        progress_bar.progress(current / total)
        status_text.text(f"Verarbeitet: {current}/{total}")
    
    # Process based on auto-recommend or manual method
    results = []
    
    with st.spinner("Verarbeite Bilder..."):
        for i, (filename, image_array) in enumerate(images_data):
            try:
                # Analyze and determine method
                if use_auto_recommend:
                    analysis = analyze_image(image_array)
                    recommendation = recommend_method(analysis)
                    method = recommendation['method']
                else:
                    method = 'trace' if conversion_method == "Vektorisierung (Tracing)" else 'embed'
                    analysis = analyze_image(image_array)
                
                # Convert
                if method == 'trace':
                    svg_content, _ = png_to_svg_trace(
                        image_array,
                        threshold=threshold,
                        simplify=simplify,
                        background_color=background_color if analysis.get('has_transparency') else None
                    )
                else:
                    svg_content = png_to_svg_embed(image_array)
                
                results.append((filename, svg_content, True, ""))
            except Exception as e:
                results.append((filename, "", False, str(e)))
            
            update_progress(i + 1, len(images_data))
    
    progress_bar.empty()
    status_text.empty()
    
    # Display results summary
    successful = sum(1 for _, _, success, _ in results if success)
    st.success(f"{successful}/{len(results)} Bilder erfolgreich konvertiert")
    
    if successful < len(results):
        st.warning(f"{len(results) - successful} Fehler aufgetreten")
    
    # Show results in grid
    st.markdown("### Ergebnisse")
    
    cols = st.columns(min(3, len(results)))
    for idx, (filename, svg_content, success, error) in enumerate(results):
        with cols[idx % len(cols)]:
            if success:
                st.markdown(f"**{filename}**")
                st.markdown(svg_content, unsafe_allow_html=True)
                svg_size = len(svg_content.encode('utf-8'))
                st.caption(f"{svg_size / 1024:.1f} KB")
                
                # Individual download
                st.download_button(
                    label="Download",
                    data=svg_content,
                    file_name=Path(filename).stem + '.svg',
                    mime="image/svg+xml",
                    key=f"download_{idx}"
                )
            else:
                st.markdown(f"**Fehler: {filename}**")
                st.error(f"Fehler: {error}")
    
    # Bulk download as ZIP
    if successful > 0:
        st.markdown("---")
        zip_data = create_zip_archive(results)
        
        st.download_button(
            label=f"Alle SVGs als ZIP herunterladen ({successful} Dateien)",
            data=zip_data,
            file_name="converted_svgs.zip",
            mime="application/zip",
            use_container_width=True
        )


def show_info_section():
    """Show information when no files are uploaded"""
    
    st.info("Lade eine oder mehrere Bilddateien hoch, um zu starten")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
### Konvertierungs-Methoden

**Vektorisierung (Tracing)**
- Erstellt echte SVG-Pfade
- Ideal für: Logos, Icons, einfache Grafiken
- Kleine Dateigröße
- Skalierbar ohne Qualitätsverlust
- In Vektorgrafik-Programmen editierbar
- Verliert Details bei komplexen Bildern

**Einbettung (Base64)**
- Bettet Bild als Base64 in SVG ein
- Ideal für: Fotos, komplexe Grafiken
- Behält alle Details
- Pixel-perfekte Wiedergabe
- Größere Dateigröße
- Nicht als Vektor editierbar
""")
    
    with col2:
        st.markdown("""
### Features

- **Batch-Verarbeitung**: Bis zu 20 Bilder gleichzeitig
- **Auto-Empfehlung**: KI schlägt beste Methode vor
- **Transparenz-Support**: Alpha-Kanal wird korrekt behandelt
- **Anpassbare Parameter**: Schwellenwert & Vereinfachung
- **Bildanalyse**: Detaillierte Informationen zu jedem Bild
- **ZIP-Export**: Alle konvertierten Dateien auf einmal

### Unterstützte Formate

- PNG (mit Transparenz)
- JPG/JPEG
- WebP
- BMP
""")
    
    st.markdown("---")
    st.markdown("""
    ### Wann welche Methode?
    
    | Bildtyp | Empfohlene Methode | Warum |
    |---------|-------------------|-------|
    | Logo mit wenigen Farben | Vektorisierung | Kleine Datei, perfekt skalierbar |
    | Icon/Symbol | Vektorisierung | Editierbar, kleine Datei |
    | Foto/Screenshot | Einbettung | Behält alle Details |
    | Komplexe Grafik | Einbettung | Qualität bleibt erhalten |
    | Transparentes Logo | Vektorisierung | Transparenz wird zu Vektorpfaden |
    """)


if __name__ == "__main__":
    main()
