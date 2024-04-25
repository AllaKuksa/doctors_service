from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from doctors_service.models import Doctor, DoctorSpecialty


def validate_licence_number(licence_number):
    if len(licence_number) != 8:
        raise ValidationError("License number should consist of 8 characters")
    elif not licence_number[:3].isupper() or not licence_number[:3].isalpha():
        raise ValidationError("First 3 characters should be uppercase letters")
    elif not licence_number[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return licence_number


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