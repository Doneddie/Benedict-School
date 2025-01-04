# Generated by Django 4.2.17 on 2025-01-04 16:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("benedict_school", "0008_subject_staff_department_staff_role_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="child",
            name="application_status",
        ),
        migrations.AddField(
            model_name="child",
            name="sex",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female")],
                default="male",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="staff",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="staff_photos/"),
        ),
        migrations.AddField(
            model_name="staff",
            name="sex",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female")],
                default="male",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="staff",
            name="name",
            field=models.CharField(max_length=50),
        ),
    ]
