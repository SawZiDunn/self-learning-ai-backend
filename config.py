import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))
    
    @classmethod
    def validate(cls):
        """Validate that required config is present"""
        if not cls.GROQ_API_KEY and not cls.GEMINI_API_KEY:
            raise ValueError("At least one LLM API key (GROQ or GEMINI) is required")
        if not cls.SUPABASE_URL or not cls.SUPABASE_KEY:
            raise ValueError("Supabase credentials are required")
        return True
