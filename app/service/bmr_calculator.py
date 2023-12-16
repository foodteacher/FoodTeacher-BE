from ..db.models.user import User

# 기초대사량 계산
def calculate_bmr(user: User):
    # Mifflin-St Jeor 공식을 사용
    gender = user.gender; weight = user.weight; height = user.height; age = user.age
    if gender == '남성':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == '여성':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender")

    return bmr