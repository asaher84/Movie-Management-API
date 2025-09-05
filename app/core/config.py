
import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class Settings(BaseModel):
    app_name: str = "Movie Management API"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./movies.db")
    page_limit_default: int = int(os.getenv("PAGE_LIMIT_DEFAULT", "10"))
    page_limit_max: int = int(os.getenv("PAGE_LIMIT_MAX", "50"))

settings = Settings()
