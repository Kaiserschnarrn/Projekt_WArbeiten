import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64

def footer():
    st.markdown("""
        <div class="footer">
            Entwickelt von Gruppe A. © 2024.  
        </div>
    """, unsafe_allow_html=True)

def limit_last_used_files(LAST_USED_DIRECTORY):
    files = os.listdir(LAST_USED_DIRECTORY)
    files_with_paths = [os.path.join(LAST_USED_DIRECTORY, f) for f in files]

    files_with_paths.sort(key=os.path.getmtime)

    while len(files_with_paths) > 5:
        os.remove(files_with_paths[0])
        files_with_paths.pop(0)

def load_data_after_header(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    try:
        data_start_index = lines.index("-END HEADER-\n") + 1
    except ValueError:
        raise ValueError("Die Datei ist nicht kompatibel. Beachte das Tutorial auf der ersten Seite.")

    from io import StringIO
    data_str = ''.join(lines[data_start_index:])

    df = pd.read_csv(StringIO(data_str))

    return df

def validate_file(file_path):
    is_valid = True
    error = None

    if not file_path.endswith('.csv'):
        is_valid = False
        error = "Die Datei muss im CSV-Format sein."
        return is_valid, error

    try:
        df = load_data_after_header(file_path)

        st.session_state.dataframe = df

        required_columns = ['YEAR', 'MO', 'DY', 'HR', 'ALLSKY_SFC_SW_DWN', 'PRECTOTCORR', 'WS50M', 'PS']

        for col in required_columns:
            if col not in df.columns:
                is_valid = False
                error = f"Die erforderliche Spalte '{col}' fehlt in den Daten."
                return is_valid, error

        total_unique_dates = df[['YEAR', 'MO', 'DY']].drop_duplicates().shape[0]
        if total_unique_dates < 365:
            is_valid = False
            error = "Die Datei muss Daten für ein ganzes Jahr enthalten."

    except Exception as e:
        is_valid = False
        error = f"Fehler beim Lesen der Datei: {str(e)}"

    return is_valid, error


def display_video():
    video_file_path = "pages/content/video_base64.txt"

    try:
        with open(video_file_path, "r") as file:
            video_base64 = file.read()

        video_bytes = base64.b64decode(video_base64)

        st.video(video_bytes)
    except FileNotFoundError:
        st.error(f"Die Datei '{video_file_path}' wurde nicht gefunden.")
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")

@st.cache_data
def plot_example_graph():
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    def generate_monthly_data():
        months = pd.date_range("2023-01-01", periods=12, freq="ME")
        solar = np.random.uniform(50, 200, 12)
        wind = np.random.uniform(100, 300, 12)
        rain = np.random.uniform(0, 200, 12)
        pressure = np.random.uniform(950, 1050, 12)
        return pd.DataFrame(
            {
            "Month": months,
            "Solar": solar,
            "Wind": wind,
            "Regen": rain,
            "Druck": pressure
            }
        )

    data = generate_monthly_data()

    fig, ax = plt.subplots(figsize=(15, 6))

    ax.plot(data["Month"], data["Solar"], marker="o", label="Solar")
    ax.plot(data["Month"], data["Wind"], marker="o", label="Wind")
    ax.plot(data["Month"], data["Regen"], marker="o", label="Regen")
    ax.plot(data["Month"], data["Druck"], marker="o", label="Druck")

    ax.set_title("Wetterdaten (Beispieldaten)")
    ax.set_xlabel("Monat")
    ax.set_ylabel("Wert")
    ax.legend()
    ax.grid()

    return fig