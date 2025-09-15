from app.services.rephraser import rephrase_query
from app.services.sql_generator import generate_sql
from app.services.validator import validate_sql
from app.services.optimizer import optimize_sql
from app.services.rag_service import get_schema_info
from app.prompts import CHATBOT_CONTEXT_PROMPT
from app.config import genai

import pandas as pd
from io import BytesIO
from tabulate import tabulate

session_context = {}


def process_user_query(session_id: str, query: str, uploaded_file: bytes = None) -> str:
    if session_id not in session_context:
        session_context[session_id] = []

    session_context[session_id].append(query)

    context_prompt = CHATBOT_CONTEXT_PROMPT.format(user_input=query)
    context_response = genai.generate(prompt=context_prompt, model="gemini-1.5-flash").result.strip()
    if "assist only with data queries" in context_response:
        return "I'm designed to assist only with data queries related to enterprise databases."

    if "explain" in query.lower():
        return "This SQL query retrieves specific columns based on user input."

    rephrased = rephrase_query(query)

    if uploaded_file:
        df = pd.read_csv(BytesIO(uploaded_file))
        schema_info = "Table: uploaded_data (" + ", ".join(df.columns) + ")"
        sql_query = generate_sql(rephrased, schema_info)

        if not validate_sql(sql_query):
            return "Error: Generated SQL is invalid."

        optimized_sql = optimize_sql(sql_query)

        try:
            import pandasql
            extracted_data = pandasql.sqldf(optimized_sql, {"uploaded_data": df})
            table_text = tabulate(extracted_data, headers='keys', tablefmt='grid')
        except Exception as e:
            table_text = f"Error executing query: {str(e)}"

        response_text = f"SQL Query:\n{optimized_sql}\n\nExtracted Data:\n{table_text}"
        return response_text

    else:
        schema_info = get_schema_info()
        sql_query = generate_sql(rephrased, schema_info)

        if not validate_sql(sql_query):
            return "Error: Generated SQL is invalid."

        optimized_sql = optimize_sql(sql_query)

        return optimized_sql
