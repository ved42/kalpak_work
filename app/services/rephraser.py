from app.config import generate
from app.prompts import REPHRASER_PROMPT
import re

def rephrase_query(query: str) -> str:
    prompt = REPHRASER_PROMPT.format(query=query)
    response = generate(prompt)

    if not response:
        return query

    # Clean up response (remove markdown/code fences if model adds them)
    cleaned = re.sub(r"```|Rephrased Query:", "", response, flags=re.IGNORECASE).strip()

    return cleaned or query
