import json

from .models import Category

from django.views import View
from django.http  import HttpResponse,JsonResponse

MISSIONS = {
    '1' : 'GET 미션에 오신 여러분 환영합니다. GET 미션은 무엇일까요? 먼저 여러분이 미션을 수행할 장소인 현재 연결한 서버의 주소에 /api부분을 /account로 변경 후 입력해보세요. 이 경로를 호출하기 위해서 쿼리스트링은 필요하지 않습니다. 이번  미션은  /account 경로를 호출하는 것입니다.',
    '2' : 'POST 미션에 오신 여러분 환영합니다. POST 미션은 무엇일까요? 먼저 여러분이 미션을 수행할 장소인 현재 연결한 서버의 주소에 /account/sign-up 라고 변경 입력해보세요. 이번 미션은 POST메소드를 사용해 보는 것입니다. 과제의 안내대로 수행해 주세요.',
    '3' : 'PUT 미션에 오신 여러분 환영합니다. PUT 미션은 무엇일까요? 먼저 여러분이 미션을 수행할 장소인  /account/profile/에 회원가입 후 전달 받은 코드를 추가로 입력합니다. 예시) http://localhost:8000/account/profile/fc69c821-fdc7-413a-9c81-2bc7d96f31 이번 미션은 PUT 메소드를 사용해 보는 것입니다. 또한 경로를 호출 할때 메소드는 PUT을 선택 해야합니다. PUT은 어떨때 사용하는 메소드 일까요? 부분적인 업데이트 즉, 수정을 할때 사용 합니다. 이 메소드를 호출하고 접근하려면, 여러분 이 자기 자신이라는 증명을 해야합니다. 로그인을 하셨다면 access_token 이라는 것을 발급 받 으셨을 겁니다. headers에 Authorization이라는 key를 지정하고, 토큰값을 Value로 지정합니다. 앞으로 profile 경로에 접근할때는 항상 이 토큰이 전달 되어야 합니다. 그럼 마지막으로 PUT 메소드는 수정하는 메소드라고 했습니다. 수정을 하려면 데이터를 전달해야겠죠? 데이터를 전 달하려면 어떻게 해야하죠? 여러분이 과정을 잘 지나오셨다면 지금 입력하실 수 있습니다. 전달해야 할 데이터는 hobby와 address입니다. 취미와 주소 중 하나만 변경하고 싶다면 변경하셔도 작동합니다. PUT 메소드는 잘 사용하지 않는 추세로 POST로 많이 대체하고 있지만, 여러분이 기본적인 메소드 실행을 해보도록 하기위해 준비했습니다.',
    '4' : 'DELETE! 마지막 미션입니다. 이 번 미션도 token은 필요합니다. 메소드를 DELETE로 설정하시고, account/profile/코드 로 호출 만 하시면, 삭제가 완료 됩니다. 삭제가 완료됐는지 확인하려면 GET을 다시 해보시면 됩니다.  여기까지가 마지막 입니다. 실습진행하시느라 고생하셨습니다. DELETE는 점점 사용하지 않고 POST를 쓰는 추세이지만, 여러분의 실습을 위해 메소드화 했습니다. 참고해 주세요!'
}


class MissionView(View):
    def get(self, request):
        print(request.GET)
        category = request.GET.get('category', None)
        try:
            if category:
                result = [{
                    "name" : Category.objects.get(pk = category).name,
                    "description" : MISSIONS[category]
                }]
                return JsonResponse({"message":result}, status = 200)

            mission = [{
                "id"   : category.id,
                "name" : category.name
            } for category in Category.objects.all()]

            return JsonResponse([
                {
                    'message':[
                        'HTTP 메소드 연습장에 오신 여러분 환영 합니다.',
                        '아래의 목록은 여러분이 진행해야 할 메소드의 미션 목록 입니다.',
                        '해당 미션을 호출하시려면 특별한 호출을 해야만 합니다.',
                        '바로, 쿼리스트링 혹은 쿼리 파라미터 라고 부르는 요소 입니다.',
                        '😀 POSTMAN 항목에는 메소드 호출 부분 하단에 첫번째 탭인 Params 탭에 입력할 수 있습니다.',
                        '🐶 KEY에 category, VALUE에 1을 입력하시면 됩니다.',
                        '👩🏻‍💻 입력하시고나면 주소창에 보이는 주소값은 서버주소명/api?category=1 과 같이 표시될 것입니다.',
                        '🐭 httpie로 호출할 경우에는 본 경로를 입력한 다음 category==1과 같이 값을 전달하면 주소처리되어 호출합니다.'
                    ]
                },
                {'list':mission}], safe = False, status = 200)

        except Category.DoesNotExist:
            return JsonResponse({'message' : '🧐 쿼리 파리미터는 리스트에 있는 숫자만 전달해 주세요!'}, status = 400)
