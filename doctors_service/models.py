from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


from doctors_patients_service import settings


class DoctorSpecialty(models.Model):
    specialty = models.CharField(max_length=255)

    class Meta:
        ordering = ("specialty",)

    def __str__(self):
        return self.specialty


class Doctor(AbstractUser):
    licence_number = models.CharField(max_length=8, unique=True)
    city = models.CharField(max_length=255, blank=False)
    hospital = models.CharField(max_length=255, blank=False)
    specialty = models.ManyToManyField(
        DoctorSpecialty,
        related_name="doctors"
    )

    class Meta:
        ordering = ("city", "hospital",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DoctorSchedule(models.Model):

    TIMESLOT_LIST = (
        (0, "09:00 – 10:00"),
        (1, "10:00 – 11:00"),
        (2, "11:00 – 12:00"),
        (3, "12:00 – 13:00"),
        (4, "14:00 – 15:00"),
        (5, "15:00 – 16:00"),
        (6, "16:00 – 17:00"),
        (7, "17:00 – 18:00"),
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_schedule",
    )
    date = models.DateField(help_text="YYYY-MM-DD")
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)

    class Meta:
        unique_together = ("doctor", "date", "timeslot", )
        ordering = ("date", "timeslot",)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]

    def __str__(self):
        return f"{self.date} / {self.time}"


class Appointment(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    doctor_schedule = models.ForeignKey(
        DoctorSchedule,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = PhoneNumberField()
    insurance_number = models.IntegerField(max_length=10, unique=True, blank=False)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("doctor_schedule",)

    def __str__(self):
        return f"patient {self.first_name} {self.last_name} has a visit - {self.doctor_schedule}"


