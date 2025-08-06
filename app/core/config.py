from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = True
    GEMINI_API_KEY : str = "your-gemini-api-key"
    LANGCHAIN_API_KEY: str = "your-langchain-api-key"
    SMTP_USERNAME :str = "your_email@gmail.com"
    SMTP_PASSWORD: str = "your_app_password"
    SMTP_HOST : str= "smtp.gmail.com"
    SMTP_PORT: int = 587

    class Config:
        env_file = ".env"

settings = Settings()