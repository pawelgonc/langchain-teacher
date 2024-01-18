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

def navigation():
    st.sidebar.title('Navigation')
    # Get the current page selection
    st.session_state["current_selection"] = st.sidebar.radio("Go to", list(PAGES.keys()))

def main():
    print("Before main: ", st.session_state)  # Debugging print statement
    # Initialize the session state for 'Teacher'
    if "teacher" not in st.session_state:
        st.session_state.teacher = {}
    if "teacher_current_lesson" not in st.session_state:
        st.session_state["teacher_current_lesson"] = None
    if "teacher_current_section" not in st.session_state:
        st.session_state["teacher_current_section"] = None
    if "teacher_current_lesson_file" not in st.session_state:
        st.session_state["teacher_current_lesson_file"] = None
    if "teacher_chat_history" not in st.session_state:
        st.session_state["teacher_chat_history"] = []

    # Initialize the session state for 'Creator'
    if "creator" not in st.session_state:
        st.session_state.creator = {}
    if "creator_current_lesson" not in st.session_state:
        st.session_state["creator_current_lesson"] = None
    if "creator_current_section" not in st.session_state:
        st.session_state["creator_current_section"] = None
    if "creator_current_lesson_file" not in st.session_state:
        st.session_state["creator_current_lesson_file"] = None
    if "creator_chat_history" not in st.session_state:
        st.session_state["creator_chat_history"] = []
    
    # Check if the page selection has changed
    if st.session_state.get("current_selection") != st.session_state["current_selection"]:
        # If the selection has changed, clear the messages
        st.session_state["messages"] = []
        # Update the current selection
        st.session_state["current_selection"] = st.session_state["current_selection"]

    # Load the selected page
    page = PAGES[st.session_state["current_selection"]]
    page.app()

    print("After main: ", st.session_state)  # Debugging print statement

# Call the navigation function before main
navigation()
main()