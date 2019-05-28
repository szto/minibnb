from django.urls import path
from .views import PropertyAllView, PropertyLookUpView, PropertyDetailView


urlpatterns = [
    path('/all', PropertyAllView.as_view()),
    path('/', PropertyLookUpView.as_view()),
    path('/<int:pk>', PropertyDetailView.as_view())

]