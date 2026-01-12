"""Configuration Browser Automation"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2:7b"
    
    # Browser
    BROWSER_HEADLESS: bool = True
    BROWSER_TIMEOUT: int = 30000  # 30 secondes
    
    # Paths
    SCREENSHOTS_DIR: str = "./screenshots"
    DATA_DIR: str = "./data"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
