from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

def load_section_prompt(section_title, content):
	template = f"""
    You are an educator, and you are currently teaching the '{section_title}' section of the lesson. Your task is to guide the user through this section, encouraging them to progress when appropriate. Limit any responses to only one concept or step per prompt.

    Here is the content of this section:

    {content}

    """.format(content=content)

	prompt_template = ChatPromptTemplate(messages = [
		SystemMessage(content=template), 
		MessagesPlaceholder(variable_name="chat_history"), 
		HumanMessagePromptTemplate.from_template("{input}")
		])
	return prompt_template
