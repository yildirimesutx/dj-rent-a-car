from rest_framework import serializers
from .models import Car, Reservation








class CarReservationSerializer(serializers.ModelSerializer):
   
    # car = serializers.StringRelatedField()
     #reservation modelindeki car fieldi default id geliyor, bu şekilde car modeldeki str geldi.
    # car_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"
        # fields = (
            
        #     "rent_start_date",
        #     "rent_end_date",
        #     "car"

        # )


class CarSerializer(serializers.ModelSerializer):
    # cars = serializers.StringRelatedField()
    cars = CarReservationSerializer(read_only=True)
    # cars = ReservationSerializer() # default olarak write_only geliyor, create ederken ihtiyacimiz olmadigindan read_only yaptık 
    class Meta:
        model = Car
        fields = "__all__"        