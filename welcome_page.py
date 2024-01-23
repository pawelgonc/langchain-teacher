# pages/description.py
import streamlit as st

def app():
    st.title('Welcome')
    st.write('''
1. Select the lesson from the menu, the teacher will teach the first topic from the lesson.

2. Browse the topics in the "Section Preview" menu.

3. Prompt the teacher with the section title to switch to that section.
After that, you can continue conversation and the prompt which you used to switch the section will disappear.''')
