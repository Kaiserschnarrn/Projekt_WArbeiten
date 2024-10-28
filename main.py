import streamlit as st
import pandas as pd

# Laden der CSV-Datei
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


# Hauptfunktion der Streamlit-App
def main():
    st.title('CSV Datei Visualisierung')

    # Datei-Upload
    uploaded_file = st.file_uploader('Wählen Sie eine CSV-Datei aus', type='csv')

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.write('Daten aus der CSV-Datei:')
        st.dataframe(data)

        # Beispiel für eine einfache Visualisierung
        st.line_chart(data)


if __name__ == '__main__':
    main()
