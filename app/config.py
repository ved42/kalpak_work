import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Create a reusable model instance
_model = genai.GenerativeModel("gemini-1.5-flash")

def generate(prompt: str) -> str:
    """Wrapper for generating responses using Gemini."""
    response = _model.generate_content(prompt)
    return response.text.strip() if response and response.text else ""
