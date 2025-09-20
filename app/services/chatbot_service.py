from app.services.rephraser import rephrase_query
from app.services.sql_generator import generate_sql
from app.services.validator import validate_sql
from app.services.optimizer import optimize_sql
from app.services.rag_service import get_schema_info
from app.prompts import CHATBOT_CONTEXT_PROMPT
from app.config import generate
from app.services.memory_service import save_message, get_last_messages, init_db

# Initialize DB when service starts
init_db()

def process_user_query(session_id: str, query: str) -> dict:
    # Save query in memory
    save_message(session_id, query)

    # Get last 10 messages for context
    history = get_last_messages(session_id, 10)
    conversation_history = "\n".join([f"User: {q}" for q in history])

    # Context-aware filtering
    context_prompt = CHATBOT_CONTEXT_PROMPT.format(
        conversation_history=conversation_history,
        user_input=query
    )
    context_response = (generate(context_prompt) or "").strip()

    # Reject irrelevant queries
    if "assist only with data queries" in context_response.lower():
        return {"sql_query": None, "explanation": context_response}

    # Handle explicit "explain" queries
    if "explain" in query.lower():
        explanation = f"This SQL query is designed to retrieve relevant columns or rows efficiently.\n\nContext:\n{query}"
        return {"sql_query": None, "explanation": explanation}

    # Run NL2SQL pipeline
    rephrased = rephrase_query(query)
    schema_info = get_schema_info()
    sql_query = generate_sql(rephrased, schema_info, conversation_history)

    # Validate SQL
    if not validate_sql(sql_query):
        return {"sql_query": None, "explanation": "Generated SQL is invalid."}

    # Optimize SQL
    optimized_sql = optimize_sql(sql_query)

    return {"sql_query": optimized_sql, "explanation": None}
