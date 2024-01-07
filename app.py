# app.py

import streamlit as st
import teacher, creator, description

PAGES = {
    "Description": description,
    "Lesson Creator": creator,
    "Teacher": teacher,
}

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()