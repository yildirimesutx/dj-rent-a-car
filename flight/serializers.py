from rest_framework import serializers

from .models import Flight, Passenger, Reservation

class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model= Flight
        fields = (
           "flight_number",
           "operation_airlines",
           "departure_city",
           "arrival_city",
           "date_of_departure",
           "etd"             
        )
        # fields = "__all__"


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model =Passenger
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer(many=True, required=True)
    flight = serializers.StringRelatedField() # create ederken kullanılmıyor read_only, bu sebeple id ile tanımlıyoruz, 
    flight_id = serializers.IntegerField(write_only=True)

    user =serializers.StringRelatedField()
    user_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Reservation
        # fields = "__all__" 
        fields = (
          "id",
          "flight",  # GET
          "flight_id", # POST
          "user",   # GET
          "user_id", # POST
          "passenger"
                
        )
        
    def create(self, validated_data):
        passenger_data = validated_data.pop('passenger')
        # <!-- datanın içinde pop ile passenger i yakaladık -->
        print(validated_data)
        validated_data['user_id'] = self.context['request'].user.id
        # <!-- login olan user atama yaptık, serializers içinde request.user ile atama yapamıyoruz -->
        reservation = Reservation.objects.create(**validated_data)
        # <!-- bir reservation da bir çok yolcu olacağından for ile devam ettik -->
        for passenger in passenger_data:
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
        reservation.save()
        return reservation           
