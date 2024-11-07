# Generated by Django 5.1.1 on 2024-11-06 09:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("benedict_school", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="About",
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
                ("description", models.TextField()),
                ("anthem", models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name="parent",
            name="id_number",
        ),
        migrations.RemoveField(
            model_name="parent",
            name="password",
        ),
        migrations.RemoveField(
            model_name="parent",
            name="username",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="last_name",
        ),
        migrations.AddField(
            model_name="parent",
            name="first_name",
            field=models.CharField(default="Unknown", max_length=50),
        ),
        migrations.AddField(
            model_name="parent",
            name="last_name",
            field=models.CharField(default="Unknown", max_length=50),
        ),
        migrations.AddField(
            model_name="staff",
            name="class_name",
            field=models.CharField(default="Primary One", max_length=50),
        ),
        migrations.AddField(
            model_name="staff",
            name="teacher_name",
            field=models.CharField(default="Unknown", max_length=100),
        ),
        migrations.AlterField(
            model_name="parent",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="parent_images/"),
        ),
        migrations.AlterField(
            model_name="staff",
            name="subjects_handled",
            field=models.CharField(
                choices=[
                    ("math", "Mathematics"),
                    ("science", "Science"),
                    ("english", "English"),
                    ("social_studies", "Social Studies"),
                    ("literacy_1A", "Literacy 1A"),
                    ("literacy_1B", "Literacy 1B"),
                    ("literacy", "Literacy"),
                    ("luganda", "Luganda"),
                    ("reading", "Reading"),
                    ("religious_education", "Religious Education"),
                    ("learning_area_1_5", "Learning Area 1-5"),
                ],
                default="math",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="parent",
            name="ID_number",
            field=models.CharField(
                default="AA0000000A00AA", max_length=14, unique=True
            ),
        ),
    ]