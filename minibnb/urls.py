from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('user', include('user.urls')),
    path('admin', admin.site.urls),
    path('property', include('property.urls')),
    #path(r'^booking', include(booking.urls)),
    #path(r'^talk'), include(talk.urls)
]
