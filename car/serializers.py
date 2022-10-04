from rest_framework import serializers
from .models import Car, Reservation





class CarSerializer(serializers.ModelSerializer):
    cars = serializers.StringRelatedField()
    # cars = ReservationSerializer(many=True)
    class Meta:
        model = Car
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    # cars = CarSerializer(many=True)
    # cars = CarSerializer(many=True, required=False)
    # car = serializers.StringRelatedField() #reservation modelindeki car fieldi default id geliyor, bu şekilde car modeldeki str geldi.
    # user = CarSerializer(many=True, required=False)

    class Meta:
        model = Reservation
        fields = "__all__"
        # fields = (
            
        #     rent_start_date,
        #     rent_end_date,
        #     cars

        # )