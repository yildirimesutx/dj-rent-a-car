from rest_framework import serializers
from .models import Car, Reservation








class ReservationSerializer(serializers.ModelSerializer):
   
    car = serializers.StringRelatedField() #reservation modelindeki car fieldi default id geliyor, bu şekilde car modeldeki str geldi.
    

    class Meta:
        model = Reservation
        # fields = "__all__"
        fields = (
            
            "rent_start_date",
            "rent_end_date",
            "car"

        )


class CarSerializer(serializers.ModelSerializer):
    # cars = serializers.StringRelatedField()
    cars = ReservationSerializer()
    class Meta:
        model = Car
        fields = "__all__"        