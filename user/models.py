from enum import Enum
from django.db import models

class LoginType(Enum):
    FACEBOOK = 1
    KAKAO = 2
    
    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in LoginType]

class User(models.Model):
    user_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    login_type = models.CharField(max_length=30, choices=LoginType.choices())
    id_kakao = models.CharField(max_length=250, default=None)
    is_host = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:

        db_table='users'
