import json

from .models import Category, Mission

from django.views import View
from django.http  import HttpResponse,JsonResponse

class MissionView(View):
    def get(self, request):
        category = request.GET.get('category', None)
        print(request.GET)
        try:
            if category:
                int(category)
                missions  =  Mission.objects.select_related('category').filter(category_id = category)
                result = [{
                    "name" : mission.name,
                    "description": mission.description,
                    "category":mission.category.name
                } for mission in missions]

                return JsonResponse({"message":result}, status = 200)

            mission = Mission.objects.values('name','category')
            return JsonResponse([
                {
                    'message':[
                        'HTTP 메소드 연습장에 오신 여러분 환영 합니다.',
                        '아래의 목록은 여러분이 진행해야 할 메소드의 미션 목록 입니다.',
                        '해당 미션을 호출하시려면 특별한 호출을 해야만 합니다.',
                        '바로, 쿼리스트링 혹은 쿼리 파라미터 라고 부르는 요소 입니다.',
                        '😀 POSTMAN 항목에는 메소드 호출 부분 하단에 첫번째 탭인 Params 탭에 입력할 수 있습니다.',
                        '🐶 KEY에 category, VALUE에 1을 입력하시면 됩니다.',
                        '👩🏻‍💻 입력하시고나면 주소창에 보이는 주소값은 서버주소명/api?category=1 과 같이 표시될 것입니다.'
                        '🐭 httpie로 호출할 경우에는 본 경로 입력한 다음 category==1과 같이 값을 전달하면 주소처리되어 호출합니다.'
                    ]
                },
                {'list':list(mission)}], safe = False, status = 200)

        except ValueError:
            return JsonResponse({'message' : '🧐 쿼리 파리미터는 리스트에 있는 숫자만 전달해 주세요!'}, status = 400)
