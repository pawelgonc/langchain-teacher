# app.py

import streamlit as st
import teacher, lesson_creator

PAGES = {
    "Teacher": teacher,
    "Lesson Creator": lesson_creator
}

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()
