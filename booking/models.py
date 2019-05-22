#from django.db import models
#
#from user.models import User
#
#class Booking(models.Model):
#   property = models.ForeignKey(Property, on_delet=models.CASCADE)
#   user = models.ForeignKey(User, on_delete=models.CASCADE)
#   check_in_date = models.DateField()
#   check_out_date = models.DateField()
#   price_per_day = models.DecimalField()
#   price_for_stay = models.DecimalField()
#   amount_paid = models.DecimalField()
#   is_refund = models.BooleanField(default=False)
#   cancel_date = models.DateField(default=None)
#   refund_paid = models.BooleanField(default=False)
#   booking_date = models.DateTimeField()
#   created_at = models.DataTimeField(auto_now_add=True)
#   modified_at = models.DateTimeField(auto_now=True)
#   status = models.BooleanField(default=True)
