from pages.fileuploadpage import file_upload_page
from pages.parameterselectionpage import parameter_selection_page
from pages.resultspage import results_page
from pages.startpage import start_page
from utils import *

# Statische Pfade und Konstanten
DATA_DIRECTORY = "./data"
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)
STATIC_FILE_PATH = os.path.join(DATA_DIRECTORY, "NASA_Data.csv")
LAST_USED_DIRECTORY = os.path.join(DATA_DIRECTORY, "last_used")
if not os.path.exists(LAST_USED_DIRECTORY):
    os.makedirs(LAST_USED_DIRECTORY)
WINDRAD_IMAGE_PATH = os.path.abspath("windrad.gif")

# Funktion: Hauptlogik
def main():
    if "page" not in st.session_state:
        st.session_state.page = "Start"
        footer()

    if st.session_state.page == "Start":
        start_page()
        footer()
    elif st.session_state.page == "Dateiauswahl":
        file_upload_page(LAST_USED_DIRECTORY, WINDRAD_IMAGE_PATH, STATIC_FILE_PATH)
        footer()
    elif st.session_state.page == "Parameterauswahl":
        parameter_selection_page(STATIC_FILE_PATH)
        footer()
    elif st.session_state.page == "Ergebnisse":
        results_page()
        footer()


if __name__ == "__main__":
    main()
