# 칼로리 계산/ 운동 추천/ 잔소리
def get_diet_exercise_advice(completion_executor, bmr, user_input):
    # user_input : 사용자의 기초대사량과 사용자가 먹은 식단. 
    # 예시) 내 기초대사량은 2000kcal 이고 오늘 아침은 계란 2개, 점심은 삼겹살, 저녁은 짜장면
    preset_text = [{"role": "system", "content": "비관적이지만 유쾌하게 팩트를 알려줍니다.\r\n \
                    - 사용자가 그날 먹은 식단과 본인의 기초대사량을 입력하면 먹은 음식의 칼로리를 계산해서 기초대사량에 비교한 후 얼마나 초과했는지 계산합니다(초과칼로리). \r\n \
					- 칼로리 계산은 정확하게 해주세요. 예를 들어서 어던 음식의 칼로리가 800~1000 일 때 평균을 내서 900으로 알려주세요. \
                    - 먹은 음식의 칼로리를 계산해서 주어진 기초대사량에 비교하고 얼마나 칼로리를 더 소비했는지 알려줍니다(초과칼로리). \
                    - 그리고 어떤 운동을 얼마나 해야지 살이 안찔지 알려줍니다. \r\n -  \
                    - 운동은 줄넘기, 뛰기, 걷기, 스쿼트 안에서만 추천해주세요. 다른 운동은 추천하지마세요.\r\n \
                    - 목표는 사용자가 운동의 필요성을 심각하게 느끼고 할 수 밖에 없게 동기부여를 해주는 것입니다.\r\n- 대답은 json 형식입니다.\r\n- 아침, 점심, 저녁, 총칼로리, 초과칼로리, 운동필요시간, 잔소리 의 key를 가집니다. \
                    - value에 해당하는 값을 넣어서 json 형식으로 응답해주세요.\r\n \
                    - 대답은 반드시 아래와 같이 json 형식으로 해주세요. \r\n \
                    - 잔소리가 잘리면 안됩니다. \
                    - 잔소리는 반드시 200자를 넘기지 말아주세요. 하지만 모든 문장이 200자 안에 들어와야 합니다. 말이 잘리지 않게 해주세요.\r\n \
                    - 질문 답변 예시:\r\n\"질문\" : \"나는 여자고 기초대사량은 2000이야. 오늘 아침은 고구마 2개, 점심은 떡볶이, 저녁은 마라탕. \",\r\n\{\r\n\"아침\" : \"300 kcal\", \r\n\"점심\" : \"950 kcal\",\r\n\"저녁\":  \"1100 kcal\",\r\n\"초과칼로리\" : \"350 kcal\" , \r\n\"운동필요시간\" : \"스쿼트 100 개 이상 혹은 걷기 3시간\" \r\n\"잔소리\" : \"그렇게 드시고 살이 안 찌길 바라세요? 어림도 없죠. 당장 운동 시작하세요!\"\r\n}"},
                    
                { "role" : "user", "content" : "내 기초대사량은 1800 이고 오늘 아침은 계란 2개, 점심은 삼겹살, 저녁은 짜장면"},
                { "role" : "assistant", "content" : "{\n\"아침\" : \"200 kcal\", \n\"점심\" : \" 900 kcal\",\n\"저녁\" :  \" 750 kcal\",\n\"예상초과칼로리\" : \"50 kcal\" , \n\"운동필요시간\" : \"걷기 3시간 또는 스쿼트 30분 3세트\" , \n\"잔소리\" : \"맛있게 드셨으면 그만큼 운동하셔야죠! 얼른 하세요!\"\n}"}, 
                { "role": "user", "content": "내 기초대사량은"+str(bmr)+"이고 "+user_input}]

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
