from django.urls import path

from .views import (
    KakaoSignupView,
    UserLoginView,
    GuestPageView,
    HostPageView,
    HostOrGuestView
)

urlpatterns = [
    path('/kakao', KakaoSignupView.as_view()),
    path('/id', UserLoginView.as_view()),
    path('/guestpage', GuestPageView.as_view()),
    path('/hostpage', HostPageView.as_view()),
    path('/ishost', HostOrGuestView.as_view()),
]
