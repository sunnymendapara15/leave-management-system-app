from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "super-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./leave_app.db"

    class Config:
        env_file = ".env"


settings = Settings()
