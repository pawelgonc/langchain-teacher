from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

#Here are the tasks you must complete:
#1. Identify the topic, concept, or phenomenon that the user is interested in.
#2. Identify the user's knowledge gaps regarding their specified area of interest.
#3. Create a lesson plan that fills these gaps and does not include concepts the user is already familiar with.

#Structure of the lesson plan:
#Begin with the headline LESSON_PLAN_START.
#Include the following sections in order: Lesson Title, Background and Prerequisites, Learning Objectives, Content Delivery (Outline the main content points and the sequence in which they should be delivered. This could be in the form of a detailed script, a list of topics, or a combination of both), Introduction, Main Points (The main topics or points covered in the lesson. This section should contain at least one "Point/Topic" section), Point/Topic (Each point or topic should have an "Explanation", "Examples", and "Applications" sections), Conclusion (A summary of the main points of the lesson and relations between them), and Next Steps (Description of what should be done next to expand or specify the knowledge gained from this lesson. This could be in the form of a homework, further reading, or recent recent scientific discoveries that relate to the lesson)
#End the lesson plan with the footnote LESSON_PLAN_END.

#The created lesson plan will be an output to the AI, therefore it must be written as a command or prompt.
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
