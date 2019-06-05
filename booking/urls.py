from django.urls import path
from .views import BookRequestView, BookConfirmView

urlpatterns = [
        path('/request', BookRequestView.as_view()),
        path('/confirm', BookConfirmView.as_view()),
]

