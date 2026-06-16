# app/core/config.py
class Settings:
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "curriculum_db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite:///./curriculum.db"

settings = Settings()