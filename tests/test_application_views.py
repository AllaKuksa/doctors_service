from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from doctors_service.models import (
    DoctorSchedule,
    DoctorSpecialty,
    Appointment
)

APPOINTMENTS_LIST = reverse("doctors_service:appointments-list")
APPOINTMENT_FORM = reverse("doctors_service:appointment-form")


class PublicAppointmentViewsTestCase(TestCase):

    def setUp(self):
        self.specialty1 = DoctorSpecialty.objects.create(
            specialty="Cardiology"
        )
        self.specialty2 = DoctorSpecialty.objects.create(
            specialty="Dermatology"
        )
        self.doctor = get_user_model().objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
            password="<PASSWORD>",
            username="test_username",
            licence_number="TES12345",
            city="test_city",
            hospital="test_hospital",
        )
        self.doctor.specialty.add(self.specialty1, self.specialty2)
        self.doctor.save()

        self.schedule1 = DoctorSchedule.objects.create(
            doctor=self.doctor,
            date="2026-10-20",
            timeslot=5,
            is_booked=False
        )

    def test_appointment_create_login_not_required(self):
        response = self.client.get(APPOINTMENT_FORM)
        self.assertEqual(response.status_code, 200)

    def test_create_appointment(self):
        form_data = {
            "doctor": self.doctor.pk,
            "doctor_schedule": self.schedule1.pk,
            "first_name": "test_patient_first_name",
            "last_name": "test_patient_last_name",
            "email": "test123@test.com",
            "phone": "+380682222222",
            "insurance_number": "2345678765",
            "comments": "Check up"
        }
        response = self.client.post(
            APPOINTMENT_FORM,
            data=form_data,
        )
        appointment = Appointment.objects.get(
            doctor_id=self.doctor.pk,
            doctor_schedule_id=self.schedule1.pk
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(appointment.first_name, form_data["first_name"])
        self.assertEqual(appointment.last_name, form_data["last_name"])
        self.assertEqual(
            appointment.insurance_number,
            form_data["insurance_number"]
        )
        self.assertEqual(appointment.phone, form_data["phone"])
        self.assertRedirects(
            response,
            reverse(
                "doctors_service:appointment-confirm",
                kwargs={"pk": appointment.pk}
            )
        )


class PrivateAppointmentViewsTestCase(TestCase):
    def setUp(self):
        self.specialty1 = DoctorSpecialty.objects.create(
            specialty="Cardiology"
        )
        self.specialty2 = DoctorSpecialty.objects.create(
            specialty="Dermatology"
        )
        self.doctor = get_user_model().objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
            password="<PASSWORD>",
            username="test_username",
            licence_number="TES12345",
            city="test_city",
            hospital="test_hospital",
        )
        self.doctor.specialty.add(self.specialty1, self.specialty2)
        self.doctor.save()
        self.client.force_login(self.doctor)

        self.schedule1 = DoctorSchedule.objects.create(
            doctor=self.doctor,
            date="2026-10-20",
            timeslot=5,
            is_booked=False
        )
        self.schedule2 = DoctorSchedule.objects.create(
            doctor=self.doctor,
            date="2026-10-19",
            timeslot=4,
            is_booked=False
        )
        self.appointment1 = Appointment.objects.create(
            doctor=self.doctor,
            doctor_schedule=self.schedule1,
            first_name="test_patient_first_name1",
            last_name="test_patient_last_name1",
            email="test123@test.com",
            phone="+380682222222",
            insurance_number="2345678765",
        )
        self.appointment2 = Appointment.objects.create(
            doctor=self.doctor,
            doctor_schedule=self.schedule2,
            first_name="test_patient_first_name2",
            last_name="test_patient_last_name2",
            email="test12334@test.com",
            phone="+380682222223",
            insurance_number="2345678766",
        )

    def test_appointment_list_login_required(self):
        response = self.client.get(APPOINTMENTS_LIST)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_list_with_appointments(self):
        response = self.client.get(APPOINTMENTS_LIST)
        self.assertEqual(response.status_code, 200)
        appointments = Appointment.objects.all()
        self.assertEqual(
            list(response.context["appointments_list"]),
            list(appointments)
        )

    def test_appointments_list_pagination(self):
        response = self.client.get(APPOINTMENTS_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)

    def test_query_search_filter_by_city_of_doctor(self):
        response = self.client.get("/appointments/", {"date": "2026-10-20"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            [self.appointment1]
        )

    def test_search_with_empty_query(self):
        response = self.client.get("/appointments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["object_list"]),
            Appointment.objects.count()
        )

    def test_appointment_detail_information(self):
        response = self.client.get(
            reverse(
                "doctors_service:appointment-detail",
                kwargs={"pk": self.appointment1.pk}
            )
        )
        appointment_detail = response.context["appointment_detail"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            appointment_detail.first_name,
            self.appointment1.first_name
        )
        self.assertEqual(
            appointment_detail.last_name,
            self.appointment1.last_name
        )
        self.assertEqual(
            appointment_detail.doctor_schedule.time,
            self.appointment1.doctor_schedule.time
        )
