from django.urls import path, include

urlpatterns = [
    path(r'^user', include('user.urls')),
    #path(r'^property', include(property.urls)),
    #path(r'^booking', include(booking.urls)),
    #path(r'^talk'), include(talk.urls)
]
