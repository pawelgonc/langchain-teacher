# pages/description.py
import streamlit as st

def app():
    col1, col2 = st.columns(2)

    with col1:
        st.write('''
        ##### I. Create new lesson manually
        1. Create a .txt file in the **lessons** directory.
        2. In that file, each section must be separated:
        ```
        title
        - ...

        title
        - ...
        - ...
        ```
        3. You can include any number of sections
        4. Each section must have a title.
        5. Save the file.
        6. The lesson is now visible in the menu **Lesson**.
        ''')

    with col2:
        st.write('''
        ##### II. Create new lesson using Bing's Copilot
        1. Copy the prompt below to the [Bing's Copilot](https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx) and replace the "abc":
        ```
        1. Create a lesson plan for the "abc".
        2. Include sections: "abc", and "abc".

        3. Details:
        a. This lesson plan must follow this structure:
        section title
        - explanation
        - example
        b.
        1. Repeat the above structure for each section.
        2. Replace the "section title" with the appropriate name.
        3. Separate each section using newline insert.
        4. Lesson plan must be in the format of code block.
        ```
        2. Create a .txt file in the **lessons** directory.
        3. Copy the created **Sections** and paste them to that file.
        4. Save the file and the lesson will be visible in the menu **Lesson**.
        ''')
