from django.urls import path, include
from .views import RegisterView

urlpatterns = [
  path('auth/', include('dj_rest_auth.urls')),
  # path('auth_r/regis/', include('dj_rest_auth.registration.urls')),
  path('register/', RegisterView.as_view())

]