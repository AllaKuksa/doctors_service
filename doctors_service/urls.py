from django.urls import path
from doctors_service.views import index, DoctorSpecialtyListView, DoctorSpecialtyDetailView


urlpatterns = [
    path("", index, name="index"),
    path("specialties/", DoctorSpecialtyListView.as_view(), name="specialties-list"),
    path("specialties/<int:pk>/", DoctorSpecialtyDetailView.as_view(), name="specialties-detail")
]

app_name = "doctors_service"