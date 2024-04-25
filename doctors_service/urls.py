from django.urls import path
from doctors_service.views import (index,
                                   DoctorSpecialtyListView,
                                   DoctorSpecialtyDetailView,
                                   DoctorListView,
                                   DoctorDetailView,
                                   AppointmentListView,
                                   AppointmentDetailView,
                                   DoctorScheduleCreateView,
                                   DoctorScheduleDeleteView,
                                   DoctorCreateView,
                                   DoctorUpdateView,
                                   DoctorDeleteView)

urlpatterns = [
    path("", index, name="index"),
    path("specialties/", DoctorSpecialtyListView.as_view(), name="specialties-list"),
    path("specialties/<int:pk>/", DoctorSpecialtyDetailView.as_view(), name="specialties-detail"),
    path("doctors/", DoctorListView.as_view(), name="doctors-list"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctors-detail"),
    path("appointments/", AppointmentListView.as_view(), name="appointments-list"),
    path("appointments/<int:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),
    path("doctors/<int:pk>/create_schedule/", DoctorScheduleCreateView.as_view(), name="doctor-schedule-form"),
    path(
        "doctors/<int:doctor_id>/delete_schedule/<int:pk>/",
        DoctorScheduleDeleteView.as_view(),
        name="doctor-schedule-confirm-delete"),
    path("doctors/create/", DoctorCreateView.as_view(), name="doctor-create"),
    path("doctors/<int:pk>/update/", DoctorUpdateView.as_view(), name="doctor-update"),
    path("doctors/<int:pk>/deleted/", DoctorDeleteView.as_view(), name="doctor-delete")
]

app_name = "doctors_service"