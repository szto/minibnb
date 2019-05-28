from django.db import models
from user.models import User


class State(models.Model):
    name = models.CharField(max_length=250)
    # code = models.CharField(max_length=10)
    status = models.IntegerField()
   
    class Meta:
        db_table='states'
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=250)
    # status = models.IntegerField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        db_table='cities'
    def __str__(self):
        return self.name

class Property(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    address = models.TextField()
    availability_type = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField()
    max_people = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        db_table='properties'
    def __str__(self):
        return self.name


class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.TextField()
    status = models.IntegerField()
    created = models.DateTimeField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table='property_images'
    # def __str__(self):
    #     return self.property