#import streamlit as st
#import pandas as pd
#import plotly.express as px

#def load_data(file_path):
  #  try:
        # Laden der CSV-Datei ohne Header und mit festgelegten Spaltennamen
       #data = pd.read_csv(file_path, header=None, names=["timestamp", "power_output"], on_bad_lines='skip')
        # Umwandeln der 'timestamp'-Spalte in Datetime-Format
       # data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
       # return data
    #except Exception as e:
        #st.error(f"Fehler beim Laden der Daten: {e}")
       # return pd.DataFrame()  # Gibt ein leeres DataFrame zurück im Fehlerfall

# Pfad zur CSV-Datei anpassen
#data_path = r"C:\Users\kingj\AppData\Roaming\JetBrains\PyCharmCE2024.1\scratches\solar_daten.csv"

# Daten laden
#data = load_data

# Versuch am 03.11 Modelle zu erstellen; hat nicht geklappt
# Versuch 3 am 05.11 Modelle zu erstellen
# am 20.11 weiterprogrammiert (Tutorial und Verbesserungen am Code)
import streamlit as st
import os
import time
import pandas as pd

# Statische Pfade und Konstanten
DATA_DIRECTORY = "./data"
LAST_USED_FILE = os.path.join(DATA_DIRECTORY, "last_used.txt")
STATIC_FILE_PATH = os.path.join(DATA_DIRECTORY, "NASA_Data.csv")

# Initialisierung: Verzeichnisse erstellen
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)

# Funktion: Letzte verwendete Dateien laden
def load_last_used_files():
    if os.path.exists(LAST_USED_FILE):
        with open(LAST_USED_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

# Funktion: Neue Datei zur Liste der letzten Dateien hinzufügen
def add_file_to_last_used(file_path):
    last_used = load_last_used_files()
    if file_path in last_used:
        last_used.remove(file_path)
    last_used.insert(0, file_path)  # Neuste Datei zuerst
    if len(last_used) > 5:
        last_used = last_used[:5]  # Nur die letzten 5 Einträge behalten
    with open(LAST_USED_FILE, "w") as file:
        file.writelines([f"{path}\n" for path in last_used])

# Funktion: Datei validieren (Dummy-Funktion für Beispielzwecke)
def validate_file(file_path):
    try:
        # Datei als CSV laden und prüfen (z. B. auf spezifische Spalten)
        df = pd.read_csv(file_path)
        # Beispielprüfung: Mindestens 2 Spalten erforderlich
        if df.shape[1] < 2:
            return False, "Die Datei enthält nicht genügend Spalten."
        return True, None
    except Exception as e:
        return False, f"Fehler beim Lesen der Datei: {e}"

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

    # Datei-Upload und Dropdown-Optionen
    uploaded_file = st.file_uploader("Wählen Sie eine Datei zum Hochladen aus", type=["csv"])
    last_used_files = load_last_used_files()
    selected_file = st.selectbox("Oder wählen Sie eine der zuletzt verwendeten Dateien aus:", [""] + last_used_files)

    if uploaded_file and selected_file:
        st.error("Bitte wählen Sie entweder eine hochgeladene Datei oder eine zuvor verwendete Datei.")
        return

    # Ladeanimation und Validierung
    if uploaded_file:
        st.write("Validierung der hochgeladenen Datei läuft...")
        with st.spinner("Datei wird validiert..."):
            time.sleep(2)  # Simulierte Ladezeit
            with open(STATIC_FILE_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            add_file_to_last_used(STATIC_FILE_PATH)
            is_valid, error = validate_file(STATIC_FILE_PATH)
        if is_valid:
            st.success("Datei erfolgreich validiert!")
        else:
            st.error(f"Validierung fehlgeschlagen: {error}")
            st.info("Bitte prüfen Sie das Tutorial auf der Startseite.")

    elif selected_file:
        st.write(f"Validierung der Datei: {selected_file} läuft...")
        with st.spinner("Datei wird validiert..."):
            time.sleep(2)  # Simulierte Ladezeit
            is_valid, error = validate_file(selected_file)
        if is_valid:
            st.success("Datei erfolgreich validiert!")
            with open(STATIC_FILE_PATH, "wb") as f:
                f.write(open(selected_file, "rb").read())
        else:
            st.error(f"Validierung fehlgeschlagen: {error}")
            st.info("Bitte prüfen Sie das Tutorial auf der Startseite.")

    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück zur Startseite"):
            st.session_state.page = "Start"
    with col2:
        if st.button("Weiter zur Verarbeitung"):
            if uploaded_file or selected_file:
                st.session_state.page = "Verarbeitung"
            else:
                st.warning("Bitte wählen Sie zuerst eine Datei aus!")

# Funktion: Hauptlogik
def main():
    if "page" not in st.session_state:
        st.session_state.page = "Start"

    if st.session_state.page == "Start":
        start_page()
    elif st.session_state.page == "Dateiauswahl":
        file_upload_page()

if __name__ == "__main__":
    main()