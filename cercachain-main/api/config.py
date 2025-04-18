from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    debug: bool = False
    host: str = "localhost"
    port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000"]
    log_level: str = "INFO"

settings = Settings()