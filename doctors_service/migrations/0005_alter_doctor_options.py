# Generated by Django 4.2.11 on 2024-04-30 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("doctors_service", "0004_doctorschedule_is_booked_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="doctor",
            options={"ordering": ("first_name", "last_name")},
        ),
    ]
