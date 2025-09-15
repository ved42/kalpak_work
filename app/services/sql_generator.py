from app.config import genai
from app.prompts import SQL_GENERATOR_PROMPT

def generate_sql(natural_query: str, schema_info: str) -> str:
    prompt = SQL_GENERATOR_PROMPT.format(
        schema_info=schema_info,
        natural_query=natural_query
    )
    response = genai.generate(prompt=prompt, model="gemini-1.5-flash")
    return response.result.strip() if response.result else ""
