from langchain_groq import ChatGroq
from src.config.settings import settings

from groq import Groq

def get_groq_llm(model_name=None):
    return ChatGroq(
        api_key = settings.GROQ_API_KEY,
        model = model_name or settings.MODEL_NAME,
        temperature=settings.TEMPERATURE
    )

def get_supported_models():
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        models = client.models.list()
        # Filter for models that are likely LLMs (id usually starts with gemma, llama, mixtral)
        # or just return all IDs. Let's return all IDs for now to be safe, or maybe filter typical prefixes.
        return [m.id for m in models.data]
    except Exception as e:
        # Fallback list if API fails
        return ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma-7b-it"]