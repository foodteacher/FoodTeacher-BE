from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # MySQL 설정 정보
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    # # CLOVA 설정 정보
    # CLOVA_HOST: str
    # CLOVA_API_KEY: str
    # CLOVA_API_KEY_PRIMARY_VAL: str
    # CLOVA_REQUEST_ID: str

    # JWT 설정 정보
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"

@lru_cache()
def get_setting():
    return Settings()
