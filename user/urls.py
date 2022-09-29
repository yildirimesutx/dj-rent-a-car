from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls"))

]