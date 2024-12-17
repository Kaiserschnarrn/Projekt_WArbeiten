import streamlit as st
import os

# Titel der Seite
st.title("Handbuch")

# Den relativen Pfad zur PDF-Datei im Ordner 'pages' festlegen
pdf_path = "pages/Handbuch zum Tool.pdf"  # Dein Pfad zur PDF-Datei

# Überprüfen, ob die Datei existiert
if os.path.exists(pdf_path):
    # PDF-Datei im Streamlit-Fenster anzeigen
    st.markdown(f"""
    <iframe src="http://localhost:8501/{pdf_path}" width="100%" height="800px"></iframe>
    """, unsafe_allow_html=True)
else:
    st.error("Das Handbuch konnte nicht gefunden werden.")

