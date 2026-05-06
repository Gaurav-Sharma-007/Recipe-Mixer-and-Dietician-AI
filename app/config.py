import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Recipe Remix API")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user1:123456@localhost:5433/recipe_db",
    )
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


settings = Settings()
