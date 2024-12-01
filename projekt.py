# Bibliotheken importieren
import streamlit as st
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64

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
    st.markdown("<h2>Datei hochladen</h2>", unsafe_allow_html=True)

    # Letzte verwendete Dateien anzeigen
    last_used_files = load_last_used_files()
    if last_used_files:
        st.write("Zuletzt verwendete Dateien:")
        selected_file = st.selectbox("Wählen Sie eine Datei aus:", [""] + last_used_files)
        if selected_file:
            st.success(f"Ausgewählte Datei: {selected_file}")

    uploaded_file = st.file_uploader("Wählen Sie eine Datei zum Hochladen aus", type=["csv"])

    if uploaded_file:
        st.write("Validierung der hochgeladenen Datei läuft...")
        with st.spinner("Datei wird validiert..."):
            # Zeige das Windrad-GIF
            st.markdown(f"""
                <div style="text-align:center; margin: 20px 0;">
                    <img src="data:image/gif;base64,{base64.b64encode(open(WINDRAD_IMAGE_PATH, "rb").read()).decode()}" alt="Windrad" style="width:150px; height:auto;">
                </div>
            """, unsafe_allow_html=True)

            time.sleep(2)
            with open(STATIC_FILE_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Speichere die Datei als zuletzt verwendet
            save_last_used_file(STATIC_FILE_PATH)

            st.success("Datei erfolgreich validiert! ✅")

    if st.button("⬅️ Zurück zur Startseite"):
        st.session_state.page = "Start"

# Funktion: Footer
def footer():
    st.markdown("""
        <div class="footer">
            Entwickelt von Gruppe A. © 2024.  
        </div>
    """, unsafe_allow_html=True)

# Hauptlogik
def main():
    add_custom_css()
    if "page" not in st.session_state:
        st.session_state.page = "Start"

    if st.session_state.page == "Start":
        start_page()
        footer()
    elif st.session_state.page == "Dateiauswahl":
        file_upload_page()
        footer()

if __name__ == "__main__":
    main()




















