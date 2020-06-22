import json
import bcrypt
import jwt
import uuid

from .models           import Account, Profile
from api_test.settings import SECRET_KEY
from .utils            import login_required

from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.db              import IntegrityError, transaction, connection
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class AccountView(View):
    def get(self, request):
        return JsonResponse({'message':[
            '안녕하세요. 이 편지는 영국에서 최초로 시작되어 일년에 한바퀴 돌면서 받는 사람에게 행운을 주었고 지금은 당신에게로 옮겨진 이 편지는.... 농담입니다~;;;😆',
            '첫번째 미션을 가볍게 성공하신 여러분 환영합니다.🥳🥳🥳🥳',
            '이 미션은 두번째 미션을 위한 몸풀기 였습니다. ㅎㅎ',
            '여러분이 사용하신 GET 메소드는 지금처럼 무언가 데이터를 가져오기 위해 사용합니다.',
            '지금 여러분이 생각하시기에는 그냥 텍스트라고 보이시겠지만',
            '이 내용들 또한 JSON 데이터 형식으로 전달된 스트링 데이터 들입니다.',
            ' JSON 데이터의 예 {"name" : "wecode", "address" : "서울시 강남구 테헤란로 427 "}',
            '무언가 원하는 데이터를 호출하기 위해 사용하는 메소드가 바로 GET 입니다.',
            '이제 두번째 미션으로 진행하기위해 다시 /api 경로에 쿼리스트링 2번을 호출해주세요'
        ]}, status = 200)

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            validate_email(data['email'])
            if Account.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'이미 존재하는 메일 주소 입니다.'}, status = 400)
            with transaction.atomic():
                code = uuid.uuid4()
                profile = Profile(
                        code = code
                    )
                profile.save()

                Account(
                    name     = data['name'],
                    email    = data['email'],
                    password = bcrypt.hashpw(
                        data['password'].encode('utf-8'),
                        bcrypt.gensalt()).decode('utf-8'),
                        profile  = profile
                ).save()

            return JsonResponse({
                'message':[
                    '성공쓰~ 로그인 해주세요!',
                    '로그인 경로는 /account/sign-in 입니다 우선 GET으로 호출해 주세요',
                    '기록해 두세요', f'code : {code}'
                ]
            }, status = 200)

        except ValidationError:
            return JsonResponse({"message":"😱 이메일 형식이 아닙니다."}, status = 400)

        except IntegrityError:
            return JsonResponse({"message":"😪 중복 입니다."}, status = 400)

        except KeyError:
            return JsonResponse({"message":"☠️  혹시 빼놓은 키가 있을까요? 혹은 잘못된 키이름을 전달하신것 아닐까요?"}, status = 400)
        except json.JSONDecodeError:
            return JsonResponse({"message":"POST 에는 body에 json데이터를 주셔야 합니다. 확인해 주세요."}, status = 400)

    def get(self, request):
        message =[
            '회원 가입 입니다.회원가입은 GET일까요? POST일까요?',
            '여러분이 지금 엔드포인트를 호출한 메소드에 답이 있습니다.',
            '현재 메소드는 GET입니다. 그래서 이 안내문구를 보고 계십니다.',
            '회원 가입은POST 로 해야합니다.',
            'POST를 사용할 때에는 메소드도 선언하지만 동반되는 사항이 있습니다.',
            '바로 body에 들어갈 data인 JSON이겠죠.',
            '회원가입에 필요한 정보는 name, email, password 입니다.',
            '동일한 엔드포인트를 POST로 호출하고, 위의 정보에 해당하는 내용들을 작성해서 body에 담아 주세요!',
            '* Postman은 리퀘스트 작성시 body 탭에서 raw를 선택하고 추가옵션을 JSON으로 선택하신뒤에, 입력창에 JSON포맷으로 데이터를 작성하시면 됩니다.',
            '* httpie는 주소 뒤에  name='' email='' password=''로 추가 입력하시면 됩니다.',
            '😀😀😀😀😀😀 회원가입이 완료된 후 발급되는 code를 기록해 두세요!😀😀😀😀😀😀',
            '나중에 미션에 필요합니닷!'
        ]

        return JsonResponse({'message' : message}, status = 200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(email = data['email']).exists():
                user = Account.objects.get(email = data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
                    access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm = 'HS256')

                    return JsonResponse([{
                        'message' : [
                            '로그인에 성공하셨습니다. 축하드립니다.',
                            '이제 미션 3번을 진행하러 /api 경로에 쿼리스트링 3번을 호출해주세요.',
                            '😀😀😀😀 아래에 나오는 토큰도 잘 기록해 두세요! 😀😀😀😀'
                        ]},
                        {
                            'access_token' : access_token.decode('utf-8')
                        }],safe = False, status = 200)

                return JsonResponse({'message' : '💀 잘못된 비밀번호 입니다.'},status = 401)

            return JsonResponse({'message' : '🤖 계정을 확인 해주세요.'},status = 400)

        except KeyError:
            return JsonResponse({'message' : '☠️  혹시 빼놓은 키가 있을까요? 혹은 잘못된 키이름을 전달하신것 아닐까요?'}, status = 400)


    def get(self, request):
        message =['로그인 입니다😆 .로그인은 GET일까요? POST일까요?🤔 ',
                  '여러분이 지금 엔드포인트를 호출한 메소드에 답이 있습니다.',
                  '현재 메소드는 GET입니다. 그래서 이 안내문구를 보고 계십니다.',
                  '로그인 또한 POST 로 해야합니다.',
                  '바로 개인이 입력한 아이디와 패스워드 정보를 전송해서 비교하기 때문에 바로 전송시에 아이디와 패스워드를 body를 통해 전송 하기 때문입니다.',
                  '로그인에 필요한 정보는 email, password 입니다.',
                  '동일한 엔드포인트를 POST로 호출하고, 위의 정보에 해당하는 내용들을 작성해서 body에 담아 주세요!',
                  '🤠 Postman은 리퀘스트 작성시 body 탭에서 raw를 선택하고 추가옵션을 JSON으로 선택하신뒤에, 입력창에 JSON포맷으로 데이터를 작성하시면 됩니다.',
                  '🤖  httpie는 주소 뒤에 email="" password=""로 추가 입력하시면 됩니다.',
                  '😻 로그인 성공시에 리턴되는 것은 jwt라고 부르는 토큰 입니다.',
                  '🥺🥺🥺 잘 저장해서 가지고 계세요.🥺🥺🥺']

        return JsonResponse({'message':message}, status = 200)

class ProfileView(View):
    @login_required
    def get(self, request, code = None):
        if code:
            if Profile.objects.filter(code = code).exists():
                profile_data = Profile.objects.filter(code = code).values('hobby','address','code')

                return JsonResponse(
                    [
                        {'user_name':request.user.name},
                        {'profile':list(profile_data)}
                    ],safe = False, status = 200)

            return JsonResponse({'message' : '🤩 진짜 끝!!! 수고하셨습니다 🧑🏻‍💻👏🏻'}, status = 404)

        return JsonResponse({'message' : '경로에 😟 코드를 주세요!!'}, status = 404)

    @login_required
    def put(self, request, code):
        try:
            if Profile.objects.filter(code = code).exists():
                data = json.loads(request.body)
                Profile.objects.filter(code = code).update(**data)
                return JsonResponse({
                    'message' : [
                        '🥳 변경이 완료 되었습니다.',
                        '확인 하려면 GET으로 호출해주세요.',
                        '이로써 3번 미션이 완료 되었습니다.',
                        '마지막 미션인 /api 에 쿼리스트링 4번을 호출해주세요.'
                    ]
                }, status = 200)

            return JsonResponse({'message' : '코드를 확인해 주세요'}, status = 404)

        except KeyError:
            return JsonResponse({"message":"☠️  혹시 빼놓은 키가 있을까요? 혹은 잘못된 키이름을 전달하신것 아닐까요?"}, status = 400)

    @login_required
    def delete(self, request, code):
        if Profile.objects.filter(code = code).exists():
            Profile.objects.filter(code = code).delete()

            return JsonResponse({
                'message' : [
                    '삭제 되었습니다.',
                    '이로써 모든 미션이 종료 되었습니다',
                    '수고 하셨습니다.👏👏👏👏  삭제 확인을 위해 GET호출 한번 해주세요!'
                ]
            }, status = 200)

        return JsonResponse({'message' : '코드를 확인해 주세요'}, status = 404)


