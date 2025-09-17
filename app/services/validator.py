from app.config import genai
from app.prompts import SQL_VALIDATOR_PROMPT

def validate_sql(sql_query: str) -> bool:
    prompt = SQL_VALIDATOR_PROMPT.format(sql_query=sql_query)
    response = genai.generate(prompt=prompt, model="gemini-1.5-flash")
    return "yes" in (response.text or "").lower()
