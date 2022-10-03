from django.urls import path
from .views import CarView, ReservationView
from rest_framework import routers


router = routers.DefaultRouter()

router.register("cars", CarView)
router.register("resv", ReservationView)

urlpatterns = [
    # path()
]
urlpatterns += router.urls 
