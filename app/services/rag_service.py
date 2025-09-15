from app.prompts import RAG_PROMPT
from app.config import genai

def get_schema_info() -> str:
    context = "Provide schema details for query generation"
    prompt = RAG_PROMPT.format(context=context)
    response = genai.generate(prompt=prompt, model="gemini-1.5-flash")
    return response.result.strip() if response.result else "Table: employees (id, name, department, salary)"
