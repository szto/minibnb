import requests, json, jwt

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .models import User

class KakaoSignupView(View):
    def post(self, request):
        #user_token = request.header['Authorization']

        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization':'KakaoAK d012af1a354d201b99dd7a9fac684141',
                  'Content-type' : 'application/x-www-form-urlencoded;charset=utf-8',
                }
        data = {
                'target_id_type':'user_id',
                'target_id': '1088893870'
                }
        print(json.dumps(data))
        kakao_response = requests.post(url, headers=headers , data=data , timeout=10)
        print(kakao_response.status_code, kakao_response.request.headers, kakao_response.request.body)
        print(kakao_response.text)

        return HttpResponse(status=200)


