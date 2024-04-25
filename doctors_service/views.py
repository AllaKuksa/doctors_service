from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from doctors_service.forms import DoctorCreateForm
from doctors_service.models import Doctor, DoctorSpecialty, Appointment, DoctorSchedule


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


class DoctorListView(generic.ListView):
    model = Doctor
    template_name = "doctors/doctors_list.html"
    context_object_name = "doctors_list"
    paginate_by = 5


class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = "doctors/doctors_detail.html"
    context_object_name = "doctor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()

        doctor_schedule = doctor.doctor_schedule.all()

        available_schedule = [
            schedule for schedule in doctor_schedule if not schedule.appointments.exists()
        ]
        context["available_schedule"] = available_schedule
        return context


class AppointmentListView(LoginRequiredMixin, generic.ListView):
    model = Appointment
    template_name = "doctors/appointments_list.html"
    context_object_name = "appointments_list"
    paginate_by = 5


class AppointmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Appointment
    template_name = "doctors/appointment_detail.html"
    context_object_name = "appointment_detail"


class DoctorScheduleCreateView(LoginRequiredMixin, generic.CreateView):
    model = DoctorSchedule
    fields = "__all__"
    template_name = "doctors/doctor_schedule_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["doctor"] = self.request.user.id
        return initial

    def get_success_url(self):
        doctor_id = self.kwargs["pk"]
        return reverse_lazy("doctors_service:doctors-detail", kwargs={"pk": doctor_id})


class DoctorScheduleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DoctorSchedule
    template_name = "doctors/doctor_schedule_confirm_delete.html"

    def get_success_url(self):
        doctor_id = self.kwargs["pk"]
        return reverse_lazy("doctors_service:doctors-detail", kwargs={"pk": doctor_id})


class DoctorCreateView(generic.CreateView):
    form_class = DoctorCreateForm
    model = Doctor
    template_name = "doctors/doctor_create.html"
    success_url = reverse_lazy("doctors_service:doctors-list")


class DoctorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Doctor
    template_name = "doctors/doctor_create.html"
    form_class = DoctorCreateForm
    success_url = reverse_lazy("doctors_service:doctors-list")


class DoctorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Doctor
    success_url = reverse_lazy("doctors_service:index")