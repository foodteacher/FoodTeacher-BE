from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_info import UserDietPlanInfo
from app.schemas.user_diet_plan_info import UserDietPlanInfoCreate, UserDietPlanInfoUpdate


class CRUDUserDietPlanInfo(CRUDBase[UserDietPlanInfo, UserDietPlanInfoCreate, UserDietPlanInfoUpdate]):
    def create(self, db: Session, *, obj_in: UserDietPlanInfoCreate) -> UserDietPlanInfo:
        db_obj = UserDietPlanInfo(**obj_in.model_dump(exclude_unset=True))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: UserDietPlanInfo, obj_in: Union[UserDietPlanInfoUpdate, Dict[str, Any]]) -> UserDietPlanInfo:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:   
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def remove_field(self, db: Session, *, db_obj: UserDietPlanInfo, field: str) -> Optional[UserDietPlanInfo]:
        if db_obj:
            if hasattr(db_obj, field):
                setattr(db_obj, field, "")
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            return db_obj
        return None
    
    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[UserDietPlanInfo]:
        return db.query(UserDietPlanInfo).filter(UserDietPlanInfo.user_id == user_id).first()


crud_user_diet_plan_info = CRUDUserDietPlanInfo(UserDietPlanInfo)