import jwt

from django.test import TestCase, Client
from user.models import User 
from minibnb.settings import MINIBNB_SECRET_KEY

class UserTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(user_name="test" ,kakao_id=12345)

    def test_user_login(self):
        c = Client()

        test_user = User.objects.get(user_name="test")
        encoded = jwt.encode({'id':test_user.id}, MINIBNB_SECRET_KEY, algorithm='HS256').decode('UTF-8')
        response = c.get('/user/kakao', **{'HTTP_AUTHORIZATION':encoded, 'content_type':'application/json'})
        
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.get(user_name="test").delete()

