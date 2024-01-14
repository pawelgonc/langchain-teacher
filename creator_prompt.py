from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

def load_section_prompt(creator_current_lesson):
    section_title = creator_current_lesson.active_section
    content = getattr(creator_current_lesson, creator_current_lesson.active_section)
    next_section_title, next_section_content = creator_current_lesson.get_next_section_content()

    template = f"""
    You are a lesson plan creator, and you are currently creating the '{section_title}' section of the lesson. Your task is to prompt the user for details regarding content of this section.
    Here is the instruction specific to this section:

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
