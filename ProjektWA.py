import os
import streamlit as st
from pages.startpage import start_page
from pages.fileuploadpage import file_upload_page
from pages.parameterselectionpage import parameter_selection_page
from pages.resultspage import results_page
from pages.manual import manual_page
from utils import footer

DATA_DIRECTORY = "./data"
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)
LAST_USED_DIRECTORY = os.path.join(DATA_DIRECTORY, "last_used")
if not os.path.exists(LAST_USED_DIRECTORY):
    os.makedirs(LAST_USED_DIRECTORY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WINDRAD_IMAGE_PATH = os.path.join(BASE_DIR, "windrad.gif")
manual_pdf_path = "pages/content/Handbuch zum Tool.pdf"

def main():
    if "page" not in st.session_state:
        st.session_state.page = "Start"
        footer()

    if st.session_state.page == "Start":
        start_page()
        footer()
    elif st.session_state.page == "Manual":
        manual_page(manual_pdf_path)
        footer()
    elif st.session_state.page == "Dateiauswahl":
        file_upload_page(LAST_USED_DIRECTORY, WINDRAD_IMAGE_PATH)
        footer()
    elif st.session_state.page == "Parameterauswahl":
        parameter_selection_page()
        footer()
    elif st.session_state.page == "Ergebnisse":
        results_page()
        footer()

if __name__ == "__main__":
    main()
