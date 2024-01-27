from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


class CRUDExercise(CRUDBase[Exercise, ExerciseCreate, ExerciseUpdate]):
    def create(self, db: Session, *, obj_in: ExerciseCreate) -> Exercise:
        db_obj = Exercise(**obj_in.model_dump(exclude_unset=True))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Exercise, obj_in: Union[ExerciseUpdate, Dict[str, Any]]) -> Exercise:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:   
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def remove_field(self, db: Session, *, db_obj: Exercise, field: str) -> Optional[Exercise]:
        if db_obj:
            if hasattr(db_obj, field):
                setattr(db_obj, field, "")
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            return db_obj
        return None
    
    def get_by_user_diet_plan_info(self, db: Session, *, user_diet_plan_info_id) -> Optional[Exercise]:
        return db.query(Exercise).filter(Exercise.user_diet_plan_info_id == user_diet_plan_info_id).first()



crud_exercise = CRUDExercise(Exercise)