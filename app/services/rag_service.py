from app.prompts import RAG_PROMPT
from app.config import generate
import re

def get_schema_info() -> str:
    context = "Provide schema details for query generation"
    prompt = RAG_PROMPT.format(context=context)
    response = generate(prompt)

    if not response:
        # Default fallback schema
        return "Table_Name(Column1, Column2, Column3, Column4)"

    # Clean response: remove code fences or stray words
    cleaned = re.sub(r"```|Schema Info:", "", response, flags=re.IGNORECASE).strip()

    return cleaned or "Table_Name(Column1, Column2, Column3, Column4)"
