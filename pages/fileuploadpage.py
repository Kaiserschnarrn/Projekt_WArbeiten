import shutil
import time

from utils import *


# Funktion: Dateiauswahl-Seite
def file_upload_page(LAST_USED_DIRECTORY, WINDRAD_IMAGE_PATH, STATIC_FILE_PATH):
    st.markdown("<h1 style='text-align: center;'>Dateiauswahl</h1>", unsafe_allow_html=True)
    selected_file = ''
    uploaded_file = st.file_uploader("Wählen Sie eine Datei zum Hochladen aus", type=["csv"],
                                     disabled=bool(selected_file))
    last_used_files = os.listdir(LAST_USED_DIRECTORY)
    selected_file = st.selectbox("Oder wählen Sie eine der zuletzt verwendeten Dateien aus:", [""] + last_used_files)

    if uploaded_file and selected_file:
        st.error("Bitte wählen Sie entweder eine hochgeladene Datei oder eine zuvor verwendete Datei.")
        return

    if uploaded_file:
        st.write("Validierung der hochgeladenen Datei läuft...")
        with st.spinner("Datei wird validiert..."):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:  # Use the middle column for centering
                st.image(WINDRAD_IMAGE_PATH, use_column_width=True)
            time.sleep(2)  # Simulated loading time
            # Copy the uploaded file to the last_used directory with its original name
            original_file_path = os.path.join(LAST_USED_DIRECTORY, uploaded_file.name)
            with open(original_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Validate the uploaded file
            is_valid, error = validate_file(original_file_path)

            if is_valid:
                limit_last_used_files(LAST_USED_DIRECTORY)  # Ensure we have at most 5 files
                st.success("Datei erfolgreich hochgeladen!")
            else:
                st.error(f"Validierung fehlgeschlagen: {error}")
                st.info("Bitte prüfen Sie das Tutorial auf der Startseite.")

    elif selected_file:
        st.write(f"Validierung der Datei: {selected_file} läuft...")
        with st.spinner("Datei wird validiert..."):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:  # Use the middle column for centering
                st.image(WINDRAD_IMAGE_PATH, use_column_width=True)
            time.sleep(2)  # Simulated loading time
            selected_file_path = os.path.join(LAST_USED_DIRECTORY, selected_file)

            # Validate the selected file
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
        if uploaded_file or selected_file:
            if st.button("Weiter zur Parameterauswahl", disabled=not is_valid):
                if selected_file:
                    shutil.copy(selected_file_path, STATIC_FILE_PATH)
                st.session_state.page = "Parameterauswahl"
        else:
            st.button("Weiter zur Parameterauswahl", disabled=True)
