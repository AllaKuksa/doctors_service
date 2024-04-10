from django.db import models


class DoctorSpecialty(models.Model):
    specialty = models.CharField(max_length=255)

    class Meta:
        ordering = ("specialty",)

    def __str__(self):
        return self.specialty

