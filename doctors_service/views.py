from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from doctors_service.forms import (DoctorCreationForm,
                                   DoctorUpdateForm,
                                   AppointmentCreationForm,
                                   DoctorSearchForm,
                                   AppointmentSearchForm)
from doctors_service.models import (Doctor,
                                    DoctorSpecialty,
                                    Appointment,
                                    DoctorSchedule)


def index(request: HttpRequest) -> HttpResponse:
    num_doctors = Doctor.objects.count()
    num_specialties = DoctorSpecialty.objects.count()
    num_appointments = Appointment.objects.count()
    num_patients = Appointment.objects.values(
        "insurance_number").distinct().count()

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DoctorListView, self).get_context_data(**kwargs)
        city = self.request.GET.get("city", "")
        context["search_form"] = DoctorSearchForm(
            initial={
                "city": city
            }
        )
        return context

    def get_queryset(self):
        queryset = Doctor.objects.prefetch_related("specialty")
        form = DoctorSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(city__icontains=form.cleaned_data["city"])
        return queryset


class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = "doctors/doctors_detail.html"
    context_object_name = "doctor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()

        doctor_schedule = doctor.doctor_schedule.all()

        available_schedule = [schedule for schedule in doctor_schedule
                              if not schedule.is_booked]
        context["available_schedule"] = available_schedule
        return context


class DoctorCreateView(generic.CreateView):
    model = Doctor
    form_class = DoctorCreationForm
    success_url = reverse_lazy("doctors_service:doctors-list")
    template_name = "doctors/doctor_form.html"


class DoctorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Doctor
    form_class = DoctorUpdateForm
    template_name = "doctors/doctor_form.html"

    def get_success_url(self):
        doctor_id = self.kwargs["pk"]
        return reverse_lazy(
            "doctors_service:doctors-detail",
            kwargs={"pk": doctor_id}
        )


class DoctorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Doctor
    template_name = "doctors/doctor_delete.html"

    def get_success_url(self):
        doctor_id = self.kwargs["pk"]
        return reverse_lazy(
            "doctors_service:doctors-detail",
            kwargs={"pk": doctor_id}
        )


class AppointmentListView(LoginRequiredMixin, generic.ListView):
    model = Appointment
    template_name = "doctors/appointments_list.html"
    context_object_name = "appointments_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AppointmentListView, self).get_context_data(**kwargs)
        date = self.request.GET.get("date", "")
        context["search_form"] = AppointmentSearchForm(
            initial={
                "date": date
            }
        )
        return context

    def get_queryset(self):
        queryset = Appointment.objects.select_related(
            "doctor",
            "doctor_schedule"
        )
        form = AppointmentSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data["date"] is not None:
            return queryset.filter(
                doctor_schedule__date__icontains=form.cleaned_data["date"]
            )
        return queryset


class AppointmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Appointment
    template_name = "doctors/appointment_detail.html"
    context_object_name = "appointment_detail"

    def get_queryset(self):
        queryset = Appointment.objects.select_related(
            "doctor",
            "doctor_schedule"
        )
        return queryset


class AppointmentConfirmationDetailView(generic.DetailView):
    model = Appointment
    context_object_name = "appointment"
    template_name = "doctors/appointment_confirm.html"


class AppointmentCreateView(generic.CreateView):
    model = Appointment
    form_class = AppointmentCreationForm
    template_name = "doctors/appointment_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "doctors_service:appointment-confirm",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.doctor_schedule.is_booked = True
        self.object.doctor_schedule.save()
        return response


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
        return reverse_lazy(
            "doctors_service:doctors-detail",
            kwargs={"pk": doctor_id}
        )


class DoctorScheduleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DoctorSchedule
    template_name = "doctors/doctor_schedule_confirm_delete.html"

    def get_success_url(self):
        doctor_id = self.kwargs["pk"]
        return reverse_lazy(
            "doctors_service:doctors-detail",
            kwargs={"pk": doctor_id}
        )


def load_doctor_schedule(request):
    doctor_id = request.GET.get("doctor")
    doctor_schedules = DoctorSchedule.objects.filter(
        doctor_id=doctor_id,
        is_booked=False
    )
    return render(
        request,
        "doctors/doctor_schedules_dropdown_list_options.html",
        {"doctor_schedules": doctor_schedules}
    )
