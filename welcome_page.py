# pages/description.py
import streamlit as st

def app():
    st.title('Welcome')
    st.write('''
             
1. Here is the prompt you can copy to the [GPT-4 in Bing](bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx):             
```
1. Create a lesson plan for the "abc".
2. Include points/topics: "abc", "abc", "abc", and "abc".

3. Details:
a. This lesson plan must follow this structure:
point/topic
- explanation
- example
b.
1. Repeat the above structure for each point/topic.
2. Replace the "point/topic" with the appropriate name.
3. Separate each "point/topic" section using newline insert.
4. Lesson plan must be in the format of code block.
```
2. Create a .txt file in the "lessons" directory with the name of the lesson.
3. Insert the created lesson plan to that file.
''')
