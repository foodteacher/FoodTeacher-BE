from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    ENVIRONMENT: str

    # MySQL 설정 정보
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    # JWT 설정 정보
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14

    #kakao 설정 정보
    KAKAO_REST_API_KEY: str
    @property
    def redirect_uri(self):
        if self.ENVIRONMENT == "production":
            return "https://foodteacher.xyz/oauth"
        else:
            return "http://localhost:3000/oauth"

    # chatGPT
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_setting():
    return Settings()
