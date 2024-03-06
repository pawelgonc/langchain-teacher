from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage

def load_section_prompt(teacher_current_lesson):
    section_title = teacher_current_lesson.active_section
    content = getattr(teacher_current_lesson, teacher_current_lesson.active_section)

    print(f"Loading section '{section_title}' into teacher_prompt.") #debugg

    template = f"""
    You are an educator, and you are currently teaching the '{section_title}' section of the lesson. Your task is to guide the user through this section in detail, considering their current understanding. Limit any responses to only one concept or step per prompt.

    Here is the content of this section:

    {content}
    """

    prompt_template = ChatPromptTemplate(messages = [
        SystemMessage(content=template), 
        MessagesPlaceholder(variable_name="chat_history"), 
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return prompt_template