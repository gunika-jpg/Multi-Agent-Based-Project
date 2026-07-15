from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SERPAPI_KEY: str = ''
    FIRECRAWL_API_KEY: str = ''
    GOOGLE_API_KEY: str = ''
    CACHE_TTL: int = 900
    MAX_PRODUCTS_PER_SOURCE: int = 10
    LOG_LEVEL: str = 'INFO'
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

# Singleton instance
_settings = Settings()

def get_settings() -> Settings:
    return _settings
