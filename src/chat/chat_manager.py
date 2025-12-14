from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from src.llm.groq_client import get_groq_llm
from src.prompts.templates import chat_prompt_template
from src.common.logger import get_logger

class ChatManager:
    def __init__(self, model_name=None):
        self.llm = get_groq_llm(model_name)
        self.logger = get_logger(self.__class__.__name__)
        # We will manage memory manually or pass it in, but for a simple 
        # stateless manager called from Streamlit where state is external,
        # we can just use the prompt with history passed in.
        
    def get_response(self, user_input, history_text):
        try:
            # Simple invocation using the prompt template directly
            # transforming the prompt into a string
            prompt = chat_prompt_template.format(history=history_text, input=user_input)
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            self.logger.error(f"Error generating chat response: {e}")
            return "I'm having a little trouble thinking right now. Can you try again?"
