# Bibliotheken importieren
import streamlit as st
import os
import pandas as pd
import base64
import time
from datetime import datetime

# Statische Pfade und Konstanten
DATA_DIRECTORY = "./data"
LAST_USED_FILE = os.path.join(DATA_DIRECTORY, "last_used.txt")
STATIC_FILE_PATH = os.path.join(DATA_DIRECTORY, "NASA_Data.csv")
WINDRAD_IMAGE_PATH = os.path.abspath("windrad.gif")  # Absoluter Pfad zum Windrad-GIF

# Initialisierung: Verzeichnisse erstellen
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)

# Funktion: Zuletzt verwendete Dateien speichern und laden
def load_last_used_files():
    if os.path.exists(LAST_USED_FILE):
        with open(LAST_USED_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

def save_last_used_file(file_path):
    last_used_files = load_last_used_files()
    if file_path not in last_used_files:
        last_used_files.insert(0, file_path)  # Neueste Datei an den Anfang setzen
        if len(last_used_files) > 5:
            last_used_files = last_used_files[:5]  # Nur die letzten 5 behalten
        with open(LAST_USED_FILE, "w") as file:
            file.writelines(f"{path}\n" for path in last_used_files)

# CSS für Styling
def add_custom_css():
    st.markdown("""
        <style>
            body {
                background-color: #f7f9fc;
                font-family: 'Arial', sans-serif;
                color: #333;
            }
            .header {
                background-color: #004d99;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            .section {
                margin-top: 20px;
                padding: 15px;
                background-color: #eef6ff;
                border-radius: 10px;
                border: 1px solid #004d99;
            }
        </style>
    """, unsafe_allow_html=True)

# Funktion: Beispielgrafik erstellen
@st.cache_data
def plot_example_graph():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

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

    st.pyplot(plot_example_graph())  # Beispielgrafik anzeigen

    if st.button("🚀 Wetterapp starten"):
        st.session_state.page = "Dateiauswahl"

# Funktion: Datei-Upload-Seite
def file_upload_page():
    st.markdown("<h2>Datei hochladen</h2>", unsafe_allow_html=True)

    # Datei hochladen
    uploaded_file = st.file_uploader("Neue Datei hochladen", type=["csv"])
    if uploaded_file:
        with st.spinner("Datei wird hochgeladen und validiert..."):
            # Zeige Windrad-GIF während des Hochladens
            st.markdown(f"""
                <div style="text-align:center; margin: 20px 0;">
                    <img src="data:image/gif;base64,{base64.b64encode(open(WINDRAD_IMAGE_PATH, "rb").read()).decode()}" alt="Windrad" style="width:100px; height:100px;">
                </div>
            """, unsafe_allow_html=True)

            time.sleep(2)  # Simuliere Ladevorgang
            with open(STATIC_FILE_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            save_last_used_file(STATIC_FILE_PATH)
            st.success("Datei erfolgreich hochgeladen!")

    # Dropdown für zuletzt verwendete Dateien
    last_used_files = load_last_used_files()
    if last_used_files:
        selected_file = st.selectbox("Zuletzt verwendete Dateien:", [""] + last_used_files, key="recent_upload")
        if st.button("Hochladen", key="upload_recent"):
            with st.spinner("Datei wird hochgeladen und validiert..."):
                # Zeige Windrad-GIF während des Hochladens
                st.markdown(f"""
                    <div style="text-align:center; margin: 20px 0;">
                        <img src="data:image/gif;base64,{base64.b64encode(open(WINDRAD_IMAGE_PATH, "rb").read()).decode()}" alt="Windrad" style="width:100px; height:100px;">
                    </div>
                """, unsafe_allow_html=True)

                time.sleep(2)  # Simuliere Ladevorgang
                STATIC_FILE_PATH = selected_file
                st.success(f"Datei {selected_file} erfolgreich verarbeitet!")

    # Weiterleitung zur Parameterauswahl
    if st.button("Weiter zur Parameterauswahl"):
        st.session_state.page = "Parameter"

    if st.button("⬅️ Zurück zur Startseite"):
        st.session_state.page = "Start"

# Funktion: Parameterauswahl-Seite
def parameter_selection_page():
    st.markdown("<h2>Parameterauswahl</h2>", unsafe_allow_html=True)

    # CSS für größere Buttons nur auf dieser Seite
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

    # CSV-Vorschau
    try:
        df = pd.read_csv(STATIC_FILE_PATH)
        st.write("**Vorschau der hochgeladenen CSV-Datei:**")
        st.dataframe(df.head(4))
    except Exception as e:
        st.error(f"Fehler beim Laden der CSV-Datei: {e}")
        return

    # Buttons nebeneinander mit größerer Darstellung
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("Solarstrahlung")
    with col2:
        st.button("Niederschlag")
    with col3:
        st.button("Oberflächen-\ndruck")
    with col4:
        st.button("Wind-\ngeschwindigkeit\nin 50 m")

    # Parameter-Eingabe untereinander
    st.markdown("### Parameter einstellen:")
    st.checkbox("Worst Case", key="worst_case")
    st.checkbox("Best Case", key="best_case")

    for parameter in ["Nullpunkt", "Hitzewelle", "Dauerregen", "Sturm"]:
        st.markdown(f"**{parameter}**")
        st.date_input("Von", key=f"{parameter}_start", value=datetime(2024, 1, 1))
        st.date_input("Bis", key=f"{parameter}_end", value=datetime(2024, 1, 2))

    if st.button("Weiter zur nächsten Seite"):
        st.success("Parameter wurden gespeichert. Weiterleitung ...")

    if st.button("⬅️ Zurück zur Datei-Upload-Seite"):
        st.session_state.page = "Dateiauswahl"

# Hauptlogik
def main():
    add_custom_css()
    if "page" not in st.session_state:
        st.session_state.page = "Start"

    if st.session_state.page == "Start":
        start_page()
    elif st.session_state.page == "Dateiauswahl":
        file_upload_page()
    elif st.session_state.page == "Parameter":
        parameter_selection_page()

if __name__ == "__main__":
    main()













