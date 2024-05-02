from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from doctors_service.models import (Doctor,
                                    DoctorSpecialty,
                                    Appointment,
                                    DoctorSchedule)


def validate_licence_number(licence_number):
    if len(licence_number) != 8:
        raise ValidationError("License number should consist of 8 characters")
    elif not licence_number[:3].isupper() or not licence_number[:3].isalpha():
        raise ValidationError("First 3 characters should be uppercase letters")
    elif not licence_number[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return licence_number


def validate_insurance_number(insurance_number):
    if len([insurance_number]) != 10:
        raise ValidationError(
            "Insurance number should consist of 10 characters"
        )
    elif not insurance_number.isdigit():
        raise ValidationError(
            "Insurance number should consist of 10 digits"
        )


class DoctorCreationForm(UserCreationForm):

    specialty = forms.ModelMultipleChoiceField(
        queryset=DoctorSpecialty.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    hospital = forms.CharField(required=True)
    city = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Doctor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "licence_number",
            "city",
            "hospital",
            "specialty",
        )

    def clean_licence_number(self):
        return validate_licence_number(self.cleaned_data["licence_number"])


class DoctorUpdateForm(forms.ModelForm):

    specialty = forms.ModelMultipleChoiceField(
        queryset=DoctorSpecialty.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Doctor
        fields = ["licence_number", "city", "hospital", "specialty"]

    def clean_licence_number(self):
        return validate_licence_number(self.cleaned_data["licence_number"])


class AppointmentCreationForm(forms.ModelForm):

    doctor_schedule = forms.ModelChoiceField(
        queryset=DoctorSchedule.objects.filter(is_booked=False)
    )

    class Meta:
        model = Appointment
        fields = "__all__"

    def clean_insurance_number(self):
        return validate_insurance_number(self.cleaned_data["insurance_number"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doctor_schedule"].queryset = DoctorSchedule.objects.none()

        if "doctor" in self.data:
            try:
                doctor_id = int(self.data.get("doctor"))
                self.fields["doctor_schedule"].queryset = (
                    DoctorSchedule.objects.filter(doctor_id=doctor_id)
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["doctor_schedule"].queryset = (
                self.instance.doctor.doctor_schedule_set
            )


class DoctorSearchForm(forms.Form):
    city = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by city"}
        )
    )


class AppointmentSearchForm(forms.Form):
    date = forms.DateField(
        required=False,
        label="",
        widget=forms.DateInput(
            attrs={"placeholder": "Search by date YYYY-MM-DD"}
        )
    )
