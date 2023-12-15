# 칼로리 계산/ 운동 추천/ 잔소리
def get_diet_exercise_advice(completion_executor, bmr, user_input):
    # user_input : 사용자의 기초대사량과 사용자가 먹은 식단. 
    # 예시) 내 기초대사량은 2000kcal 이고 오늘 아침은 계란 2개, 점심은 삼겹살, 저녁은 짜장면
    preset_text = [{"role": "system", "content": "비관적이지만 유쾌하게 팩트를 알려줍니다.\r\n- 이모티콘을 사용해서 생동감을 더합니다.\r\n- 먹은 음식의 칼로리를 계산해서 주어진 기초대사량에 비교하고 얼마나 칼로리를 더 소비했는지 알려줍니다. 그리고 어떤 운동을 얼마나 해야지 살이 안찔지 알려줍니다.\r\n- 목표는 사용자가 운동의 필요성을 심각하게 느끼고 할 수 밖에 없게 동기부여를 해주는 것입니다.\r\n- 대답은 json 형식입니다.\r\n- 아침, 점심, 저녁, 총칼로리, 초과칼로리, 운동필요시간, 잔소리 의 key를 가집니다. value에 해당하는 값을 넣어서 json 형식으로 응답해주세요.\r\n- 대답은 반드시 아래와 같이 json 형식으로\r\n- 잔소리는 200자를 넘기지 말아주세요.\r\n- 질문 답변 예시:\r\n\"질문\" : \"저는 키 160 에 몸무게 50 나가는 20대 여자입니다. 오늘 아침은 고구마 2개, 점심은 떡볶이, 저녁은 마라탕 먹었어요. \",\r\n\{\r\n\"아침\" : \"300 kcal\", \r\n\"점심\" : \"900-1000 kcal\",\r\n\"저녁\":  \"1000-1200 kcal\",\r\n\"초과칼로리\" : \"300 kcal\" , \r\n\"운동필요시간\" : \"스쿼트 100 개 이상 혹은 걷기 3시간\" \r\n\"잔소리\" : \"그렇게 드시고 살이 안 찌길 바라세요? 어림도 없죠. 당장 운동 시작하세요!\"\r\n}\r\n\r\n\n"},
            { "role" : "user", "content" : "내 기초대사량은 1800 이고 오늘 아침은 계란 2개, 점심은 삼겹살, 저녁은 짜장면"},
            { "role" : "assistant", "content" : "{\n\"아침\" : \"200 kcal\", \n\"점심\" : \"800-1000 kcal\",\n\"저녁\":  \"700-800 kcal\",\n\"초과칼로리\" : \"100 kcal\" , \n\"운동필요시간\" : \"런닝머신 1시간 또는 자전거 타기 30분 4세트\" \n\"잔소리\" : \"맛있게 드셨으면 그만큼 운동하셔야죠! 얼른 하세요!\"\n}"}, 
            {"role": "user", "content": "내 기초대사량은"+bmr+"이고 "+user_input}]

    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 100,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True
    }

    response_text = completion_executor.execute(request_data)

    # 형식 확인
    if '아침' in response_text and '점심' in response_text and '저녁' in response_text and '초과칼로리' in response_text and '운동필요시간' in response_text and '잔소리' in response_text:
        print(response_text)
        return response_text
    else:
        return {"error": "잘못된 형식의 응답입니다."}
