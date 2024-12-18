from utils import *

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

    st.pyplot(plot_example_graph())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Zum Handbuch 📖"):
            st.session_state.page = "Manual"

    with col4:
        if st.button("🚀 Wetterapp starten"):
            st.session_state.page = "Dateiauswahl"

# Grafik als Beispiel
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
