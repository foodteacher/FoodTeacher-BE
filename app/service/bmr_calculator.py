from ..db.models.user import User
from .. import utils

# 기초대사량 계산
def calculate_bmr(user_data: utils.TempUserInput):
    # Mifflin-St Jeor 공식을 사용
    gender = user_data.gender; weight = user_data.weight; height = user_data.height; age = user_data.age
    if gender == '남성':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == '여성':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender")

    return bmr