from django.db import models

from user.models import User
from property.models import Property


class Booking(models.Model):
   property = models.ForeignKey(Property, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
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

   class Meta:
        db_table='bookings'
   def __str__(self):
        return str(self.property)
