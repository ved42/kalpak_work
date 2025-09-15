from fastapi import FastAPI, Form, Request, UploadFile,File
from app.models.data_models import QueryRequest, QueryResponse
from app.services.chatbot_service import process_user_query
from fastapi.responses import PlainTextResponse
app = FastAPI(title="Conversational NL2SQL API")

from fastapi.responses import PlainTextResponse

@app.post("/query", response_class=PlainTextResponse)
async def query_endpoint(
    query: str = Form(...),
    file: UploadFile = File(None),
    request: Request = None
):
    session_id = request.cookies.get("session_id", "default_session")
    uploaded_bytes = await file.read() if file else None

    result_text = process_user_query(session_id, query, uploaded_bytes)

    return result_text

