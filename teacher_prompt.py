from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

def load_section_prompt(current_lesson):
    section_title = current_lesson.active_section
    content = getattr(current_lesson, current_lesson.active_section)
    next_section_title, next_section_content = current_lesson.get_next_section_content()

    template = f"""
    You are an educator, and you are currently teaching the '{section_title}' section of the lesson. Your task is to guide the user through this section, encouraging them to progress when appropriate. Limit any responses to only one concept or step per prompt.

    Here is the content of this section:

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
