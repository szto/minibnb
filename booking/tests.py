import json
import jwt

from datetime import datetime
from django.test import TestCase, Client

from user.models import User
from property.models import Property
from booking.models import Booking

class BookTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(user_name='test', kakao_id=12345)
        test_property = Property(
                    property_name = '선릉 근처 근사한 숙소',
                    description   = '머물기 정말 편한 숙소입니다.',
                    address1      = '서울시 성북구',
                    address2      = '',
                    postal        = '12345',
                    max_people    = 4,
                    price         = 50000,
        )
        test_property.save()

    def book_request(self):
        c = Client()
        encoded = self.getToken(test_user)
        data = {
                    'property_id'    : test_property.id,
                    'check_in_date'  : datetime.date(2019,5,10),
                    'check_out_date' : datetime.date(2019,5,15),
                    'booking_date'   : datetime.now()
        }
        response = c.post(
                    '/booking/request',
                    json.dumps(data),
                    **{'HTTP_AUTHORIZATION': encoded, 'content_type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqaul(response.json(),{'message':'예약이 정상적으로 요청되었습니다.'})
         
        
    def tearDown(self):
        User.objects.get(user_name='test').delete()

    def getToken(self, test_user):
        return jwt.encode({'id': test_user.id}, MINIBNB_SECRET_KEY, algorithm='HS256').decode('UTF-8')
