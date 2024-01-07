# app.py

import streamlit as st
import teacher, creator, description

PAGES = {
    "Description": description,
    "Lesson Creator": creator,
    "Teacher": teacher,
}

def main():
    # Initialize the session state for 'Teacher' and 'Lesson Creator'
    if "teacher" not in st.session_state:
        st.session_state.teacher = {}
    if "lesson_creator" not in st.session_state:
        st.session_state.creator = {}

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()