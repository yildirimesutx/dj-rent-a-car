from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Car(models.Model):
    car_brand = models.CharField(max_length=20)
    car_model = models.CharField(max_length=20)
    daily_price = models.CharField(max_length=20)
    is_available = models.BooleanField()
    place_number = models.CharField(max_length=20)
   

    def __str__(self):
        return f"{self.car_brand}-{self.car_model}"
    
class Reservation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    car = models.ForeignKey(Car, on_delete=models.CASCADE,related_name="cars")
    rent_start_date =models.DateTimeField()
    rent_end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.client}- {self.car}"
    