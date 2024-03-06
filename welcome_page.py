# pages/description.py
import streamlit as st

def app():
    st.title('Welcome')
    st.title(' ')
    
    col1, col2 = st.columns(2)

    with col1:
        st.write('''
        ##### I. Create new lesson manually
        1. Create a .txt file in the `lessons` directory. The name of the file will be visible in the dropdown menu.
        2. In that file, each section must be separated:
        ```
        section title
        - explanation
        - example

        section title
        - explanation
        - example
        ```
        3. You can include any number of sections
        4. Each section must have a title. The names of the titles will be visible in the dropdown menu.
        5. Save the file.
        6. Lesson should be visible in the dropdown menu.
        ''')

    with col2:
        st.write('''
        ##### II. Create new lesson using Bing's Copilot
        1. Copy the prompt below to the [Bing's Copilot](bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx) and replace the "abc":
        ```
        1. Create a lesson plan for the "abc".
        2. Include section titles: "abc", "abc", "abc", and "abc".

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
        2. Create a .txt file in the `lessons` directory. The name of the file will be visible in the dropdown menu.
        3. Copy the created lesson plan in Bing's Copilot, and paste it to that file.
        4. Save the file, lesson should be visible in the dropdown menu.
        ''')
