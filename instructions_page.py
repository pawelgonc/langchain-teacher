# pages/description.py
import streamlit as st

def app():
    col1, col2 = st.columns(2)

    with col1:
        st.write('''
        ##### I. Custom lesson
        1. Create a .txt file in the **lessons** directory.
        2. In that file, each Section must have a title:
        ```
        title
        - ...

        title
        - ...
        - ...
        ```
        3. Each Section must be separated.
        4. You can include any number of Sections.
        5. Save the file.
        6. The lesson is now visible in the menu **Lesson**.
        ''')

    with col2:
        st.write('''
        ##### II. Create a lesson using AI
        1. Copy the prompt below to the [Bing's Copilot](https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx):
        ```
        1. Create a lesson for the xyz.
        2. Include sections: xyz, and xyz.

        3. Details:
        a. The lesson must follow this structure:
        section title
        - explanation
        - example
        b. Repeat the above structure for each section.
        c. Replace the "section title" with the appropriate name.
        d. Separate each section using newline insert.
        e. The lesson must be in the format of a code block.
        ```
        2. Create a .txt file in the **lessons** directory.
        3. Copy created Sections to that file.
        4. Save the file.
        5. The lesson is now visible in the menu **Lesson**.
        ''')
