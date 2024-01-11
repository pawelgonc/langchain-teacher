
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langsmith import Client
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
import os
from teacher_prompt import load_section_prompt

def app():
    st.title('Teacher')
    button_css = """.stButton>button {
        color: #4F8BF9;
        border-radius: 50%;
        height: 2em;
        width: 2em;
        font-size: 4px;
    }"""
    st.markdown(f'<style>{button_css}</style>', unsafe_allow_html=True)

    class StreamHandler(BaseCallbackHandler):
        def __init__(self, container, initial_text=""):
            self.container = container
            self.text = initial_text

        def on_llm_new_token(self, token: str, **kwargs) -> None:
            self.text += token
            self.container.markdown(self.text)

    class Lesson:
        def get_next_section_content(self):
            if self.active_section_index < len(self.lesson_sections):
                next_section_title = self.lesson_sections[self.active_section_index]
                next_section_content = getattr(self, next_section_title)
                return next_section_title, next_section_content
            else:
                return None, None  # No more lesson_sections
            
        def __init__(self, filename):
            self.filename = filename
            self.lesson_sections = []  # Initialize as empty list
            self.active_section_index = 0
            self.load_content()

        def update_current_section(self):
            if self.active_section_index < len(self.lesson_sections):
                self.active_section = self.lesson_sections[self.active_section_index]
                self.active_section_index += 1
            else:
                self.active_section = None  # No more lesson_sections

        def load_content(self):
            with open(f"lessons/{self.filename}", "r") as file:
                content = file.read()
                sections = content.split("-----")
                for i, section in enumerate(sections):
                    section = section.strip()
                    if section:  # Ignore empty sections
                        if "\n----" in section:  # Check if the section has subsections
                            section_title, subsections = section.split("\n----", 1)
                            subsections = self.parse_subsections(subsections, "----")
                            self.lesson_sections.append(section_title.strip())
                            setattr(self, section_title.strip(), subsections)
                        else:
                            section_title, section_content = section.split("\n", 1)
                            self.lesson_sections.append(section_title.strip())
                            setattr(self, section_title.strip(), section_content.strip())

        def parse_subsections(self, subsections, separator):
            if "\n" + separator[:-1] in subsections:  # Check if the subsections have further nested sections
                subsection_title, nested_subsections = subsections.split("\n" + separator[:-1], 1)
                nested_subsections = self.parse_subsections(nested_subsections, separator[:-1])
                return {subsection_title.strip(): nested_subsections}
            else:
                return subsections.split("\n")

        def display(self):
            for section_title in self.lesson_sections[:3]:  # Iterate over the first three sections
                section_content = getattr(self, section_title)
                st.markdown(f"**{section_title}**")
                st.write(section_content)

        def set_section(self, section_title):
            if section_title in self.lesson_sections:
                self.active_section_index = self.lesson_sections.index(section_title)
                self.update_current_section()
            else:
                print(f"Section '{section_title}' not found in lesson.")

        def get_section_names(self):
            return self.lesson_sections
        
    def handle_user_input():
        if user_input := st.chat_input():
            st.chat_message("user").write(user_input)
            return user_input
        return None

    def get_prompt_template(current_lesson):
        prompt_template = load_section_prompt(current_lesson)
        return prompt_template

    def get_llm_chain(prompt_template):
        stream_handler = StreamHandler(st.empty())
        model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-3.5-turbo-16k")
        chain = LLMChain(prompt=prompt_template, llm=model)
        return chain

    def get_response(chain, user_input):
        response = chain(
            {"input": user_input, "chat_history": st.session_state.messages[-20:]},
            include_run_info=True,
            tags=[current_lesson.filename]  # removed selected_lesson_type
        )
        return response

    def update_messages(user_input, response, chain):
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.session_state.messages.append(AIMessage(content=response[chain.output_key]))

    def handle_assistant_response(user_input, current_lesson):
        # Check if the user's input contains a command to switch sections
        if user_input.startswith("switch to "):
            section_title = user_input[len("switch to "):]
            current_lesson.set_section(section_title)
        else:
            current_lesson.update_current_section()  # Update current_section before using it

        with st.chat_message("assistant"):
            prompt_template = get_prompt_template(current_lesson)
            chain = get_llm_chain(prompt_template)
            response = get_response(chain, user_input)
            update_messages(user_input, response, chain)
            run_id = response["__run"].run_id

            display_feedback_buttons(run_id)  # Display feedback buttons after assistant's response

    def display_feedback_buttons(run_id):
        col_blank, col_text, col1, col2 = st.columns([10, 2, 1, 1])
        with col_text:
            st.text("Feedback:")

        with col1:
            st.button("👍", on_click=send_feedback, args=(run_id, 1))

        with col2:
            st.button("👎", on_click=send_feedback, args=(run_id, 0))

    def initialize_state():
        if st.session_state.get("current_lesson") != selected_lesson_file:
            st.session_state["current_lesson"] = selected_lesson_file
            welcome_message = f"Once you are prepared, we shall begin our exploration of {selected_lesson_file}. I will be your guide throughout this intellectual journey."
            st.session_state["messages"] = [AIMessage(content=welcome_message)]

    # Message handling and interaction
    def send_feedback(run_id, score):
        langsmith_client.create_feedback(run_id, "user_score", score=score)

    def display_messages():
        for msg in st.session_state["messages"]:
            if isinstance(msg, HumanMessage):
                st.chat_message("user").write(msg.content)
            else:
                st.chat_message("assistant").write(msg.content)
    
    def format_section_content(content, separator="----"):
        formatted_content = ""
        if isinstance(content, dict):
            for key, value in content.items():
                formatted_content += key.replace(separator, "") + "\n"
                formatted_content += format_section_content(value, separator[:-1])
        elif isinstance(content, list):
            for item in content:
                formatted_content += format_section_content(item, separator)
        else:  # content is a string
            formatted_content += content.replace(separator, "") + "\n"
        return formatted_content

    # Initialize LangSmith langsmith_client
    langsmith_client = Client()

    # Get all current_lesson files in the lessons directory
    lesson_files = os.listdir("lessons")

    # Lesson selection sidebar
    selected_lesson_file = st.sidebar.selectbox("Select Lesson", os.listdir("lessons"))

    # Create a new Lesson object
    current_lesson = Lesson(selected_lesson_file)
    # Display the title, background and prerequisites, and learning objectives
    current_lesson.display()

    # Dropdown menu for section selection
    selected_section = st.sidebar.selectbox("Select Section", current_lesson.get_section_names(), key='section_select')
    # Display the content of the selected section
    section_content = getattr(current_lesson, selected_section)
    formatted_content = format_section_content(section_content)
    st.sidebar.markdown(formatted_content)

    initialize_state()

    display_messages()

    # Handle user input and assistant responses
    if user_input := handle_user_input():
        handle_assistant_response(user_input, current_lesson)
