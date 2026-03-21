from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./egitim.db"
    cors_origins: list[str] = ["http://localhost:5173"]
    log_level: str = "INFO"
    content_dir: str = "content"

    class Config:
        env_file = ".env"


settings = Settings()
