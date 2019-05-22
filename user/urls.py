from django.urls import path

from .views import KakaoSignupView

urlpatterns = [
    path('/kakao', KakaoSignupView.as_view()),        
]
