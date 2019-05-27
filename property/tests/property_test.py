import json 
import jwt

from io import BytesIO
from PIL import Image
from datetime import datetime
from django.test import TestCase, Client
from unittest.mock import MagicMock, patch
from minibnb.settings import MINIBNB_SECRET_KEY
from requests_toolbelt.multipart.encoder import MultipartEncoder

from user.models import User
from property.models import Property
from datetime import datetime

def create_test_image():
    file = BytesIO()
    image = Image.new('RGBA', size=(50,50), color=(155,0,0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file

class PropertyTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(user_name="test", kakao_id=12345)

    def test_property_create(self):
        c = Client()

        test_user = User.objects.get(user_name="test")
        test_user.is_host = False
        encoded = self.getToken(test_user)
        test_image=create_test_image()
        print(test_image.getvalue())
        print(MultipartEncoder({'picture':create_test_image()}))

        multipart_data = MultipartEncoder({
            'name'        : '선릉 근처 근사한 숙소',
            'description' : '머물기 정말 편한 숙소입니다.',
            'address1'    : '서울시 성북구',
            'address2'    : '',
            'postal'      : '12345',
            'max_people'  : 4,
            'price'       : 50000,
            'picture1'    : create_test_image(),
            'picture2'    : create_test_image(),
            'picture3'    : create_test_image(),
            'picture4'    : create_test_image(),
            'picture5'    : create_test_image()
        })
        response = c.post(
                        '/property/create',
                        multipart_data,
                        **{'HTTP_AUTHORIZATION': encoded, 'content_type': 'multipart/form-data'} )
        new_property = Property.objects.get(user__id=test_user.id)
        self.assertEqual(response.status_code, 200)

        test_user.is_host = True 
        response = c.post(
                        '/property/create',
                        test_body,
                        **{'HTTP_AUTHORIZATION': encoded, 'content_type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'숙소가 이미 존재합니다.'})

    def test_property_delete(self):
        c = Client()

        test_user =User.objects.get(user_name="test")
        new_property = Property.objects.create(
            name='테스트집',
            description='테스트 설명',
            address1='주소1',
            address2='주소2',
            postal='12345',
            max_people=3,
            price=100_000,
            start_date=datetime.now(),
            end_date=None,
            user_id=test_user.id,
        )
        test_user.is_host = True
        test_user.save()
        encoded = self.getToken(test_user)
        test_body = {
            'property_id' : new_property.id
        }
        response = c.post(
                        '/property/delete',
                        json.dumps(test_body),
                        **{'HTTP_AUTHORIZATION': encoded, 'content_type': 'application/json'}
        )

        self.assertEqual(response.status_code,200)

    def tearDown(self):
        User.objects.get(user_name="test").delete()

    def getToken(self, test_user):
        return jwt.encode({'id': test_user.id}, MINIBNB_SECRET_KEY, algorithm='HS256').decode('UTF-8')
