import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Create model instance
_model_cache = {}

def generate(prompt: str, model: str = "gemini-1.5-flash"):
    """Wrapper function so services can call genai.generate(...) easily"""
    if model not in _model_cache:
        _model_cache[model] = genai.GenerativeModel(model)
    response = _model_cache[model].generate_content(prompt)
    return response