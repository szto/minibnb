import requests, json, jwt

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from minibnb.settings import MINIBNB_SECRET_KEY

from .models import User, LoginType
from .utils import login_decorator

class KakaoSignupView(View):
    def post(self, request):
        try: 
            user_token = json.loads(request.body)['Authorization']

        except Exception as e:
            print(e, "No Token information.")
            return HttpResponse(status=500)
        else:
            kakao_user=self.get_kakao_user(user_token)
            
            try:
                user, is_created = User.objects.get_or_create(id_kakao=kakao_user['id'])
                user.email = (kakao_user['email'] or None)
                user.user_name = (kakao_user['nickname'] or None)
                user.login_type = LoginType.KAKAO
                user.save()

                encoded = jwt.encode({'id':user.id}, MINIBNB_SECRET_KEY, algorithm='HS256')
                return JsonResponse({
                        'access_token': encoded.decode('UTF-8'),
                        'is_host': user.is_host,
                        'is_created': is_created,
                        'user_info': kakao_user,
                    })

            except Exception as e:
                print(e, "Token is not accepted")
    
    @login_decorator
    def get(self, request):
        return JsonResponse({
                'user_name':request.user.user_name
            })

    def get_kakao_user(self, user_token):
        try:
            url = 'https://kapi.kakao.com/v2/user/me'
            headers = {'Authorization':f'Bearer {user_token}',
                      'Content-type' : 'application/x-www-form-urlencoded;charset=utf-8',
                    }
            kakao_response = requests.post(url, headers=headers, timeout=10).json()
            kakao_userinfo = {
                        'id': kakao_response['id'],
                        'nickname' : kakao_response['properties']['nickname'],
                        'thumbnail_image' : kakao_response['properties']['thumbnail_image'],
                        'email' : (kakao_response['kakao_account']['email'] or None) 
                    } 
            return kakao_userinfo
        except Exception as s:
            print(s)
            return None 

#페이스북 로그인 프론트엔드 커뮤니케이션 기다리는 중
#class FacebookView(View):
#    def POST(self, request):
#        return HttpResponse(status=200)
#    
#    def get_facebook_user(self, user_token):
#        url = ''
