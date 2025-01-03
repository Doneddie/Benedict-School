# Generated by Django 5.1.1 on 2024-11-03 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Child",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("date_of_birth", models.DateField()),
                (
                    "profile_image",
                    models.ImageField(blank=True, null=True, upload_to="child_images/"),
                ),
                (
                    "application_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                            ("left", "Left"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("date", models.DateTimeField()),
                ("location", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="event_images/"),
                ),
                (
                    "video",
                    models.FileField(blank=True, null=True, upload_to="event_videos/"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Parent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=50, unique=True)),
                ("password", models.CharField(max_length=128)),
                ("id_number", models.CharField(max_length=50, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("address", models.CharField(max_length=100)),
                (
                    "profile_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_images/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=50, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                (
                    "subjects_handled",
                    models.CharField(
                        choices=[
                            ("math", "Mathematics"),
                            ("science", "Science"),
                            ("english", "English"),
                            ("history", "History"),
                            ("geography", "Geography"),
                            ("art", "Art"),
                            ("music", "Music"),
                            ("physical_education", "Physical Education"),
                            ("computing", "Computing"),
                        ],
                        default="math",
                        max_length=100,
                    ),
                ),
                ("years_of_experience", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Exit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("exit_date", models.DateField()),
                ("reason", models.TextField(blank=True, null=True)),
                (
                    "child",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="benedict_school.child",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="child",
            name="parent",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="benedict_school.parent",
            ),
        ),
        migrations.CreateModel(
            name="PupilApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("application_date", models.DateField(auto_now_add=True)),
                (
                    "documents",
                    models.FileField(blank=True, null=True, upload_to="applications/"),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "child",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="benedict_school.child",
                    ),
                ),
            ],
        ),
    ]
