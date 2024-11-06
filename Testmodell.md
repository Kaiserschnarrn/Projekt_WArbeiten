import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Funktion zum Laden von Wetterdaten aus einer CSV-Datei
def load_weather_data(file):
    df = pd.read_csv(file, skiprows=15)
    return df


# Hauptfunktion
def main():
    st.title("Wetterdaten- und Szenarien-Tool")
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Bitte Seite wählen",
                                ["Hauptseite", "Upload Daten", "Szenarienauswahl", "Simulationsmöglichkeit",
                                 "Überblick"])

    if page == "Hauptseite":
        main_page()
    elif page == "Upload Daten":
        upload_data_page()
    elif page == "Szenarienauswahl":
        scenario_page()
    elif page == "Simulationsmöglichkeit":
        simulation_results()
    elif page == "Überblick":
        overview_page()


def main_page():
    st.write("Herzlich Willkommen zu unserem selbsterstellten Tool zur Analyse von Wetterdaten.")
    st.write("Um Ihre Wetterdaten hochzuladen, wählen Sie bitte die Rubrik Upload.")
    st.write("Um mögliche Szenarien durchzuspielen, gehen Sie bitte in die Rubrik Szenarienauswahl.")
    st.write("Um sich Simulationen anzuschauen, gehen Sie bitte in die Rubrik Simulation.")


def upload_data_page():
    st.title("CSV-Datei hochladen")
    uploaded_file = st.file_uploader("Wählen Sie eine CSV-Datei für den Upload aus", type="csv")

    if uploaded_file is not None:
        try:
            # Daten laden
            df = load_weather_data(uploaded_file)
            st.session_state.df = df  # Speichern der Daten in der Sitzung
            st.success("Daten erfolgreich hochgeladen!")

            # Anzeige der ersten fünf Zeilen der Daten
            st.dataframe(df.head())

            if st.button("Weiter zu Szenarien"):
                st.session_state.page = "Szenarienauswahl"  # Navigiere zur Szenarienauswahl-Seite
                scenario_page()

        except Exception as e:
            st.error(f"Fehler beim Laden der Datei: {e}")


def scenario_page():
    st.title("Entwicklung von Szenarien")
    st.write("Erstellen Sie benutzerdefinierte Wetterbedingungen.")

    # Dropdown für Szenarien
    scenario_options = ['Viel Sonne', 'Viel Wind', 'Viel Regen']
    selected_scenario = st.selectbox("Wählen Sie ein Szenario aus:", scenario_options)

    # Eingabefeld für die Dunkelflaute, nun auch mit 0 Tagen möglich
    dark_spell_duration = st.number_input("Dauer der Dunkelflaute (in Tagen):", min_value=0, max_value=10, value=0)

    if st.button("Szenario speichern"):
        st.session_state.dark_spell_duration = dark_spell_duration
        st.session_state.selected_scenario = selected_scenario
        st.success("Szenario wurde erfolgreich gespeichert!")
        st.session_state.page = "Simulationsmöglichkeit"  # Navigiere zur Simulation-Seite
        simulation_results()


def simulation_results():
    st.title("Simulationsergebnisse")
    if 'dark_spell_duration' not in st.session_state or 'selected_scenario' not in st.session_state:
        st.warning("Bitte speichern Sie ein Szenario, bevor Sie die Simulationsergebnisse anzeigen.")
        return

    st.write(
        f"Simulation für {st.session_state.dark_spell_duration} Tage Dunkelflaute mit dem Szenario '{st.session_state.selected_scenario}'.")

    # Beispielhafte Berechnung und Anzeige von Ergebnissen
    base_output = st.session_state.dark_spell_duration * 1.5  # Dummy-Berechnung
    scenario_effect = calculate_scenario_effect(base_output, st.session_state.selected_scenario)
    st.write(f"Simulierte Auswirkung: {scenario_effect:.2f} kWh")

    # Grafik für die Simulationsergebnisse
    st.subheader("Simulationsergebnisse als Grafik")

    # Beispielhafte Werte für die Grafik
    days = range(0, st.session_state.dark_spell_duration + 1)  # Range von 0 bis Dunkelflaute
    outputs = [calculate_scenario_effect(day * 1.5, st.session_state.selected_scenario) for day in days]

    plt.figure(figsize=(10, 6))
    plt.plot(days, outputs, marker='o', linestyle='-', color='orange')
    plt.title(f"Simulierte Auswirkung der Dunkelflaute mit dem Szenario '{st.session_state.selected_scenario}'")
    plt.xlabel("Tage der Dunkelflaute")
    plt.ylabel("Simulierte Auswirkung (kWh)")
    plt.xticks(days)
    plt.grid()
    st.pyplot(plt)

    # Möglichkeit, die Ergebnisse als CSV zu speichern
    if st.button("Ergebnisse als CSV speichern"):
        results_df = pd.DataFrame({
            'Dunkelflaute (Tage)': days,
            'Simulierte Auswirkung (kWh)': outputs
        })
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='simulation_results.csv',
            mime='text/csv',
        )

    # PDF-Download (hier muss die PDF-Erstellung implementiert werden)
    if st.button("Ergebnisse als PDF speichern"):
        st.warning("PDF-Erstellung ist noch nicht implementiert.")

    if st.button("Zurück zur Hauptseite"):
        st.session_state.page = "Hauptseite"  # Zurück zur Hauptseite
        main_page()


def calculate_scenario_effect(base_output, scenario):
    """Berechnet die Auswirkungen des gewählten Szenarios."""
    if scenario == 'Viel Sonne':
        return base_output * 1.2  # Erhöhung um 20%
    elif scenario == 'Viel Wind':
        return base_output * 1.5  # Erhöhung um 50%
    elif scenario == 'Viel Regen':
        return base_output * 0.8  # Reduzierung um 20%
    return base_output


def overview_page():
    st.title("Überblick und Analyse")
    st.write("Zusammenfassung der gesammelten Daten und Simulationsergebnisse.")

    # Dummy-Daten für die Übersicht
    st.write("Trendanalysen... (Hier können Sie echte Datenanalysen hinzufügen)")

    if st.button("Zurück zur Hauptseite"):
        st.session_state.page = "Hauptseite"  # Zurück zur Hauptseite
        main_page()


if __name__ == "__main__":
    # Initialisierung des Streamlit-Sitzungsstatus
    if 'page' not in st.session_state:
        st.session_state.page = "Hauptseite"
    main()
