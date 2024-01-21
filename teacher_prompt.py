from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

def load_section_prompt(teacher_current_lesson):
    section_title = teacher_current_lesson.active_section
    content = getattr(teacher_current_lesson, teacher_current_lesson.active_section)

    print(f"Loading section '{section_title}' into teacher_prompt.")

    template = f"""
    - You are a research collaborator, and you are currently assisting with the '{section_title}' step of the scientific method.
    - Your task is to:
    {content}
    """

    if next_section_title and next_section_content:
        template += f"""

        Looking ahead, the next section will be '{next_section_title}'. Here is a preview of the content:

        {next_section_content}

        Please ensure that the user is ready to move on to this next section.
        """

    prompt_template = ChatPromptTemplate(messages = [
        SystemMessage(content=template), 
        MessagesPlaceholder(variable_name="chat_history"), 
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return prompt_template
