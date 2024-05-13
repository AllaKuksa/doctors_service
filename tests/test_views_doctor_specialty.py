from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from doctors_service.models import DoctorSpecialty

DOCTOR_SPECIALTY_URL = reverse("doctors_service:specialties-list")
DOCTOR_SPECIALTY_DETAIL_URL = reverse(
    "doctors_service:specialties-detail",
    kwargs={"pk": 1}
)


class PublicDoctorSpecialtyTest(TestCase):

    def setUp(self):
        self.specialty1 = DoctorSpecialty.objects.create(
            specialty="Cardiology"
        )
        self.specialty2 = DoctorSpecialty.objects.create(
            specialty="Dermatology"
        )

    def test_specialty_list_login_not_required(self):
        response = self.client.get(DOCTOR_SPECIALTY_URL)
        self.assertEqual(response.status_code, 200)

    def test_specialty_detail_list_login_not_required(self):
        response = self.client.get(DOCTOR_SPECIALTY_DETAIL_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_list_with_specialty(self):
        response = self.client.get(DOCTOR_SPECIALTY_URL)
        self.assertEqual(response.status_code, 200)
        specialties = DoctorSpecialty.objects.all()
        self.assertEqual(
            list(response.context["specialties_list"]),
            list(specialties)
        )
        self.assertTemplateUsed(response, "doctors/specialties_list.html")

    def test_test_retrieve_list_with_specialty_detail(self):
        doctor = get_user_model().objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
            password="<PASSWORD>",
            username="test_username",
            licence_number="TES12345",
            city="test_city",
            hospital="test_hospital",
        )
        doctor.specialty.add(self.specialty1, self.specialty2)
        doctor.save()
        response = self.client.get(
            DOCTOR_SPECIALTY_DETAIL_URL,
            {"pk": doctor.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["specialty"],
            doctor.specialty.first()
        )
