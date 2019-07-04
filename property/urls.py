from django.urls import path
from .views import (
    PropertyAllView,
    PropertyLookUpView,
    PropertyDetailView,
    PropertyCreateView,
    PropertyDeleteView,
)

urlpatterns = [
    path('/all', PropertyAllView.as_view()),
    path('/', PropertyLookUpView.as_view()),
    path('/<int:pk>', PropertyDetailView.as_view()),
    path('/create' , PropertyCreateView.as_view()),
    path('/delete', PropertyDeleteView.as_view()),
    path('/userid', PropertyDeleteView.as_view()),

]
