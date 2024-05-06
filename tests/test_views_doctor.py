from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from doctors_service.models import DoctorSpecialty
from doctors_service.forms import DoctorUpdateForm


DOCTORS_LIST = reverse("doctors_service:doctors-list")
DOCTOR_DETAIL = reverse("doctors_service:doctors-detail", kwargs={"pk": 1})


class PublicDoctorTest(TestCase):

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

    def test_doctors_list_login_not_required(self):
        response = self.client.get(DOCTORS_LIST)
        self.assertEqual(response.status_code, 200)

    def test_doctors_list_pagination(self):
        response = self.client.get(DOCTORS_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)

    def test_doctor_detail_view_login_not_required(self):
        response = self.client.get(DOCTOR_DETAIL, {"pk": self.doctor.pk})
        self.assertEqual(response.status_code, 200)

    def test_retrieve_list_with_doctors(self):
        response = self.client.get(DOCTORS_LIST)
        self.assertEqual(response.status_code, 200)
        doctors = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["doctors_list"]),
            list(doctors)
        )

    def test_create_doctor(self):
        form_data = {
            "username": "test_user_test",
            "first_name": "Test",
            "last_name": "Test",
            "hospital": "Test hospital",
            "city": "Test city",
            "email": "test123@test.com",
            "specialty": [self.specialty1.pk, self.specialty2.pk],
            "licence_number": "TTT12345",
            "password1": "<PASSWORD>123",
            "password2": "<PASSWORD>123",
        }

        response = self.client.post(
            reverse("doctors_service:doctor-form"),
            data=form_data
        )
        new_user = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.licence_number, form_data["licence_number"])
        self.assertListEqual(
            list(new_user.specialty.values_list("pk", flat=True)),
            form_data["specialty"]
        )
        self.assertRedirects(response, "/doctors/")

    def test_query_search_filter_by_city_of_doctor(self):
        response = self.client.get("/doctors/", {"city": "tes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["object_list"]), [self.doctor])

    def test_search_with_empty_query(self):
        response = self.client.get("/doctors/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["object_list"]),
            get_user_model().objects.count()
        )


class PrivateDoctorTest(TestCase):

    def setUp(self):
        self.specialty1 = DoctorSpecialty.objects.create(
            specialty="Endocrinology"
        )
        self.specialty2 = DoctorSpecialty.objects.create(
            specialty="Gastroenterology"
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

    def test_update_doctor_info(self):
        new_licence_number = "TES12349"
        form_data = {
            "licence_number": new_licence_number,
            "city": self.doctor.city,
            "hospital": self.doctor.hospital,
            "specialty": [self.specialty1.pk, self.specialty2.pk],
        }
        form = DoctorUpdateForm(data=form_data, instance=self.doctor)
        self.assertTrue(form.is_valid())
        response = self.client.post(
            reverse(
                "doctors_service:doctor-update",
                kwargs={"pk": self.doctor.pk}
            ),
            data=form_data,
        )
        self.assertEqual(response.status_code, 302)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.licence_number, new_licence_number)
        self.assertRedirects(
            response,
            reverse(
                "doctors_service:doctors-detail",
                kwargs={"pk": self.doctor.pk}
            )
        )

    def test_delete_doctor(self):
        response = self.client.get(
            reverse("doctors_service:doctor-delete",
                    kwargs={"pk": self.doctor.pk}),
            follow=True
        )
        self.assertContains(
            response, "Are you sure that you want to delete the Doctor"
        )
        self.client.post(
            reverse(
                "doctors_service:doctor-delete",
                kwargs={"pk": self.doctor.pk}),
            follow=True
        )
        self.assertRaises(
            ObjectDoesNotExist,
            get_user_model().objects.get,
            id=self.doctor.id
        )
