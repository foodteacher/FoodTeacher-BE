from db.base import user_read

# 기초대사량 계산
def calculate_bmr(name, height, weight, age, gender):
    # Mifflin-St Jeor 공식을 사용
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender")

    return bmr