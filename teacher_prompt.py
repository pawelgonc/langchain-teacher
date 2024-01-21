from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

def load_section_prompt(teacher_current_lesson):
    section_title = teacher_current_lesson.active_section
    content = getattr(teacher_current_lesson, teacher_current_lesson.active_section)

    print(f"Loading section '{section_title}' into teacher_prompt.") #debugg

    template = f"""
    - You are a research collaborator, and you are currently assisting with the '{section_title}' step of the scientific method.
    - Your task is to:
    {content}
    """

    prompt_template = ChatPromptTemplate(messages = [
        SystemMessage(content=template), 
        MessagesPlaceholder(variable_name="chat_history"), 
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return prompt_template
