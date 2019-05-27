from django.db import models
from user.models import User


class State(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=10)
    status = models.IntegerField()
   
    class Meta:
        db_table='states'
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=250)
    status = models.IntegerField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        db_table='cities'
    def __str__(self):
        return self.name

class Property(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    latitude = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=50, null=True)
    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500, null=True)
    postal = models.CharField(max_length=10)
    availability_type = models.IntegerField(null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    price = models.IntegerField()
    max_people = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE,default=None,null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE,default=None,null=True)

    class Meta:
        db_table='properties'
    def __str__(self):
        return self.name

class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.TextField()
    status = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table='property_images'
    def __str__(self):
        return self.property
