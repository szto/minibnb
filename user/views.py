import jwt
import json

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .models import User

class KakaoSignupView(View):
    def post(self, request):
        payloads = json.loads(request.body)

        
        
