from django.urls import path
from doctors_service.views import (index,
                                   DoctorSpecialtyListView,
                                   DoctorSpecialtyDetailView,
                                   DoctorListView,
                                   DoctorDetailView)

urlpatterns = [
    path("", index, name="index"),
    path("specialties/", DoctorSpecialtyListView.as_view(), name="specialties-list"),
    path("specialties/<int:pk>/", DoctorSpecialtyDetailView.as_view(), name="specialties-detail"),
    path("doctors/", DoctorListView.as_view(), name="doctors-list"),
    path("doctors/<int:pk>", DoctorDetailView.as_view(), name="doctors-detail"),
]

app_name = "doctors_service"