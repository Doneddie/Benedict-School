# Generated by Django 5.1.1 on 2024-12-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("benedict_school", "0007_remove_about_description_about_title_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
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
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="staff",
            name="department",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="staff",
            name="role",
            field=models.CharField(
                choices=[
                    ("teacher", "Teacher"),
                    ("director", "Director"),
                    ("cleaner", "Cleaner"),
                    ("cook", "Cook"),
                    ("admin", "Admin Staff"),
                    ("other", "Other"),
                ],
                default="teacher",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="staff",
            name="work_schedule",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="staff",
            name="class_name",
            field=models.CharField(
                blank=True, default="Primary One", max_length=50, null=True
            ),
        ),
        migrations.RemoveField(
            model_name="staff",
            name="subjects_handled",
        ),
        migrations.AlterField(
            model_name="staff",
            name="tel_no",
            field=models.CharField(default="", max_length=22),
        ),
        migrations.AlterField(
            model_name="staff",
            name="years_of_experience",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="staff",
            name="subjects_handled",
            field=models.ManyToManyField(blank=True, to="benedict_school.subject"),
        ),
    ]