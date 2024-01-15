
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
from creator_prompt import load_section_prompt

def app():
    st.title('Creator')
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
            self.active_section = None  # Initialize active_section attribute
            self.load_content()

        def update_current_section(self):
            if self.active_section_index < len(self.lesson_sections):
                print(f"Updating section from '{self.active_section}' to '{self.lesson_sections[self.active_section_index]}'") #debugg
                self.active_section = self.lesson_sections[self.active_section_index]
                self.active_section_index += 1
            else:
                self.active_section = None  # No more lesson_sections
                print("No more sections to update.") #debugg

        def load_data(self):
            with open(f"templates/{self.filename}", "r") as file:
                content = file.read()
            return content

        def parse_data(self, content):
            sections = content.split("\n\n")  # Use double newline as separator
            for i, section in enumerate(sections):
                section = section.strip()
                if section:  # Ignore empty sections
                    if "\n" in section:  # Check if section has a newline
                        section_title, section_content = section.split("\n", 1)
                        self.lesson_sections.append(section_title.strip())
                        setattr(self, section_title.strip(), section_content.strip())
                    else:
                        self.lesson_sections.append(section)
                        setattr(self, section, "")

        def load_content(self):
            content = self.load_data()
            self.parse_data(content)

        def set_section(self, section_title):
            if section_title in self.lesson_sections:
                print(f"Switching section from '{self.active_section}' to '{section_title}'") #debugg
                self.active_section_index = self.lesson_sections.index(section_title)
                self.update_current_section()
            else:
                print(f"Section '{section_title}' not found in template.")

        def get_section_names(self):
            return self.lesson_sections
        
    def handle_user_input():
        if user_input := st.chat_input():
            st.chat_message("user").write(user_input)
            return user_input
        return None

    def get_prompt_template(creator_current_lesson):
        prompt_template = load_section_prompt(st.session_state["creator_current_lesson"])
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
            tags=[st.session_state["creator_current_lesson"].filename]  # removed selected_lesson_type
        )
        return response

    def update_messages(user_input, response, chain):
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.session_state.messages.append(AIMessage(content=response[chain.output_key]))

    def handle_assistant_response(user_input, creator_current_lesson):
        # Check if the user's input contains a command to switch sections
        if user_input.startswith("switch to "):
            section_title = user_input[len("switch to "):]
            st.session_state["creator_current_lesson"].set_section(section_title)
        elif user_input == "next section":
            st.session_state["creator_current_lesson"].update_current_section()  # Update creator_current_section before using it
            st.session_state["creator_current_section"] = st.session_state["creator_current_lesson"].active_section

        with st.chat_message("assistant"):
            prompt_template = get_prompt_template(st.session_state["creator_current_lesson"])
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
        if st.session_state.get("creator_current_lesson_file") != selected_lesson_file:
            st.session_state["creator_current_lesson_file"] = selected_lesson_file
            welcome_message = f"Once you are prepared, we shall begin creating a lesson plan based on {selected_lesson_file}. I will be your guide."
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
    
    def update_session_state(session_state, selected_lesson_file, active_section):
        if session_state["creator_current_lesson"] is None or session_state["creator_current_lesson"].filename != selected_lesson_file:
            session_state["creator_current_lesson"] = Lesson(selected_lesson_file)
            session_state["creator_current_lesson"].update_current_section()  # Update creator_current_section immediately
        if session_state["creator_current_section"] is None or (session_state["creator_current_lesson"].active_section is not None and session_state["creator_current_section"] != session_state["creator_current_lesson"].active_section):
            session_state["creator_current_section"] = session_state["creator_current_lesson"].active_section

    # Initialize LangSmith langsmith_client
    langsmith_client = Client()

    # Lesson selection sidebar
    selected_lesson_file = st.sidebar.selectbox("Select Template", os.listdir("templates"))

    # Create a new Lesson object
    update_session_state(st.session_state, selected_lesson_file, st.session_state["creator_current_section"])

    # Dropdown menu for section selection
    selected_section = st.sidebar.selectbox("Section Preview", st.session_state["creator_current_lesson"].get_section_names(), key='section_select')
    # Get the content of the selected section
    section_content = getattr(st.session_state["creator_current_lesson"], selected_section)
    # Display the content in the sidebar
    st.sidebar.markdown(section_content)

    initialize_state()

    display_messages()

    # Handle user input and assistant responses
    if user_input := handle_user_input():
        handle_assistant_response(user_input, st.session_state["creator_current_lesson"])
