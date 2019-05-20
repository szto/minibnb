from django.urls import path, include

urlpatterns = [
    path('user', include(user.urls)),
    path('property', include(property.urls)),
    path('booking', incloude(booking.urls))
]
