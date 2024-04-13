from django.urls import path
from doctors_service.views import index


urlpatterns = [
    path("", index, name="index"),
]

app_name = "doctors_service"