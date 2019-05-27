import requests
import json
import jwt
import logging

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
            logger.exception(e)
            return HttpResponse(status=500)
        else:
            kakao_user=self.get_kakao_user(user_token)
            try:
                user, is_created = User.objects.get_or_create(kakao_id=kakao_user['kakao_id'])
                if is_created == True:
                    user.email = kakao_user.get('email', None)
                    user.user_name = kakao_user.get('nickname', None)
                    user.login_type = LoginType.KAKAO
                    user.is_host = False
                    user.save()

                encoded = jwt.encode({'id':user.id}, MINIBNB_SECRET_KEY, algorithm='HS256')
                data = {
                        'access_token': encoded.decode('UTF-8'),
                        'is_host': user.is_host,
                        'is_created': is_created,
                        'user_info': kakao_user,
                    }

                return JsonResponse(data)

            except Exception as e:
                logging.exception("Error occured on /user/kakao")
                return JsonResponse({"message":"에러가 발생했습니다."})
    
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
                        'kakao_id': kakao_response['id'],
                        'nickname' : kakao_response['properties']['nickname'],
                        'thumbnail_image' : kakao_response['properties']['thumbnail_image'],
                        'email' : kakao_response.get('kakao_account', None).get('email',None)
                    } 
            return kakao_userinfo
        except Exception as s:
            logging.exception("Error occured on /user/kakao, get_kakao_user method")
            return None 

