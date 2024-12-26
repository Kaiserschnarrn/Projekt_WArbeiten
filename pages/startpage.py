from utils import display_video, plot_example_graph
import streamlit as st

def start_page(video_file_path):
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

        st.subheader("📹 Video-Tutorial")
        display_video(video_file_path)

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
