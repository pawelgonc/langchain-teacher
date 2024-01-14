# app.py

import streamlit as st
import teacher, creator, description

# Set the page config
st.set_page_config(page_title="LangChain", page_icon="🦜")

PAGES = {
    "Description": description,
    "Lesson Creator": creator,
    "Teacher": teacher,
}

def main():
    # Initialize the session state for 'Teacher'
    if "teacher" not in st.session_state:
        st.session_state.teacher = {}
    if "teacher_current_lesson" not in st.session_state:
        st.session_state["teacher_current_lesson"] = None
    if "teacher_current_section" not in st.session_state:
        st.session_state["teacher_current_section"] = None
    if "teacher_current_lesson_file" not in st.session_state:
        st.session_state["teacher_current_lesson_file"] = None

    # Initialize the session state for 'Creator'
    if "creator" not in st.session_state:
        st.session_state.creator = {}
    if "creator_current_lesson" not in st.session_state:
        st.session_state["creator_current_lesson"] = None
    if "creator_current_section" not in st.session_state:
        st.session_state["creator_current_section"] = None
    if "creator_current_lesson_file" not in st.session_state:
        st.session_state["creator_current_lesson_file"] = None

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()