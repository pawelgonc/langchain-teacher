#lc_main.py

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
from get_prompt import load_prompt, load_prompt_with_questions
import os

st.set_page_config(page_title="LangChain: Custom Lesson", page_icon="🦜")
st.title("🦜 LangChain: Custom Lesson")
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
        self.content = self.load_content()

    def load_content(self):
        with open(f"lc_guides/{self.filename}", "r") as file:
            return file.read()

    def display(self):
        st.markdown(f"**{self.filename}**")
        st.write(self.content)

def handle_user_input():
    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        return prompt
    return None

def handle_assistant_response(prompt, lesson):
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-3.5-turbo-16k")

        if lesson_type == "Instructions based lesson":
            prompt_template = load_prompt(content=lesson.content)
        else:
            prompt_template = load_prompt_with_questions(content=lesson.content)

        chain = LLMChain(prompt=prompt_template, llm=model)

        response = chain(
            {"input": prompt, "chat_history": st.session_state.messages[-20:]},
            include_run_info=True,
            tags=[lesson.filename, lesson_type]
        )
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.session_state.messages.append(AIMessage(content=response[chain.output_key]))
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

# Clear chat session if dropdown option or radio button changes
def initialize_state():
    if st.session_state.get("current_lesson") != lesson_file or st.session_state.get("current_lesson_type") != lesson_type:
        st.session_state["current_lesson"] = lesson_file
        st.session_state["current_lesson_type"] = lesson_type
        st.session_state["messages"] = [AIMessage(content="Welcome! This short course will help you get started with LangChain. Let me know when you're all set to jump in!")]

# Message handling and interaction
def send_feedback(run_id, score):
    client.create_feedback(run_id, "user_score", score=score)

def display_messages():
    for msg in st.session_state["messages"]:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("assistant").write(msg.content)

# Initialize LangSmith client
client = Client()

# Get all lesson files in the lc_guides directory
lesson_files = os.listdir("lc_guides")

# Lesson selection sidebar
lesson_file = st.sidebar.selectbox("Select Lesson", os.listdir("lc_guides"))

# Create a new Lesson object and display the lesson
lesson = Lesson(lesson_file)
lesson.display()

# Radio buttons for lesson type selection
lesson_type = st.sidebar.radio("Select Lesson Type", ["Instructions based lesson", "Interactive lesson with questions"])

initialize_state()

display_messages()

# Handle user input and assistant responses
if prompt := handle_user_input():
    handle_assistant_response(prompt, lesson)
