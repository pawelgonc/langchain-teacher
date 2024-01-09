from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

def load_lesson_plan_prompt():
    template = f"""
    Your task is to create a lesson plan. If the user has not specified a topic, ask them for one. Otherwise, create a lesson plan for the topic or phenomenon of the user's choice.
    
    LESSON_PLAN_START
    Lesson plan must contain these sections in this order: Lesson Title, Background and Prerequisites, Learning Objectives, Content Delivery, Introduction, Main Points, Conclusion, and Next Steps.
    
    Additionally, the "Main Points" section must contain at least one "Point/Topic" section. Moreover, each "Point/Topic" section must contain the "Explanation", "Examples", and "Applications" sections.
    LESSON_PLAN_END
    """

    prompt_template = ChatPromptTemplate(messages = [
        SystemMessage(content=template), 
        MessagesPlaceholder(variable_name="chat_history"), 
        HumanMessagePromptTemplate.from_template("{input}")
        ])
    return prompt_template
