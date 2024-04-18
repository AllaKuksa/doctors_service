from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic


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


class DoctorSpecialtyListView(generic.ListView):
    model = DoctorSpecialty
    paginate_by = 5
    template_name = "doctors/specialties_list.html"
    context_object_name = "specialties_list"


class DoctorSpecialtyDetailView(generic.DetailView):
    model = DoctorSpecialty
    template_name = "doctors/specialties_detail.html"
    context_object_name = "specialty"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specialty = self.get_object()
        doctors = specialty.doctors.all()
        context["doctors_list"] = doctors
        return context
