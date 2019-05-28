from django.contrib import admin
from .models import Property, Image, City, State

admin.site.register(Property)
admin.site.register(Image)
admin.site.register(City)
admin.site.register(State)