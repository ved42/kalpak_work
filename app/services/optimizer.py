from app.config import genai
from app.prompts import SQL_OPTIMIZER_PROMPT

def optimize_sql(sql_query: str) -> str:
    prompt = SQL_OPTIMIZER_PROMPT.format(sql_query=sql_query)
    response = genai.generate(prompt=prompt, model="gemini-1.5-flash")
    return response.result.strip() if response.result else sql_query
