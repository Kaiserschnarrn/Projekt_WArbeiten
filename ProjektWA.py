import streamlit as st
import os
import time
import shutil

# Statische Pfade und Konstanten
DATA_DIRECTORY = "./data"
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)
STATIC_FILE_PATH = os.path.join(DATA_DIRECTORY, "NASA_Data.csv")
LAST_USED_DIRECTORY = os.path.join(DATA_DIRECTORY, "last_used")
if not os.path.exists(LAST_USED_DIRECTORY):
    os.makedirs(LAST_USED_DIRECTORY)


def limit_last_used_files():
    # Get a list of files in the last_used directory
    files = os.listdir(LAST_USED_DIRECTORY)
    files_with_paths = [os.path.join(LAST_USED_DIRECTORY, f) for f in files]

    # Sort files by modification time (oldest first)
    files_with_paths.sort(key=os.path.getmtime)

    # If there are more than 5 files, delete the oldest ones
    while len(files_with_paths) > 5:
        os.remove(files_with_paths[0])  # Remove the oldest file
        files_with_paths.pop(0)  # Remove it from the list


# Funktion: Letzte verwendete Dateien laden
def load_last_used_files():
    if os.path.exists(LAST_USED_FILE):
        with open(LAST_USED_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []


def add_file_to_last_used(file_path):
    with open(LAST_USED_FILE, "a") as file:
        file.write(file_path + "\n")


# Funktion: Datei validieren (Dummy-Funktion für Beispielzwecke)
def validate_file(file_path):
    is_valid = True
    error = None
    # Needs to be adjusted to validate the content of the csv
    if not file_path.endswith('.csv'):
        is_valid = False
        error = "Die Datei muss im CSV-Format sein."

    return is_valid, error


# Funktion: Startseite
def start_page():
    st.markdown("<h1 style='text-align: center;'>Start</h1>", unsafe_allow_html=True)
    st.write("""Willkommen zur **Wetterdaten-App**!  
    Analysieren und visualisieren Sie Wetterdaten einfach und effizient.  
    Nutzen Sie die App, um benutzerdefinierte Wetter-Szenarien für erneuerbare Energiesysteme zu erstellen.""")

    with st.expander("Tutorial anzeigen"):
        st.write("""Willkommen zum Tutorial!  
        Schön, dass Sie dabei sind.  

        **Schritt 1:** Laden Sie eine Wetterdatendatei im CSV-Format hoch.  
        **Schritt 2:** Sehen Sie sich die Vorschau Ihrer Daten an und wählen Sie die gewünschte Verarbeitung.  
        **Schritt 3:** Visualisieren Sie Ergebnisse basierend auf den von Ihnen gewählten Parametern.  

        Alles, was Sie brauchen, ist eine CSV-Datei und etwas Neugier.  
        Viel Erfolg und Spaß!""")

    st.markdown(
        "[Besuchen Sie die NASA POWER Seite](https://power.larc.nasa.gov/data-access-viewer/) "
        "für weitere Informationen zu den Wetterdaten.",
        unsafe_allow_html=True,
    )

    if st.button("Wetterapp starten"):
        st.session_state.page = "Dateiauswahl"


# Funktion: Dateiauswahl-Seite
def file_upload_page():
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
            time.sleep(2)  # Simulierte Ladezeit
            # Copy the uploaded file to the last_used directory with its original name
            original_file_path = os.path.join(LAST_USED_DIRECTORY, uploaded_file.name)
            with open(original_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            limit_last_used_files()  # Ensure we have at most 5 files
            st.success("Datei erfolgreich hochgeladen!")

    elif selected_file:
        st.write(f"Validierung der Datei: {selected_file} läuft...")
        with st.spinner("Datei wird validiert..."):
            time.sleep(2)  # Simulierte Ladezeit
            selected_file_path = os.path.join(LAST_USED_DIRECTORY, selected_file)
            is_valid, error = validate_file(selected_file_path)  # Validate the selected file
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
            if st.button("Weiter zur Parameterauswahl"):
                if selected_file:
                    shutil.copy(selected_file_path, STATIC_FILE_PATH)
                st.session_state.page = "Parameterauswahl"
        else:
            st.button("Weiter zur Parameterauswahl", disabled=True)


def parameter_selection_page():
    st.markdown("<h1 style='text-align: center;'>Parameter Auswahl</h1>", unsafe_allow_html=True)

    # Add parameter selection controls here
    parameter1 = st.slider("Parameter 1", 0, 100, 50)
    parameter2 = st.selectbox("Parameter 2", ["Option 1", "Option 2", "Option 3"])

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück zur Dateiauswahl"):
            st.session_state.page = "Dateiauswahl"
    with col2:
        if st.button("Weiter zu den Ergebnissen"):
            st.session_state.page = "Ergebnisse"


def results_page():
    st.markdown("<h1 style='text-align: center;'>Ergebnisse</h1>", unsafe_allow_html=True)

    # Display the results here
    st.write("This is where the results will be displayed.")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück zur Parameterauswahl"):
            st.session_state.page = "Parameterauswahl"
    with col2:
        if st.button("Zurück zur Startseite"):
            st.session_state.page = "Start"


# Funktion: Hauptlogik
def main():
    if "page" not in st.session_state:
        st.session_state.page = "Start"

    if st.session_state.page == "Start":
        start_page()
    elif st.session_state.page == "Dateiauswahl":
        file_upload_page()
    elif st.session_state.page == "Parameterauswahl":
        parameter_selection_page()
    elif st.session_state.page == "Ergebnisse":
        results_page()


if __name__ == "__main__":
    main()
