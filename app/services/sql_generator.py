from app.config import generate
from app.prompts import SQL_GENERATOR_PROMPT
import re

def generate_sql(natural_query: str, schema_info: str, conversation_history: str = "") -> str:
    prompt = SQL_GENERATOR_PROMPT.format(
        schema_info=schema_info,
        natural_query=natural_query,
        conversation_history=conversation_history
    )
    response = generate(prompt)

    if not response:
        return ""

    # Clean up model output → remove markdown & extra text
    cleaned = re.sub(r"```sql|```", "", response, flags=re.IGNORECASE).strip()

    # Extract only the SQL query if explanation accidentally included
    match = re.search(r"(SELECT .*?;)", cleaned, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return cleaned
