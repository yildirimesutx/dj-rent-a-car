from django.shortcuts import render
from rest_framework import viewsets
from .models import Car, Reservation
from .serializers import CarSerializer, ReservationSerializer
from rest_framework.permissions import  IsAdminUser
from .permission import IsStafforReadOnly
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.



# class CarView(viewsets.ModelViewSet):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer
#     # permission_classes = [IsStafforReadOnly]
class CarListCreate(ListCreateAPIView):
     queryset = Car.objects.all()
     serializer_class = CarSerializer


# concrete Views update ve delete islemi sagliyor
class CarUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset =Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = "id"




class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
