import json

from django.views import View
from django.http import JsonResponse, HttpResponse
from datetime import datetime

from .models import Booking
from user.utils import login_decorator

#@login_decorator
class BookRequestView(View):
    def post(self, request):
        guest = request.user
        property_id = request.POST.get('id')
        host = User.objects.get(property__id=property_id)

        check_in_date = request.POST.get['check_in_date']
        check_out_date = request.POST.get['check_out_date']
        nights = check_out_date - check_in_date

        if self.property_occupied(property_id, check_in_date, check_out_date):
            return JsonResponse({'message':'예약이 이미 존재합니다.'}, status=400)

        new_book = Booking(
            property = property_id,
            check_in_date = check_in_date,
            check_out_date = check_out_date,
            nights = nights,
            booking_date = datetime.now(),
            booking_status = WAITING
        )
        new_book.save()

        if new_book:
            book_response = {
                'message' : "예약이 정상적으로 요청되었습니다."
            }
            return JsonResponse(book_response, status=200)
        else:
            return JsonReponse({ \
                'message':'예약요청이 실패하였습니다.. 다시 시도하세요.'}, \
                status=400)

    def property_occupied(self, property_id, check_in_date, check_out_date):
        if Property.objects.filter(
                id=property_id, check_in_date__gte=check_in_date, \
                check_out_date__lt=checkout_date
                ).exist():
            return True
        else:
            return False

class BookConfirmView(View):
    @login_decorator
    def post(self):
        host = request.user
        response = request.POST
        booking_info = Booking.objects.get(id=response['booking_id'])

        if response['booking_accept']:
            booking_info.is_reserved = True
            booking_info.booking_date = datetime.now()
            return JsonResponse({'message':'예약이  확정되었습니다.'})
        else:
            return JsonResponse({
                'message':'예약 요청을 수락하지 않았습니다.'} \
                ,status=400)

    @login_decorator
    def get(self, request):
        host = request.user
        response = request.GET
        booking_list = Booking.objects.filter(
                property__id=response['property_id']
                )
        data = {
            'property_id' : booking_list.response['prepertu+id'],
            'booking_list' : {
                    'property_id'    : booking['property_id'],
                    'check_in_date'  : booking['check_in_date'],
                    'check_out_date' : booking['check_out_date'],
                    'price_per_day'  : booking['price_per_day'],
                    'total_price'    : booking['price_for_stay']
                }
        }
        return JsonResponse(data)

class GuestMyPageView(View):
    @login_decorator
    def get(self, request):
        guest = request.user
        response = request.GET

