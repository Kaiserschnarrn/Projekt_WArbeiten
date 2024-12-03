from datetime import datetime
import streamlit as st
import os
import time
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Statische Pfade und Konstanten
DATA_DIRECTORY = "./data"
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)
STATIC_FILE_PATH = os.path.join(DATA_DIRECTORY, "NASA_Data.csv")
LAST_USED_DIRECTORY = os.path.join(DATA_DIRECTORY, "last_used")
if not os.path.exists(LAST_USED_DIRECTORY):
    os.makedirs(LAST_USED_DIRECTORY)
WINDRAD_IMAGE_PATH = os.path.abspath("windrad.gif")


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


def add_custom_css():
    st.markdown("""
        <style>
            body {
                background-color: #f7f9fc;
                font-family: 'Arial', sans-serif;
                color: #333;
            }
            .main {
                padding: 2rem;
            }
            .header {
                background-color: #004d99;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                color: white;
                font-family: 'Arial', sans-serif;
                margin-bottom: 30px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .header h1 {
                margin: 0;
                font-size: 2.5rem;
                letter-spacing: 1px;
            }
            .header p {
                font-size: 1rem;
                margin: 5px 0 0;
                color: #cce6ff;
            }
            .footer {
                margin-top: 3rem;
                background-color: #e6f2ff;
                padding: 1rem;
                text-align: center;
                border-radius: 8px;
                color: #004d99;
                font-size: 0.9rem;
            }
            .stButton>button {
                background-color: #0066cc;
                color: white;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-size: 1rem;
                border: none;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #004d99;
            }
            .stExpander {
                background-color: #f7fbff;
                border-left: 4px solid #004d99;
                padding: 1rem;
                margin-top: 1rem;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)


# Funktion: Beispielgrafik erstellen
@st.cache_data  # Caching der Grafik für Konsistenz
def plot_example_graph():
    dates = pd.date_range(start="2024-01-01", periods=30)
    temperatures = np.random.uniform(low=-5, high=25, size=30)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, temperatures, marker='o', linestyle='-', color='blue')
    ax.set_title("Beispiel für Wetterdaten", fontsize=14)
    ax.set_xlabel("Datum", fontsize=12)
    ax.set_ylabel("Temperatur (°C)", fontsize=12)
    ax.grid(visible=True, linestyle='--', alpha=0.7)
    fig.autofmt_xdate(rotation=45)  # Datum leserlich formatieren
    return fig


# Funktion: Startseite
def start_page():
    st.markdown("""
        <div class="header">
            <h1>Wetterdaten-App</h1>
            <p>Analysieren und visualisieren Sie Wetterdaten einfach und effizient</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("""
    Willkommen bei der **Wetterdaten-App**!  
    Nutzen Sie diese Plattform, um Wetterdaten zu analysieren, Szenarien zu erstellen und Ergebnisse zu visualisieren.
    """)

    with st.expander("📖 Tutorial anzeigen"):
        st.write("""
        **Anleitung:**  
        1️⃣ Laden Sie eine CSV-Datei mit Wetterdaten hoch.  
        2️⃣ Prüfen Sie die Datei und wählen Sie Parameter aus.  
        3️⃣ Analysieren und visualisieren Sie Ihre Daten.  
        """)

    st.markdown(
        "<a href='https://power.larc.nasa.gov/data-access-viewer/' style='color: #004d99; text-decoration: none;'>🌐 Besuchen Sie die NASA POWER-Seite</a>",
        unsafe_allow_html=True,
    )

    # Statische Grafik anzeigen
    st.pyplot(plot_example_graph())

    if st.button("🚀 Wetterapp starten"):
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
                limit_last_used_files()  # Ensure we have at most 5 files
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
            if st.button("Weiter zur Parameterauswahl"):
                if selected_file:
                    shutil.copy(selected_file_path, STATIC_FILE_PATH)
                st.session_state.page = "Parameterauswahl"
        else:
            st.button("Weiter zur Parameterauswahl", disabled=True)

def parameter_selection_page():
    st.markdown("<h2>Parameterauswahl</h2>", unsafe_allow_html=True)

    st.markdown("""
        <style>
            .stButton button {
                width: 220px; /* Breite der Buttons */
                height: 90px; /* Höhe der Buttons */
                font-size: 16px; /* Größere Schrift */
                text-align: center; /* Text zentrieren */
                white-space: pre-wrap; /* Text auf mehrere Zeilen erlauben */
            }
        </style>
    """, unsafe_allow_html=True)

    try:
        df = pd.read_csv(STATIC_FILE_PATH)
        st.write("**Vorschau der ausgewählten Datei:**")
        st.dataframe(df.head(4))
    except Exception as e:
        st.error(f"Fehler beim Laden der CSV-Datei: {e}")
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("Solarstrahlung")
    with col2:
        st.button("Niederschlag")
    with col3:
        st.button("Oberflächen-\ndruck")
    with col4:
        st.button("Wind-\ngeschwindigkeit\nin 50 m")

    st.markdown("### Parameter einstellen:")
    if 'worst_case' not in st.session_state:
        st.session_state.worst_case = False
    if 'best_case' not in st.session_state:
        st.session_state.best_case = False

    def update_checkboxes(selected_case):
        if selected_case == "worst_case":
            st.session_state.worst_case = True
            st.session_state.best_case = False
        elif selected_case == "best_case":
            st.session_state.best_case = True
            st.session_state.worst_case = False

    col_checkbox1, col_checkbox2 = st.columns(2)
    #Fix conditions here to appear in the ui immedeately
    with col_checkbox1:
        worst_case_checked = st.checkbox("Worst Case", value=st.session_state.worst_case)
        if worst_case_checked and not st.session_state.worst_case:
            update_checkboxes("worst_case")

    with col_checkbox2:
        best_case_checked = st.checkbox("Best Case", value=st.session_state.best_case)
        if best_case_checked and not st.session_state.best_case:
            update_checkboxes("best_case")

    st.session_state.worst_case = worst_case_checked
    st.session_state.best_case = best_case_checked
    #Change here to use the year from the file
    for parameter in ["Nullpunkt", "Hitzewelle", "Dauerregen", "Sturm"]:
        st.markdown(f"**{parameter}**")
        col_imputs1, col_imputs2 = st.columns(2)

        with col_imputs1:
            st.date_input("Von", key=f"{parameter}_start", value=datetime(2024, 1, 1))

        with col_imputs2:
            st.date_input("Bis", key=f"{parameter}_end", value=datetime(2024, 1, 2))

    col_buttons1, col_buttons2 = st.columns(2)
    with col_buttons1:
        if st.button("⬅️ Zurück zur Datei-Upload-Seite"):
            st.session_state.page = "Dateiauswahl"
    with col_buttons2:
        if st.button("Weiter zu den Ergebnissen"):
            st.success("Parameter wurden gespeichert. Weiterleitung ...")
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


def footer():
    st.markdown("""
        <div class="footer">
            Entwickelt von Gruppe A. © 2024.  
        </div>
    """, unsafe_allow_html=True)


# Funktion: Hauptlogik
def main():
    if "page" not in st.session_state:
        st.session_state.page = "Start"
        footer()

    if st.session_state.page == "Start":
        start_page()
        footer()
    elif st.session_state.page == "Dateiauswahl":
        file_upload_page()
        footer()
    elif st.session_state.page == "Parameterauswahl":
        parameter_selection_page()
        footer()
    elif st.session_state.page == "Ergebnisse":
        results_page()
        footer()


if __name__ == "__main__":
    main()
