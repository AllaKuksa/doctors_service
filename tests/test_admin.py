from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

        self.doctor = get_user_model().objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
            password="<PASSWORD>",
            username="test_username",
            licence_number="TES12345",
            city="test_city",
            hospital="test_hospital",
        )

    def test_doctor_additional_information_listed(self):
        url = reverse(
            "admin:doctors_service_doctor_change",
            args=[self.doctor.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.doctor.licence_number)
        self.assertContains(response, self.doctor.city)
        self.assertContains(response, self.doctor.hospital)
