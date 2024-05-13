from django.contrib.auth import get_user_model
from django.test import TestCase
from doctors_service.models import (
    DoctorSpecialty,
    DoctorSchedule,
    Appointment
)


class ModelsTestCase(TestCase):

    def setUp(self) -> None:
        self.user_doctor = get_user_model().objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
            password="<PASSWORD>",
            username="test_username",
        )
        self.date = "2024-12-24"
        self.doctor_schedule = DoctorSchedule.objects.create(
            doctor=self.user_doctor,
            date=self.date,
            timeslot=1,
            is_booked=False
        )

    def test_doctor_specialty_str(self):
        specialty = DoctorSpecialty.objects.create(
            specialty="test_specialty"
        )
        self.assertEqual(
            str(specialty), "test_specialty"
        )

    def test_doctor_str(self):
        self.assertEqual(
            str(self.user_doctor),
            f"{self.user_doctor.first_name} {self.user_doctor.last_name}"
        )

    def test_create_doctor_with_additional_information(self):
        first_name = "test_first_name"
        last_name = "test_last_name"
        password = "<PASSWORD>"
        username = "test_username1"
        licence_number = "TES12345"
        city = "test_city"
        hospital = "test_hospital"
        specialty1 = DoctorSpecialty.objects.create(
            specialty="test_specialty1"
        )
        specialty2 = DoctorSpecialty.objects.create(
            specialty="test_specialty2"
        )
        doctor = get_user_model().objects.create(
            first_name=first_name,
            last_name=last_name,
            password=password,
            username=username,
            licence_number=licence_number,
            city=city,
            hospital=hospital,
        )
        doctor.specialty.add(specialty1, specialty2)
        doctor.set_password(password)
        doctor.save()
        self.assertEqual(doctor.first_name, first_name)
        self.assertEqual(doctor.last_name, last_name)
        self.assertEqual(doctor.username, username)
        self.assertEqual(doctor.licence_number, licence_number)
        self.assertEqual(doctor.city, city)
        self.assertEqual(doctor.hospital, hospital)
        self.assertIn(specialty1, doctor.specialty.all())
        self.assertIn(specialty2, doctor.specialty.all())
        self.assertEqual(doctor.specialty.count(), 2)
        self.assertTrue(doctor.check_password(password))

    def test_doctor_schedule_str(self):
        self.assertEqual(
            str(self.doctor_schedule),
            f"{self.doctor_schedule.date} / {self.doctor_schedule.time}"
        )

    def test_time_properly(self):
        self.assertEqual(self.doctor_schedule.time, "10:00 – 11:00")

    def test_create_doctor_schedule(self):
        self.assertEqual(self.doctor_schedule.doctor, self.user_doctor)
        self.assertEqual(self.doctor_schedule.date, self.date)
        self.assertEqual(self.doctor_schedule.timeslot, 1)
        self.assertFalse(self.doctor_schedule.is_booked)

    def test_appointment_str(self):
        appointment = Appointment.objects.create(
            doctor=self.user_doctor,
            doctor_schedule=self.doctor_schedule,
            first_name="test_first_name",
            last_name="test_last_name",
            email="test@gmail.com",
            phone="+380682222222",
            insurance_number=12345678901,
        )
        self.assertEqual(
            str(appointment),
            f"patient {appointment.first_name} {appointment.last_name} "
            f"has a visit - {appointment.doctor_schedule}"
        )

    def test_appointment_creat(self):
        patient_first_name = "test_first_name"
        patient_last_name = "test_last_name"
        email = "test@gmail.com"
        phone = "+380682222222"
        patient_insurance_number = 12345678901
        comments = ""
        appointment = Appointment.objects.create(
            doctor=self.user_doctor,
            doctor_schedule=self.doctor_schedule,
            first_name=patient_first_name,
            last_name=patient_last_name,
            email=email,
            phone=phone,
            insurance_number=patient_insurance_number,
            comments=comments
        )
        self.assertEqual(appointment.first_name, patient_first_name)
        self.assertEqual(appointment.last_name, patient_last_name)
        self.assertEqual(appointment.email, email)
        self.assertEqual(appointment.phone, phone)
        self.assertEqual(
            appointment.insurance_number,
            patient_insurance_number
        )
        self.assertEqual(appointment.comments, comments)
