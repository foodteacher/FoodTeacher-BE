from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import get_setting
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

settings = get_setting()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    settings.MYSQL_USER,
    settings.MYSQL_PASSWORD,
    settings.MYSQL_HOST,
    settings.MYSQL_PORT,
    settings.MYSQL_DATABASE,
)

db_engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

def conn_test(engine):
    # 연결 테스트를 위한 쿼리 실행
    ql = text("SELECT 1")
    try:
        # Connection 객체 생성
        with engine.connect() as connection:
            # 간단한 쿼리 실행
            result = connection.execute(ql)
            # 결과 출력 (일반적으로 1)
            for row in result:
                print("Connection Test Result:", row[0])
            print("Database connection successful.")
    except OperationalError as e:
        print("Error occurred during Database connection:", e)



# 의존성 인젝터를 사용하여 세션 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()