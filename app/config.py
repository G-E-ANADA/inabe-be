import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    origins = os.getenv("CORS_ORIGINS", "").split(",")
    if not origins:
        origins = ["http://localhost:1234"]

settings = Settings()
