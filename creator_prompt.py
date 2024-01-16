from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

def load_section_prompt(creator_current_lesson):
    section_title = creator_current_lesson.active_section
    content = getattr(creator_current_lesson, creator_current_lesson.active_section)

    print(f"Loading section '{section_title}' into creator_prompt.") #debugg

    template = f"""
    You are helping the user to create a lesson plan, and you are currently creating the '{section_title}' section of the lesson. Your task is to prompt the user for details regarding content of this section.
    You should expect the user to provide details in a various of methods: they might have an already specified area of interest, they might be in an exploratory phase of their area of interest, or their are of interest might not be specified yet. Here is the instruction specific to this section:

    {content}

    """

    prompt_template = ChatPromptTemplate(messages = [
        SystemMessage(content=template), 
        MessagesPlaceholder(variable_name="chat_history"), 
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return prompt_template
