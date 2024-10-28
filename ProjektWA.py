import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Datei laden und Parameter umbenennen
@st.cache_data
def load_data():
    # Absoluter Pfad zur Datei
    df = pd.read_csv('C:/Users/fatih/Projekt/ProjektWA/NASA.csv', skiprows=15)
    # Spaltennamen anpassen
    df.columns = [
        'Parameter', 'Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May',
        'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Annual'
    ]
    return df

# Daten laden
data = load_data()

# Titel und Beschreibung für das Tool
st.title("NASA POWER Wetter-Szenarien-Tool")
st.write("Analysieren und visualisieren Sie benutzerdefinierte Wetterdaten.")

# Parameter-Übersetzung für die Dropdown-Auswahl (nur die 4 Parameter aus dem Screenshot)
parameter_dict = {
    'PS': 'Luftdruck an der Oberfläche (kPa)',
    'WSC': 'Korrigierte Windgeschwindigkeit (angepasst für Höhe, m/s)',
    'WS50M': 'Windgeschwindigkeit in 50 m Höhe (m/s)',
    'ALLSKY_SFC_SW_DWN': 'Globalstrahlung an der Oberfläche (kWh/m²/Tag)',
}

# Auswahlfeld für Parameter mit erklärenden Bezeichnungen
parameter = st.selectbox(
    "Wählen Sie den Parameter zur Analyse",
    options=list(parameter_dict.keys()),
    format_func=lambda x: parameter_dict[x]
)

# Zeitspanne auswählen
year_range = st.slider(
    "Wählen Sie die Jahresperiode",
    int(data['Year'].min()),
    int(data['Year'].max()),
    (int(data['Year'].min()), int(data['Year'].max()))
)

# Filterung der Daten basierend auf Auswahl
filtered_data = data[(data['Parameter'] == parameter) & (data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

# Jährliche Durchschnittswerte visualisieren
if not filtered_data.empty:
    years = filtered_data['Year']
    annual_data = filtered_data['Annual']

    st.subheader(f"Jährliche Durchschnittswerte für {parameter_dict[parameter]} von {year_range[0]} bis {year_range[1]}")
    plt.figure(figsize=(10, 6))
    plt.plot(years, annual_data, marker='o', linestyle='-', color='orange')
    plt.title(f"Jährliche Durchschnittswerte für {parameter_dict[parameter]}")
    plt.xlabel("Jahr")
    plt.ylabel(f"{parameter_dict[parameter]}")
    plt.grid()
    st.pyplot(plt)
else:
    st.warning("Keine Daten für den ausgewählten Zeitraum und Parameter verfügbar.")

# Monatliche Durchschnittswerte visualisieren
st.subheader(f"Monatliche Durchschnittswerte für {parameter_dict[parameter]}")
monthly_means = filtered_data[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']].mean()

plt.figure(figsize=(10, 6))
monthly_means.plot(kind='bar', color='skyblue')
plt.title(f"Durchschnittliche monatliche Werte für {parameter_dict[parameter]}")
plt.xlabel("Monat")
plt.ylabel(f"{parameter_dict[parameter]}")
plt.xticks(rotation=45)
plt.grid()
st.pyplot(plt)

