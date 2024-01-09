
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
from creator_prompt import load_lesson_plan_prompt

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
        def __init__(self, filename):
            self.filename = filename
            st.session_state.lesson_plan = ""  # Initialize an empty lesson plan as a single string in session state

        def update_lesson_plan(self, content):
            # Extract the lesson plan content from the AI's response
            lesson_plan_content = extract_lesson_plan_content(content)

            # Append the lesson plan content to the lesson plan
            st.session_state.lesson_plan += "\n" + lesson_plan_content
            #print(f"Updated Lesson Plan: {st.session_state.lesson_plan}")  # Debugging print statement

        def display(self):
            # Display the current state of the lesson plan
            st.code(f"Lesson Plan\n\n{st.session_state.lesson_plan}")
            #print(" debugging in display() Lesson Plan Displayed")  # Debugging print statement

    def extract_lesson_plan_content(content):
        # Define the start and end markers
        start_marker = "LESSON_PLAN_START"
        end_marker = "LESSON_PLAN_END"

        # Find the start and end of the lesson plan content
        start = content.find(start_marker) + len(start_marker)
        end = content.find(end_marker)

        # Extract the lesson plan content
        lesson_plan_content = content[start:end].strip()

        return lesson_plan_content

    def handle_user_input():
        if user_input := st.chat_input():
            st.chat_message("user").write(user_input)
            #print(f"debugging in handle_user_input() User Input: {user_input}")  # Debugging print statement
            return user_input
        return None

    def get_prompt_template(current_template):
        # Use the general prompt template for the entire lesson plan
        prompt_template = load_lesson_plan_prompt()
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
            tags=[current_template.filename, selected_lesson_type]
        )
        #print(f"debugging in get_response() Assistant Response: {response}")  # Debugging print statement
        return response

    def update_messages(user_input, response, chain):
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.session_state.messages.append(AIMessage(content=response[chain.output_key]))

    def handle_assistant_response(user_input, current_template):
        # No need to check for "switch to" command or update current_section

        with st.chat_message("assistant"):
            prompt_template = get_prompt_template(current_template)
            chain = get_llm_chain(prompt_template)
            response = get_response(chain, user_input)

            # Update the lesson plan with the assistant's response
            current_template.update_lesson_plan(response[chain.output_key])

            update_messages(user_input, response, chain)
            run_id = response["__run"].run_id

        # Update the lesson plan display after the user inputs new content
        current_template.display()


    def display_feedback_buttons(run_id):
        col_blank, col_text, col1, col2 = st.columns([10, 2, 1, 1])
        with col_text:
            st.text("Feedback:")

        with col1:
            st.button("👍", on_click=send_feedback, args=(run_id, 1))

        with col2:
            st.button("👎", on_click=send_feedback, args=(run_id, 0))

    def initialize_state():
        if st.session_state.get("current_template") != selected_template_file or st.session_state.get("current_lesson_type") != selected_lesson_type:
            st.session_state["current_template"] = selected_template_file
            st.session_state["current_lesson_type"] = selected_lesson_type
            welcome_message = f"Once you are prepared, we shall begin creating a lesson plan. I will assist you."
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

    # Get all current_template files in the lessons directory
    template_files = os.listdir("templates")

    # Lesson selection sidebar
    selected_template_file = st.sidebar.selectbox("Select Lesson", os.listdir("templates"))

    # Radio buttons for current_template type selection
    selected_lesson_type = st.sidebar.radio("Select Lesson Type", ["Instructions based lesson", "Interactive lesson with questions"])

    # Create a new Lesson object
    current_template = Lesson(selected_template_file)
    # Display the title, background and prerequisites, and learning objectives
    current_template.display()

    initialize_state()

    display_messages()

    # Handle user input and assistant responses
    if user_input := handle_user_input():
        handle_assistant_response(user_input, current_template)
