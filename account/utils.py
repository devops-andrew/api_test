import jwt 
import json

from .models import Account
from api_test.settings import SECRET_KEY

from django.http import JsonResponse


def login_required(func):

   def wrapper(self, request, *args, **kwargs):
       access_token = request.headers.get('Authorization', None)
       secret = SECRET_KEY
       if access_token:
           try:
               decode = jwt.decode(access_token, secret, algorithms=['HS256'])
               user_id = decode["user_id"]
               user = Account.objects.get(id=user_id)
               request.user = user
           except jwt.DecodeError:
               return JsonResponse({"message" : "🤮 잘못된 토큰 입니다."}, status = 403)
           except User.DoesNotExists:
               return JsonResponse({"message" : "😜 존재하지 않는 아이디 입니다."}, status=401)

           return func(self, request, *args, **kwargs)

       return JsonResponse({"message" : "😫 로그인이 필요한 서비스 입니다."}, status=401)

   return wrapper
