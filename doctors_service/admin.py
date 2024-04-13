from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from doctors_service.models import Doctor, DoctorSpecialty, DoctorSchedule, Appointment


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "licence_number", "city", "hospital",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": (
            "licence_number",
            "city",
            "hospital",
        )}
          ),
         )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "licence_number",
                        "city",
                        "hospital",
                        "email",
                    )
                },
            ),
        )
    )


@admin.register(DoctorSpecialty)
class DoctorSpecialtyAdmin(admin.ModelAdmin):
    search_fields = ("specialty",)


admin.site.register(DoctorSchedule)
admin.site.register(Appointment)
