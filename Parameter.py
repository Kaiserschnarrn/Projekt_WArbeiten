import streamlit as st
from datetime import date
import pandas as pd

def main():
    st.title("Parameter für den gewünschten Output setzen")

    st.markdown("---")

    # Optionen und Parameter
    st.subheader("Wählen Sie die gewünschten Optionen und Parameter aus")

    # Multiple Choice Optionen
    options = ["Wort Case", "Best Case"]
    selected_options = st.multiselect("Optionen:", options)

    # Zeiträume für spezifische Ereignisse
    events = ["Nullpunkt/Dunkelflaute", "Hitzewelle", "Dauerregen", "Sturm"]
    selected_events = {}
    any_event_selected = False  # Flag, um zu prüfen, ob mindestens ein Zeitraum ausgewählt wurde

    for event in events:
        with st.expander(f"{event} von/bis"):
            col1, col2 = st.columns(2)
            start_date = col1.date_input(f"{event} Startdatum", key=f"{event}_start", value=None)
            end_date = col2.date_input(f"{event} Enddatum", key=f"{event}_end", value=None)
            selected_events[event] = {'start': start_date, 'end': end_date}

            # Prüfen, ob Start- und Enddatum ausgewählt wurden
            if start_date and end_date:
                any_event_selected = True

    # Überprüfen, ob mindestens eine Option oder ein Zeitraum ausgewählt wurde
    is_option_selected = len(selected_options) > 0 or any_event_selected

    # 'Weiter' Button
    next_button = st.button("Weiter", disabled=not is_option_selected)

    if not is_option_selected:
        st.warning("Bitte wählen Sie mindestens eine Option oder einen Zeitraum aus.")

    # Wenn 'Weiter' geklickt wurde
    if next_button:
        # Parameter speichern
        st.session_state['parameters'] = {
            'options': selected_options,
            'events': selected_events
        }
        st.success("Parameter wurden erfolgreich gespeichert. Ergebnisse werden unten angezeigt.")

        # Verarbeitung und Darstellung
        verarbeitung_und_darstellung()

def verarbeitung_und_darstellung():
    st.markdown("---")
    st.header("Verarbeitung und Darstellung")

    if 'parameters' in st.session_state:
        parameters = st.session_state['parameters']
        options = parameters['options']
        events = parameters['events']

        st.write("**Ausgewählte Optionen:**", options)

        st.write("**Ausgewählte Ereignisse und Zeiträume:**")
        for event, dates in events.items():
            start = dates['start']
            end = dates['end']
            if start and end:
                st.write(f"- {event}: von {start} bis {end}")

        # Beispielhafte Verarbeitung
        st.subheader("Ergebnisse der Verarbeitung")
        st.write("Die Verarbeitung erfolgt basierend auf den ausgewählten Parametern.")
        # Hier können Sie Ihren Verarbeitungs-Code einfügen
    else:
        st.error("Keine Parameter gefunden.")

if __name__ == "__main__":
    main()
