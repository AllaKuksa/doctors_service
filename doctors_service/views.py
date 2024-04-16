from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from doctors_service.models import Doctor, DoctorSpecialty, Appointment


def index(request: HttpRequest) -> HttpResponse:
    num_doctors = Doctor.objects.count()
    num_specialties = DoctorSpecialty.objects.count()
    num_appointments = Appointment.objects.count()
    num_patients = Appointment.objects.values("insurance_number").distinct().count()

    context = {
        "num_doctors": num_doctors,
        "num_specialties": num_specialties,
        "num_appointments": num_appointments,
        "num_patients": num_patients,
    }

    return render(request, "doctors/index.html", context=context)
