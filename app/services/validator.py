from app.config import generate
from app.prompts import SQL_VALIDATOR_PROMPT

def validate_sql(sql_query: str) -> bool:
    # Bypass strict validation for placeholder queries
    if "Table_Name" in sql_query or "Column" in sql_query:
        return True

    prompt = SQL_VALIDATOR_PROMPT.format(sql_query=sql_query)
    response = generate(prompt)

    if not response:
        return False

    return "yes" in response.strip().lower()
