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
from booking.models import Booking
from property.models import Image, Property

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

class UserLoginView(View):
    def post(self, request):
        userid = json.loads(request.body)['userid']
        if userid is None:
            return HttpResponse(status=404)
        else:
            encoded = jwt.encode({'id':userid}, MINIBNB_SECRET_KEY, algorithm='HS256')
            data = {
                    'access_token': encoded.decode('UTF-8'),
                }
            return JsonResponse(data)

class GuestPageView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        booking_list = Booking.managers.guest_booking_list(user)
        booking_list_dict = [{
            'property' : {
                'property_id' : b.property.id,
                'name' : b.property.name,
                'description' : b.property.description,
                'address1' : b.property.address1,
                'address2' : b.property.address2,
                'host_id' : b.property.user.id,
            },
            'booking' : {
                'nights' : b.nights,
                'price' : b.price_per_day,
                'accomodation' : b.accomodation,
                'check_in_date' : b.check_in_date,
                'check_out_date' : b.check_out_date,
            },
            'image_list' : list(Image.objects.filter(property__id=b.property.id).values('image'))

        } for b in booking_list ]
        return JsonResponse({
            'booking_list' : booking_list_dict
        })

class HostPageView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        property = Property.objects.get(user=user)
        img = property.image_set
        reservation_list = Booking.objects.filter(property=property)
        host_view_dict = {
            'property' : {
                'property_id' : property.id,
                'max_people' : property.max_people,
                'name' : property.name,
                'description' : property.description,
                'price' : property.price,
                'address1' : property.address1,
                'address2' : property.address2,
                'image' : img.first().image,
            },
            'reservation_list' : [{
                'nights' : r.nights,
                'price' : r.price_per_day,
                'accomodation' : r.accomodation,
                'check_in_date' : r.check_in_date,
                'check_out_date' : r.check_out_date,
                'id' : r.id,
                'guest_id' : r.guest_id,
            } for r in reservation_list ]
        }
        return JsonResponse({
            'host_page' : host_view_dict
        })

class HostOrGuestView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        return JsonResponse({
            'is_host' : user.is_host
        })
