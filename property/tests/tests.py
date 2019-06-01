import json 
import jwt

from datetime import datetime
from django.test import TestCase, Client
from unittest.mock import MagicMock, patch
from minibnb.settings import MINIBNB_SECRET_KEY
from requests_toolbelt.multipart.encoder import MultipartEncoder

from user.models import User
from property.models import Property

class PropertyTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.get_or_create(user_name="test", kakao_id=12345, is_host = False)[0]

        def getToken(test_user):
            return jwt.encode({'id': test_user.id}, MINIBNB_SECRET_KEY, algorithm='HS256').decode('UTF-8')

        self.encoded = getToken(self.test_user)
        self.client = Client()

    def test_property_create(self):
        
        multipart_data = {
            'property_name' : '선릉 근처 근사한 숙소',
            'description'   : '머물기 정말 편한 숙소입니다.',
            'address1'      : '서울시 성북구',
            'address2'      : '',
            'postal'        : '12345',
            'max_people'    : '4',
            'price'         : '50000',
            'picture1'      : open('./property/tests/1234.png', 'rb'),
        }
        data = MultipartEncoder(multipart_data)

        response =  self.client.post(
                        '/property/create',
                        data=data.to_string(),
                        **{'HTTP_AUTHORIZATION': self.encoded, 'content_type': data.content_type} )
        new_property = Property.objects.get(user__id=self.test_user.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Property.objects.count(),1)

        self.test_user.is_host = True 
        response = self.client.post(
                        '/property/create',
                        data=data.to_string(),
                        **{'HTTP_AUTHORIZATION': self.encoded, 'content_type': data.content_type}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'숙소가 이미 존재합니다.'})

    def test_property_delete(self):

        multipart_data = {
            'property_name' : '선릉 근처 근사한 숙소',
            'description'   : '머물기 정말 편한 숙소입니다.',
            'address1'      : '서울시 성북구',
            'address2'      : '',
            'postal'        : '12345',
            'max_people'    : '4',
            'price'         : '50000',
            'picture1'      : open('./property/tests/1234.png', 'rb'),
        }
        data = MultipartEncoder(multipart_data)

        response =  self.client.post(
                        '/property/create',
                        data=data.to_string(),
                        **{'HTTP_AUTHORIZATION': self.encoded, 'content_type': data.content_type} )
        new_property = Property.objects.get(user__id=self.test_user.id)

        test_body = {
            'property_id' : new_property.id
        }
        response = self.client.post(
                        '/property/delete',
                        json.dumps(test_body),
                        **{'HTTP_AUTHORIZATION': self.encoded, 'content_type': 'application/json'}
        )

        self.assertEqual(response.status_code,200)
        self.assertEqual(Property.objects.count(),0)

    def tearDown(self):
        User.objects.get(user_name="test").delete()

