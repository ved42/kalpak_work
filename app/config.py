import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# DB_URL = os.getenv("DATABASE_URL")  # Placeholder for DB connection string

import google.generativeai as genai
genai.configure(api_key=GOOGLE_API_KEY)
