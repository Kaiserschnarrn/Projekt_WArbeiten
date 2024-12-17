import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def results_page():
    st.markdown("<h2>Ergebnisse</h2>", unsafe_allow_html=True)

    # Prüfen, ob die notwendigen Daten im Session State vorhanden sind
    if "dataframe" not in st.session_state or "selected_parameter" not in st.session_state:
        st.error("Keine gültigen Parameter oder Daten gefunden. Bitte zuerst Szenarien konfigurieren.")
        if st.button("⬅️ Zurück zur Parameterauswahl"):
            st.session_state.page = "Parameterauswahl"
        return

    # Daten und ausgewählte Einstellungen abrufen
    df = st.session_state.dataframe
    selected_parameter = st.session_state.selected_parameter
    selected_scenarios = st.session_state.selected_scenarios

    # Mapping der Parameter zu Spaltennamen
    parameter_mapping = {
        "Wind": "WS50M",
        "Solar": "ALLSKY_SFC_SW_DWN",
        "Regen": "PRECTOTCORR",
        "Druck": "PS"
    }

    # Szenario-Beschränkungen
    disabled_scenarios = {
        "Druck": ["Nullpunkt", "Hitzewelle", "Dauerregen", "Sturm"],
        "Wind": ["Hitzewelle", "Dauerregen"],
        "Solar": ["Dauerregen", "Sturm"],
        "Regen": ["Hitzewelle", "Sturm"]
    }

    # Überprüfen, ob der ausgewählte Parameter im Mapping enthalten ist
    if selected_parameter in parameter_mapping:
        column_name = parameter_mapping[selected_parameter]
    else:
        st.error(f"Der Parameter '{selected_parameter}' ist nicht bekannt.")
        if st.button("⬅️ Zurück zur Parameterauswahl"):
            st.session_state.page = "Parameterauswahl"
        return

    # Verfügbare Spalten im DataFrame prüfen
    available_columns = df.columns.tolist()
    if column_name not in available_columns:
        st.error(f"Die Spalte für den Parameter '{selected_parameter}' ('{column_name}') ist in den Daten nicht verfügbar.")
        st.write("**Verfügbare Parameter:")
        st.write(available_columns)
        if st.button("⬅️ Zurück zur Parameterauswahl"):
            st.session_state.page = "Parameterauswahl"
        return

    # Initiale Darstellung der Jahreswerte
    st.markdown("### Jahreswerte")
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_avg = df.groupby("MO")[column_name].mean()
    ax.plot(monthly_avg.index, monthly_avg.values, marker='o')
    ax.set_title(f"Durchschnittlicher Monatswert von {selected_parameter}")
    ax.set_xlabel("Monat")
    ax.set_ylabel(column_name)
    ax.grid(True)
    st.pyplot(fig)

    # Zeige eine Zusammenfassung der Auswahl
    st.markdown("### Zusammenfassung der Szenarien")
    st.write(f"**Ausgewählter Parameter:** {selected_parameter} ({column_name})")

    active_scenarios = [scenario for scenario, active in selected_scenarios.items() if active]
    if not active_scenarios:
        st.warning("Keine Szenarien wurden aktiviert. Bitte zur Parameterauswahl zurückkehren.")
        if st.button("⬅️ Zurück zur Parameterauswahl"):
            st.session_state.page = "Parameterauswahl"
        return

    st.write(f"**Aktivierte Szenarien:** {', '.join(active_scenarios)}")

    # Ergebnisse für jedes aktivierte Szenario berechnen und anzeigen
    for scenario in active_scenarios:
        st.markdown(f"#### Ergebnisse für Szenario: {scenario}")

        if scenario == "Best Case":
            best_value = df[column_name].max()
            best_month = df[df[column_name] == best_value][["YEAR", "MO"]].iloc[0]
            st.write(f"Der beste Monat für '{selected_parameter}' ist {int(best_month['MO'])}/{int(best_month['YEAR'])} mit einem Wert von {best_value}.")
        elif scenario == "Worst Case":
            worst_value = df[column_name].min()
            worst_month = df[df[column_name] == worst_value][["YEAR", "MO"]].iloc[0]
            st.write(f"Der schlechteste Monat für '{selected_parameter}' ist {int(worst_month['MO'])}/{int(worst_month['YEAR'])} mit einem Wert von {worst_value}.")
        else:
            # Filterung oder Berechnungen basierend auf Szenario und Parameter
            start_date = pd.to_datetime(st.session_state.get(f"{selected_parameter}_{scenario}_start"))
            end_date = pd.to_datetime(st.session_state.get(f"{selected_parameter}_{scenario}_end"))

            if start_date and end_date:
                st.write(f"Zeitraum: {start_date.date()} bis {end_date.date()}")

                # Erstellen einer Kopie der Daten für die Simulation
                simulated_df = df.copy()
                simulated_df["DATE"] = pd.to_datetime(simulated_df["YEAR"].astype(str) + "-" + simulated_df["MO"].astype(str) + "-" + simulated_df.get("DY", 1).astype(str), errors='coerce')

                if scenario == "Nullpunkt":
                    simulated_df.loc[(simulated_df["DATE"] >= start_date) & (simulated_df["DATE"] <= end_date), column_name] = 0
                    st.write("Simulation: Werte auf Null gesetzt.")
                elif scenario == "Hitzewelle":
                    max_value = simulated_df[column_name].max()
                    simulated_df.loc[(simulated_df["DATE"] >= start_date) & (simulated_df["DATE"] <= end_date), column_name] = max_value
                    st.write("Simulation: Werte auf maximal gesetzt.")
                elif scenario == "Dauerregen":
                    max_value = simulated_df[column_name].max()
                    simulated_df.loc[(simulated_df["DATE"] >= start_date) & (simulated_df["DATE"] <= end_date), column_name] = max_value
                    st.write("Simulation: Dauerregen simuliert.")
                elif scenario == "Sturm":
                    max_value = simulated_df[column_name].max()
                    simulated_df.loc[(simulated_df["DATE"] >= start_date) & (simulated_df["DATE"] <= end_date), column_name] = max_value
                    st.write("Simulation: Sturm simuliert.")

                # Darstellung der Daten als Graph (Simulation separat für jedes Szenario)
                simulated_monthly_avg = simulated_df.groupby(simulated_df["DATE"].dt.month)[column_name].mean()

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(simulated_monthly_avg.index, simulated_monthly_avg.values, marker='x', linestyle="--", label=f"{scenario} Simulation")
                ax.set_title(f"Szenario: {scenario} für {selected_parameter}")
                ax.set_xlabel("Monat")
                ax.set_ylabel(column_name)
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

                # Button nur für CSV-Download der simulierten Daten
                csv_buffer = BytesIO()
                simulated_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                st.download_button(
                    label=f"📥 Simulierte Daten für {scenario} herunterladen",
                    data=csv_buffer,
                    file_name=f"simulierte_daten_{scenario}_{selected_parameter}.csv",
                    mime="text/csv",
                    key=f"download_{scenario}_csv"
                )

    # Navigation
    col_buttons1, col_buttons2, col_buttons3, col_buttons4 = st.columns(4)
    with col_buttons1:
        if st.button("⬅️ Zurück zur Parameterauswahl"):
            st.session_state.page = "Parameterauswahl"
    with col_buttons4:
        if st.button("Zurück zur Startseite 🔃"):
            st.session_state.page = "Start"
