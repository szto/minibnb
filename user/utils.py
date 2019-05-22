import jwt

from django.http import HttpResponse, JsonResponse
from functools import wraps

from .models import User
from minibnb.settings import MINIBNB_SECRET_KEY

def login_decorator(f):
    @wraps(f)
    def decorated_function(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token:
            try:
                payload = jwt.decode(access_token, MINIBNB_SECRET_KEY, 'HS257')
            except jwt.InvalidTokenError:
                payload = None

            if payload is None: 
                return HttpResponse(status=401)

        else:
            return HttpResponse(status=401)

        request.user = User.objects.get(id=payload['id'])
        return f(self, request, *args, **kwargs)
    return decorated_function
