import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

def footer():
    st.markdown("""
        <div class="footer">
            Entwickelt von Gruppe A. © 2024.  
        </div>
    """, unsafe_allow_html=True)

def limit_last_used_files(LAST_USED_DIRECTORY):
    # Get a list of files in the last_used directory
    files = os.listdir(LAST_USED_DIRECTORY)
    files_with_paths = [os.path.join(LAST_USED_DIRECTORY, f) for f in files]

    # Sort files by modification time (oldest first)
    files_with_paths.sort(key=os.path.getmtime)

    # If there are more than 5 files, delete the oldest ones
    while len(files_with_paths) > 5:
        os.remove(files_with_paths[0])  # Remove the oldest file
        files_with_paths.pop(0)  # Remove it from the list


def load_data_after_header(file_path):
    # Step 1: Read the file to find the index of -END HEADER-
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Step 2: Find the index of -END HEADER-
    try:
        data_start_index = lines.index("-END HEADER-\n") + 1
    except ValueError:
        raise ValueError("Die Datei ist nicht kompatibel. Beachte das Tutorial auf der ersten Seite.")

    # Step 3: Read the CSV data, skipping rows before data_start_index
    # Use StringIO to create a string buffer from the lines after -END HEADER-
    from io import StringIO
    data_str = ''.join(lines[data_start_index:])

    # Read into DataFrame
    df = pd.read_csv(StringIO(data_str))

    return df

# Funktion: Datei validieren
def validate_file(file_path):
    is_valid = True
    error = None

    # Check if the file has a .csv extension
    if not file_path.endswith('.csv'):
        is_valid = False
        error = "Die Datei muss im CSV-Format sein."
        return is_valid, error

    try:
        # Load DataFrame after header validation
        df = load_data_after_header(file_path)

        # Store DataFrame in session state
        st.session_state.dataframe = df

        # Check if required columns exist
        required_columns = ['YEAR', 'MO', 'DY', 'HR', 'ALLSKY_SFC_SW_DWN', 'PRECTOTCORR', 'WS50M', 'PS']

        for col in required_columns:
            if col not in df.columns:
                is_valid = False
                error = f"Die erforderliche Spalte '{col}' fehlt in den Daten."
                return is_valid, error

        # Check if there are 365 days of data (considering leap years)
        total_unique_dates = df[['YEAR', 'MO', 'DY']].drop_duplicates().shape[0]
        if total_unique_dates < 365:
            is_valid = False
            error = "Die Datei muss Daten für ein ganzes Jahr enthalten."

    except Exception as e:
        is_valid = False
        error = f"Fehler beim Lesen der Datei: {str(e)}"

    return is_valid, error

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
