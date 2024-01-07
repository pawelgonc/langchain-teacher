
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

st.set_page_config(page_title="LangChain: Custom Lesson", page_icon="🦜")

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
        def __init__(self, filename):
            self.filename = filename
            self.lesson_sections = ["title", "background_and_prerequisites", "learning_objectives", "content_delivery", "introduction", "main_points", "conclusion", "next_steps"]
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
                lesson_sections = content.split("-----")
                self.title = lesson_sections[1].strip()
                self.background_and_prerequisites = lesson_sections[2].strip()
                self.learning_objectives = lesson_sections[3].strip()
                self.content_delivery = lesson_sections[4].strip()
                self.introduction = lesson_sections[5].strip()
                self.main_points = self.parse_main_points(lesson_sections[6])
                self.conclusion = lesson_sections[7].strip()
                self.next_steps = lesson_sections[8].strip()

        def parse_main_points(self, main_points_section):
            main_points = main_points_section.split("\n-----")
            return [point.strip() for point in main_points]
        
        def display(self):
            st.markdown(f"**{self.title}**")
            st.write(self.background_and_prerequisites)
            st.write(self.learning_objectives)
        
        def set_section(self, section_title):
            if section_title in self.lesson_sections:
                self.active_section_index = self.lesson_sections.index(section_title)
                self.update_current_section()
            else:
                print(f"Section '{section_title}' not found in lesson.")

    def handle_user_input():
        if user_input := st.chat_input():
            st.chat_message("user").write(user_input)
            return user_input
        return None

    def get_prompt_template(current_lesson):
        # Use the general prompt template for the current section
        prompt_template = load_section_prompt(current_lesson.active_section, getattr(current_lesson, current_lesson.active_section))
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
            tags=[current_lesson.filename, selected_lesson_type]
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
        if st.session_state.get("current_lesson") != selected_lesson_file or st.session_state.get("current_lesson_type") != selected_lesson_type:
            st.session_state["current_lesson"] = selected_lesson_file
            st.session_state["current_lesson_type"] = selected_lesson_type
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

    # Radio buttons for current_lesson type selection
    selected_lesson_type = st.sidebar.radio("Select Lesson Type", ["Instructions based lesson", "Interactive lesson with questions"])

    initialize_state()

    display_messages()

    # Handle user input and assistant responses
    if user_input := handle_user_input():
        handle_assistant_response(user_input, current_lesson)
