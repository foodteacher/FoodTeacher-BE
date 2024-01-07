from fastapi import APIRouter, Depends

from app.core.config import get_setting
from app.models.user import User
from app.schemas.gpt import UserQuery
from app.api.depends import get_current_user
from app.service.foodteacher import calculate_calory, calculate_bmr
import json

router = APIRouter()
settings = get_setting()

@router.post("/diet-exercise-advice")
def get_answer_from_gpt(query: UserQuery, current_user: User = Depends(get_current_user)):
    bmr = calculate_bmr(current_user)
    res = calculate_calory(query.query, bmr)
    result = json.loads(res)
    return result