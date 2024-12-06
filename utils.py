import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Funktion: Datei validieren (Dummy-Funktion für Beispielzwecke)
def validate_file(file_path):
    is_valid = True
    error = None
    # Needs to be adjusted to validate the content of the csv
    if not file_path.endswith('.csv'):
        is_valid = False
        error = "Die Datei muss im CSV-Format sein."

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
