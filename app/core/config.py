import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    AZURE_SPEECH_KEY: str
    AZURE_SPEECH_REGION: str = "eastus"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate required environment variables
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        if not self.AZURE_SPEECH_KEY:
            raise ValueError("AZURE_SPEECH_KEY environment variable is required")

settings = Settings()