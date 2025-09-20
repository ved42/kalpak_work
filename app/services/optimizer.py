from app.config import generate
from app.prompts import SQL_OPTIMIZER_PROMPT
import re

def optimize_sql(sql_query: str) -> str:
    """
    Optimize a SQL query using the LLM.
    Returns only a valid SQL statement.
    If no optimization possible, returns original query unchanged.
    """
    prompt = SQL_OPTIMIZER_PROMPT.format(sql_query=sql_query)
    response = generate(prompt)

    if not response:
        return sql_query

    # Remove markdown/code fences
    cleaned = re.sub(r"```sql|```", "", response, flags=re.IGNORECASE).strip()

    # Extract first SQL-like statement (safety)
    match = re.search(r"(SELECT .*?;)", cleaned, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    # If model added comments or explanations, drop them
    if cleaned.upper().startswith("SELECT"):
        return cleaned

    return sql_query  # fallback if no valid SQL found
