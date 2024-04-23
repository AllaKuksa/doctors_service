from django.urls import path
from doctors_service.views import (index,
                                   DoctorSpecialtyListView,
                                   DoctorSpecialtyDetailView,
                                   DoctorListView,
                                   DoctorDetailView,
                                   AppointmentListView,
                                   AppointmentDetailView,
                                   DoctorScheduleCreateView)

urlpatterns = [
    path("", index, name="index"),
    path("specialties/", DoctorSpecialtyListView.as_view(), name="specialties-list"),
    path("specialties/<int:pk>/", DoctorSpecialtyDetailView.as_view(), name="specialties-detail"),
    path("doctors/", DoctorListView.as_view(), name="doctors-list"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctors-detail"),
    path("appointments/", AppointmentListView.as_view(), name="appointments-list"),
    path("appointments/<int:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),
    path("doctors/<int:pk>/create_schedule/", DoctorScheduleCreateView.as_view(), name="doctor-schedule-form"),
]

app_name = "doctors_service"