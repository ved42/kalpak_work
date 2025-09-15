from app.config import genai
from app.prompts import REPHRASER_PROMPT

def rephrase_query(query: str) -> str:
    prompt = REPHRASER_PROMPT.format(query=query)
    response = genai.generate(prompt=prompt, model="gemini-1.5-flash")
    return response.result or query
