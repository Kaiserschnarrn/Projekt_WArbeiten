import os
import time

import streamlit as st

from utils import validate_file, limit_last_used_files


def file_upload_page(LAST_USED_DIRECTORY, WINDRAD_IMAGE_PATH):
    st.markdown("<h1 style='text-align: center;'>Dateiauswahl</h1>", unsafe_allow_html=True)
    selected_file = ''
    uploaded_file = st.file_uploader("Wählen Sie eine Datei zum Hochladen aus", type=["csv"],
                                     disabled=bool(selected_file))
    last_used_files = os.listdir(LAST_USED_DIRECTORY)
    selected_file = st.selectbox("Oder wählen Sie eine der zuletzt verwendeten Dateien aus:", [""] + last_used_files)

    if uploaded_file and selected_file:
        st.error("Bitte wählen Sie entweder eine hochgeladene Datei oder eine zuvor verwendete Datei.")
        return

    is_valid = False
    error = None

    if uploaded_file:
        st.write("Validierung der hochgeladenen Datei läuft...")
        with st.spinner("Datei wird validiert..."):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(WINDRAD_IMAGE_PATH, use_container_width=True)
            time.sleep(2)
            original_file_path = os.path.join(LAST_USED_DIRECTORY, uploaded_file.name)
            with open(original_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            is_valid, error = validate_file(original_file_path)

            if is_valid:
                limit_last_used_files(LAST_USED_DIRECTORY)
                st.success("Datei erfolgreich hochgeladen!")
            else:
                st.error(f"Validierung fehlgeschlagen: {error}")
                st.info("Bitte prüfen Sie das Tutorial auf der Startseite.")

    elif selected_file and selected_file != "":
        st.write(f"Validierung der Datei: {selected_file} läuft...")
        with st.spinner("Datei wird validiert..."):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(WINDRAD_IMAGE_PATH, use_container_width=True)
            time.sleep(2)
            selected_file_path = os.path.join(LAST_USED_DIRECTORY, selected_file)
            is_valid, error = validate_file(selected_file_path)

            if is_valid:
                st.success("Datei erfolgreich validiert!")
            else:
                st.error(f"Validierung fehlgeschlagen: {error}")
                st.info("Bitte prüfen Sie das Tutorial auf der Startseite.")

    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück zur Startseite"):
            st.session_state.page = "Start"
    with col2:
        if (uploaded_file or (selected_file and selected_file != "")) and is_valid:
            if st.button("Weiter zur Parameterauswahl"):
                # Da Daten im Session-State sind, kein Kopieren nötig
                st.session_state.page = "Parameterauswahl"
        else:
            st.button("Weiter zur Parameterauswahl", disabled=True)

