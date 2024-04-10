from django.contrib.auth.models import AbstractUser
from django.db import models


class DoctorSpecialty(models.Model):
    specialty = models.CharField(max_length=255)

    class Meta:
        ordering = ("specialty",)

    def __str__(self):
        return self.specialty


class Doctor(AbstractUser):
    licence_number = models.IntegerField(max_length=8, unique=True, blank=False)
    city = models.CharField(max_length=255)
    hospital = models.CharField(max_length=255)
    specialty = models.ManyToManyField(
        DoctorSpecialty,
        on_delete=models.CASCADE,
        related_name="doctors"
    )

    class Meta:
        ordering = ("hospital", "city",)

    def __str__(self):
        return (f"{self.first_name} {self.last_name} "
                f"with specialty {self.specialty}  - "
                f"city {self.city} in {self.hospital}")


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
        Doctor,
        on_delete=models.CASCADE,
        related_name="doctor_schedule",
    )
    date = models.DateField(help_text="YYYY-MM-DD")
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)

    class Meta:
        unique_together = ("doctor", "date", "timeslot", )
