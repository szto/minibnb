from django.db import models

#class Talk(models.Model):
#    property = models.ForeignKey(Property, verbose_name="Property", on_delete=models.SET_NULL)
#    guest = models.ForeignKey(User, null=True, blank=True, verbose_name="Guest" on_delete=models.SET_NULL)
#    host = models.ForeignKey(User, on_delete=CASCADE, on_delete=models.SET_NULL )
#    body = models.textField("Body")
#    sent_at = models.DateTimeField("send at", null=True, blank=True)
#    read_at = models.DateTiemField("read at", null=True, blank=True)
#    replied_at = models.DateTiemField("replied at", null=True, blank=True)
#
#    class Meta:
#        db_table='talk'
#
#    def __str__(self):
#        return self.body
