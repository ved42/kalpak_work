from fastapi import FastAPI
from app.models.data_models import QueryRequest, QueryResponse
from app.services.chatbot_service import process_user_query

app = FastAPI(title="Conversational NL2SQL API")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(payload: QueryRequest):
    session_id = "default_session"  # or generate unique IDs later
    result = process_user_query(session_id, payload.query)

    return QueryResponse(
        sql_query=result["sql_query"],
        explanation=result["explanation"])