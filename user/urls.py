from django.urls import path

from .views import KakaoSignupView

urlpatterns = [
    path('', KakaoSignupView.as_view()),        
]
