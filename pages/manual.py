import streamlit as st
import os
from streamlit_pdf_viewer import pdf_viewer

def manual_page(pdf_path):
    if os.path.exists(pdf_path):
        pdf_viewer(pdf_path)
    else:
        st.error("Das Handbuch konnte nicht gefunden werden.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⬅️ Zurück zur Startseite"):
            st.session_state.page = "Start"

    with col4:
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Handbuch herunterladen 📩",
                    data=f,
                    file_name="Handbuch_zum_Tool.pdf",
                    mime="application/pdf"
                )
