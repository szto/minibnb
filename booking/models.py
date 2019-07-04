from django.db import models

from user.models import User
from property.models import Property

class BookingManager(models.Manager):
    def guest_booking_list(self, user):
        booking_list = Booking.objects.filter(guest=user).select_related()
        return booking_list

class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_user')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    price_per_day = models.IntegerField()
    price_for_stay = models.IntegerField()
    amount_paid = models.IntegerField()
    is_refund = models.BooleanField(default=False)
    cancel_date = models.DateField(default=None)
    refund_paid = models.BooleanField(default=False)
    booking_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    nights = models.IntegerField()
    accomodation = models.IntegerField()

    objects = models.Manager()
    managers = BookingManager()

    class Meta:
        db_table='bookings'

    def __str__(self):
        return str(self.property)

    def property_occupied(self, property_id, check_in_date, check_out_date):
        if Property.objects.filter(
                id=property_id,
                check_in_date__gte=check_in_date,
                check_out_date__lt=checkout_date
                ).exist():
            return True
        else:
            return False

