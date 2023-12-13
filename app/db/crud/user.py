from ..session import SessionLocal
from ..models.user import User

def create_user(db: Session, user_data: dict):
    # SQLAlchemy 세션 생성
    db = SessionLocal()

    try:
        # User 모델을 사용하여 새로운 사용자 데이터 생성
        new_user = User(**user_data)

        # 세션에 데이터 추가
        db.add(new_user)

        # 변경사항 커밋 (데이터베이스에 저장)
        db.commit()

        # 변경사항이 데이터베이스에 반영된 후에는 사용자 생성에 성공한 것입니다.
        return new_user
    except Exception as e:
        # 예외 처리 (예: 데이터베이스 오류 등)
        db.rollback()
        raise e
    finally:
        # 세션 종료
        db.close()

def update_user(db: Session, user_id: int, update_data: dict):
    # SQLAlchemy 세션 생성
    db = SessionLocal()

    try:
        # 사용자 ID를 사용하여 사용자 데이터 쿼리
        db_user = db.query(User).filter(User.userId == user_id).first()

        if db_user:
            # 필요한 변경사항을 적용
            for key, value in update_data.items():
                setattr(db_user, key, value)

            # 변경사항 커밋 (데이터베이스에 저장)
            db.commit()

            # 변경사항이 데이터베이스에 반영된 후에는 업데이트에 성공한 것입니다.
            return db_user
        else:
            # 사용자를 찾을 수 없는 경우 예외 처리
            raise Exception("사용자를 찾을 수 없습니다.")
    except Exception as e:
        # 예외 처리 (예: 데이터베이스 오류 등)
        db.rollback()
        raise e
    finally:
        # 세션 종료
        db.close()
