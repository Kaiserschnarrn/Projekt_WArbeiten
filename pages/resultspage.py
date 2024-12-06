import streamlit as st

def results_page():
    st.markdown("<h1 style='text-align: center;'>Ergebnisse</h1>", unsafe_allow_html=True)

    # Display the results here
    st.write("This is where the results will be displayed.")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück zur Parameterauswahl"):
            st.session_state.page = "Parameterauswahl"
    with col2:
        if st.button("Zurück zur Startseite"):
            st.session_state.page = "Start"
