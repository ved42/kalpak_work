# Conversational NL2SQL Platform with Agentic AI

## Setup Instructions
1. Install dependencies:
   `pip install -r requirements.txt`
2. Set environment variables in `.env`
3. Run the app:
   `python app/main.py`

## API
POST /query  
Payload:  
```json
{
  "query": "Show me employees in Sales department"
}
