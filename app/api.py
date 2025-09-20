from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.models.data_models import QueryRequest, QueryResponse
from app.services.chatbot_service import process_user_query

app = FastAPI(title="Conversational NL2SQL API")

# ✅ Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, later restrict to ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: Request, payload: QueryRequest):
    session_id = request.cookies.get("session_id", "default_session")
    result = process_user_query(session_id, payload.query)

    return QueryResponse(
        sql_query=result["sql_query"],
        explanation=result["explanation"]
    )
