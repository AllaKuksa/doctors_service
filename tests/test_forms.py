from django.contrib.auth import get_user_model
from django.test import TestCase
from doctors_service.forms import (
    DoctorCreationForm,
    DoctorUpdateForm,
    AppointmentCreationForm)
from doctors_service.models import DoctorSpecialty, DoctorSchedule


class Forms(TestCase):

    def test_doctor_form_creation_with_additional_data(self):

        cardiology = DoctorSpecialty.objects.create(specialty="Cardiology")
        dermatology = DoctorSpecialty.objects.create(specialty="Dermatology")
        form_data = {
            "username": "test_user",
            "first_name": "Test",
            "last_name": "Test",
            "hospital": "Test hospital",
            "city": "Test city",
            "email": "test@test.com",
            "specialty": [cardiology.pk, dermatology.pk],
            "licence_number": "TES12345",
            "password1": "<PASSWORD>123",
            "password2": "<PASSWORD>123",
        }
        form = DoctorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["hospital"],
            form_data["hospital"]
        )
        self.assertEqual(
            form.cleaned_data["city"],
            form_data["city"]
        )
        self.assertEqual(
            form.cleaned_data["email"],
            form_data["email"]
        )
        self.assertEqual(
            form.cleaned_data["licence_number"],
            form_data["licence_number"]
        )
        self.assertEqual(
            form.cleaned_data["password1"],
            form_data["password1"]
        )
        self.assertEqual(
            form.cleaned_data["password2"],
            form_data["password2"]
        )
        specialties_names = [
            specialty.specialty for specialty in form.cleaned_data["specialty"]
        ]
        self.assertEqual(specialties_names, ["Cardiology", "Dermatology"])


class DoctorUpdateFormTest(TestCase):
    def test_update_valid_license_number_length_less_8(self):
        form_data = {
            "license_number": "TES1234",
        }
        form = DoctorUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_length_more_8(self):
        form_data = {
            "license_number": "TES123456",
        }
        form = DoctorUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_first_3_characters_upper(self):
        form_data = {
            "license_number": "Tes12345",
        }
        form = DoctorUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_licen_number_first_must_contain_3_char_upp(self):
        form_data = {
            "license_number": "12345678",
        }
        form = DoctorUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())

    def test_update_valid_license_number_last_5_characters_are_digits(self):
        form_data = {
            "license_number": "TES1234S",
        }
        form = DoctorUpdateForm(data=form_data)
        self.assertTrue(not form.is_valid())


class AppointmentCreateFormTest(TestCase):

    def test_create_appointment_form(self):
        specialty1 = DoctorSpecialty.objects.create(
            specialty="test_specialty1"
        )
        specialty2 = DoctorSpecialty.objects.create(
            specialty="test_specialty2"
        )
        doctor = get_user_model().objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
            password="<PASSWORD>",
            username="test_username1",
            licence_number="TES12345",
            city="test_city",
            hospital="test_hospital",
        )
        doctor.specialty.add(specialty1, specialty2)
        doctor.set_password("<PASSWORD>")
        doctor.save()

        doctor_schedule = DoctorSchedule.objects.create(
            doctor=doctor,
            date="2024-11-11",
            timeslot=2,
            is_booked=False
        )
        form_data = {
            "doctor": doctor.pk,
            "doctor_schedule": doctor_schedule.pk,
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@test.com",
            "phone": "+380682444444",
            "insurance_number": "9876543456",
        }
        form = AppointmentCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["doctor"].pk,
            form_data["doctor"]
        )
        self.assertEqual(
            form.cleaned_data["doctor_schedule"].pk,
            form_data["doctor_schedule"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["email"],
            form_data["email"]
        )
        self.assertEqual(
            form.cleaned_data["phone"],
            form_data["phone"]
        )
        self.assertEqual(
            form.cleaned_data["insurance_number"],
            form_data["insurance_number"]
        )
