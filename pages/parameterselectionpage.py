from datetime import datetime
import streamlit as st

def parameter_selection_page():
    st.markdown("<h2>Parameterauswahl</h2>", unsafe_allow_html=True)

    # Prüfen, ob die Daten im Session State vorhanden sind
    if "dataframe" not in st.session_state:
        st.error("Keine Daten im Speicher. Bitte zuerst eine Datei validieren und hochladen.")
        if st.button("Zurück zur Dateiauswahl"):
            st.session_state.page = "Dateiauswahl"
        return

    # Datenvorschau bleibt oben erhalten
    df = st.session_state.dataframe
    df['YEAR'] = df['YEAR'].astype(int)
    st.write("**Vorschau der ausgewählten Daten:**")
    st.dataframe(df.head(4).style.format({'YEAR': '{:.0f}'}), use_container_width=True)

    # Liste der Parameter mit neuen Namen
    parameters = ["Druck", "Wind", "Solar", "Regen"]
    scenarios = ["Best Case", "Worst Case", "Nullpunkt", "Hitzewelle", "Dauerregen", "Sturm"]

    # Szenarien, die für bestimmte Parameter deaktiviert werden sollen
    disabled_scenarios = {
        "Druck": ["Nullpunkt", "Hitzewelle", "Dauerregen", "Sturm"],
        "Wind": ["Hitzewelle", "Dauerregen"],
        "Solar": ["Dauerregen", "Sturm"],
        "Regen": ["Hitzewelle", "Sturm"]
    }

    # Session State für ausgewählten Parameter initialisieren
    if "selected_parameter" not in st.session_state:
        st.session_state.selected_parameter = parameters[0]  # Standardwert setzen
    if "selected_scenarios" not in st.session_state:
        st.session_state.selected_scenarios = {scenario: False for scenario in scenarios}

    # Ermitteln des verfügbaren Jahresbereichs
    unique_years = df["YEAR"].unique()
    selected_year = int(unique_years[0]) if len(unique_years) == 1 else min(unique_years)

    # Parameter-Auswahl als Radiobuttons
    st.markdown("### Parameter auswählen:")
    selected_parameter = st.radio(
        "Wählen Sie einen Parameter aus:",
        options=parameters,
        index=parameters.index(st.session_state.selected_parameter)
        if st.session_state.selected_parameter else 0
    )
    st.session_state.selected_parameter = selected_parameter

    # Zeige den aktuell ausgewählten Parameter
    st.markdown(f"### Szenarien konfigurieren ({selected_parameter})")

    # Konfiguration der Szenarien für den ausgewählten Parameter
    for scenario in scenarios:
        is_disabled = scenario in disabled_scenarios.get(selected_parameter, [])
        st.session_state.selected_scenarios[scenario] = st.checkbox(
            f"{scenario} ({selected_parameter})",
            value=st.session_state.selected_scenarios.get(scenario, False),
            key=f"{selected_parameter}_{scenario}",
            disabled=is_disabled
        )

        # Interaktive Konfiguration für Szenarien (nur für bestimmte Szenarien)
        if st.session_state.selected_scenarios[scenario] and not is_disabled:
            if scenario not in ["Best Case", "Worst Case"]:
                st.markdown(f"**{scenario} für {selected_parameter} einstellen:**")
                col_input1, col_input2 = st.columns(2)
                with col_input1:
                    st.date_input(
                        f"Von ({scenario})",
                        key=f"{selected_parameter}_{scenario}_start",
                        value=datetime(selected_year, 1, 1),
                        min_value=datetime(selected_year, 1, 1),
                        max_value=datetime(selected_year, 12, 31)
                    )
                with col_input2:
                    st.date_input(
                        f"Bis ({scenario})",
                        key=f"{selected_parameter}_{scenario}_end",
                        value=datetime(selected_year, 12, 31),
                        min_value=datetime(selected_year, 1, 1),
                        max_value=datetime(selected_year, 12, 31)
                    )

    # Navigation
    col_buttons1, col_buttons2, col_buttons3, col_buttons4 = st.columns(4)
    with col_buttons1:
        if st.button("⬅️ Zurück zur Datei-Upload-Seite"):
            st.session_state.page = "Dateiauswahl"
    with col_buttons4:
        if st.button("Weiter zu den Ergebnissen ✅"):
            st.success("Szenarien wurden gespeichert. Weiterleitung ...")
            st.session_state.page = "Ergebnisse"
