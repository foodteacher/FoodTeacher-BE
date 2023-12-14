from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import get_setting

settings = get_setting()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    settings.MYSQL_USER,
    settings.MYSQL_PASSWORD,
    settings.MYSQL_HOST,
    settings.MYSQL_PORT,
    settings.MYSQL_DATABASE,
)

db_engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

# # 의존성 인젝터를 사용하여 세션 생성
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()