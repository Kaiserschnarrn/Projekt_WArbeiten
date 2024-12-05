from datetime import datetime
import streamlit as st
from utils import *

def parameter_selection_page(STATIC_FILE_PATH):
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
        df = load_data_after_header(STATIC_FILE_PATH)
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
