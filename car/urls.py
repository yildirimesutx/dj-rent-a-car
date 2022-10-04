from django.urls import path
from .views import (
# CarView, 
ReservationView, 
CarListCreate,
CarUpdateDelete,
)
from rest_framework import routers


router = routers.DefaultRouter()

# router.register("cars", CarView)
router.register("resv", ReservationView)

urlpatterns = [
    path("list",CarListCreate.as_view()),
    path("list/<int:id>", CarUpdateDelete.as_view())
]
urlpatterns += router.urls 
