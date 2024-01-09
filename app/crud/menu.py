from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.menu import Menu
from app.schemas.menu import MenuCreate, MenuUpdate


class CRUDMenu(CRUDBase[Menu, MenuCreate, MenuUpdate]):
    def create(self, db: Session, *, obj_in: MenuCreate) -> Menu:
        db_obj = Menu(**obj_in.model_dump(exclude_unset=True))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Menu, obj_in: Union[MenuUpdate, Dict[str, Any]]) -> Menu:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:   
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def remove_field(self, db: Session, *, db_obj: Menu, field: str) -> Optional[Menu]:
        if db_obj:
            if hasattr(db_obj, field):
                setattr(db_obj, field, "")
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            return db_obj
        return None


crud_menu = CRUDMenu(Menu)