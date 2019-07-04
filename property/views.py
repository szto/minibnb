import json
import operator
import boto3
import logging
import uuid
import my_settings

from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core import serializers
from django.db.models import Q

from .models import Property,Image
from booking.models import Booking
from user.utils import login_decorator

logger = logging.getLogger('property')

#검색
class PropertyLookUpView(View):

    model = Property

#특정 집 가져오기
class PropertyView(View):
    
    model = Property

    def get(self, request):
    
        QUERY_LOOKUP = {
        "checkin_date" : lambda checkin_date: ~Q(booking__check_in_date__gte=checkin_date),
        "checkout_date" : lambda checkout_date: ~Q(booking__check_out_date__lte=checkout_date), 
        "max_people" : lambda max_people: Q(max_people__gte=max_people),
        "state" : lambda state: Q(state=state),
        "city" : lambda city: Q(city=city)
    }

        q_object = Q()
        for input_key in request.GET:
            if input_key == 'checkin_date' or input_key == 'checkout_date':
                q_object.add(QUERY_LOOKUP[input_key](request.GET[input_key]),Q.OR)
            else:      
                q_object.add(QUERY_LOOKUP[input_key](request.GET[input_key]),Q.AND) 
       
            unbooked_properties = Property.objects.filter(q_object)
   
      
        data = serializers.serialize('json', unbooked_properties)
        return HttpResponse(data, content_type='application/json')
      
#디테일 화면
class PropertyDetailView(View):
    
    def get(self, request, pk):

        properties = Property.objects.filter(id=pk)
        properties_list = list(properties.values())
        images = Image.objects.filter(property__in=properties).select_related()
        
        data = [
            {
                'property_id': property['id'],
                'property_name': property['name'],
                "description": property['description'],
                'property_address': property['address1'],
                'property_price': property['price'],
                "latitude": property['latitude'],
                "longitude": property['longitude'],
                "max_people": property['max_people'],
                # "user": property['user'],
                # "state": property['state'],
                # "city": property['city'],
                'image_list': list(images.filter(property__id=property['id']).values())
            } for property in properties_list
        ]
        

        return JsonResponse(data, safe=False)


#모든 집
class PropertyAllView(View):
    
    model = Property   
    def get(self, request):
        properties = Property.objects.all()
        properties_list = list(properties.values())
        images = Image.objects.filter(property__in=properties).select_related()
        data = [
            {
                'property_id': property['id'],
                'property_name': property['name'],
                "description": property['description'],
                'property_address': property['address1'],
                'property_price': property['price'],
                "latitude": property['latitude'],
                "longitude": property['longitude'],
                "max_people": property['max_people'],
                # "user": property['user'],
                # "state": property['state'],
                # "city": property['city'],
                'image_list': list(images.filter(property__id=property['id']).values())
            } for property in properties_list
        ]
        
        return JsonResponse(data, safe=False)

class PropertyCreateView(View):

    @login_decorator
    def post(self, request):
        user = request.user
        property_get = request.POST

        if user.is_host:
            return JsonResponse({'message':'숙소가 이미 존재합니다.'}, status=400)
        else:
            try:
                new_property = Property(
                                name        = property_get.get('property_name'),
                                description = property_get.get('description'),
                                address1    = property_get.get('address1'),
                                address2    = property_get.get('address2',None),
                                postal      = property_get.get('postal'),
                                max_people  = property_get.get('max_people'),
                                price       = property_get.get('price'),
                                user_id     = user.id
                        )
                new_property.save()
                user.is_host = True
                user.save()

            except Exception as e:
                logger.exception(e)
                return JsonResponse({'message':'숙소저장 시 오류가 생겼습니다.'}, status=400)

        self.photos_to_aws(request, new_property.id)

        data = {
                'property_id': new_property.id,
                'message':'성공적으로 숙소가 등록되었습니다.' 
        }
        return JsonResponse(data, status=200)
        
    def photos_to_aws(self, request, property_id):

        s3_client = boto3.client(
            's3',
            aws_access_key_id     = my_settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = my_settings.AWS_SECRET_ACCESS_KEY
        )
        
        for key, image in request.FILES.items():
            extension = image.name.split('.')[-1]
            file_name = f"{uuid.uuid4()}.{extension}" 
            test = s3_client.upload_fileobj(
                image,
                "minibnb-test",
                file_name,
                ExtraArgs={
                    'ContentType': image.content_type
                }
            
            )
            new_image = Image(
                image    = "https://s3.ap-northeast-2.amazonaws.com/minibnb-test/"+file_name,
                added_by = request.user,
                property_id = property_id,
                status = True
            )
            new_image.save()

class PropertyDeleteView(View):
    @login_decorator
    def post(self, request):
        user = request.user
        property_get = json.loads(request.body)
        if user.is_host:
            Property.objects.get(id=property_get['property_id']).delete()
            user.is_host = False
            user.save()
            return JsonResponse({'message':'숙소가 성공적으로 지워졌습니다'}, status=200)
        else:
            return JsonResponse({'message':'숙소가 존재하지 않습니다.'}, status=400)

