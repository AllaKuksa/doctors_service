from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from doctors_service.models import Doctor, DoctorSpecialty


class DoctorCreateForm(UserCreationForm):

    specialty = forms.ModelMultipleChoiceField(
        queryset=DoctorSpecialty.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Doctor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "licence_number",
            "city",
            "hospital",
            "specialty",
        )
