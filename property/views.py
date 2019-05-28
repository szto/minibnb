from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Property,Image
from booking.models import Booking
from django.core import serializers
import json, operator
from django.db.models import Q
from datetime import datetime


#검색
class PropertyLookUpView(View):
    
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
                'property_address': property['address'],
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
                'property_address': property['address'],
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
