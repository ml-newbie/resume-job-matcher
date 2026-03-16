from crewai import LLM
import os
from dotenv import load_dotenv
from get_keys import get_secret

load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
api_key = get_secret("OPENAI_API_KEY")

def get_llm(model_name="gpt-3.5-turbo"):
    return LLM(
    model=model_name,
    temperature=0.3,
    api_key=api_key
    )

# api_key = os.getenv("ANTHROPIC_API_KEY")   

# def get_llm(model_name="claude-3-haiku-20240307"):
#     return LLM(
#         model=f"anthropic/{model_name}",
#         temperature=0.3,
#         api_key=api_key
#     )