from rest_framework import serializers
from .models import Car, Reservation





class CarSerializer(serializers.ModelSerializer):
    car = serializers.StringRelatedField()
    class Meta:
        model = Car
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    # cars = CarSerializer(many=True)
    cars = CarSerializer(many=True, required=False)
    # cars = serializers.StringRelatedField(many=True)
    class Meta:
        model = Reservation
        fields = "__all__"