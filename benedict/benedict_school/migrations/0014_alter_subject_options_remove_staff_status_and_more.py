# Generated by Django 5.1.1 on 2025-01-09 20:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("benedict_school", "0013_alter_staff_employee_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subject",
            options={
                "ordering": ["name"],
                "verbose_name": "Subject",
                "verbose_name_plural": "Subjects",
            },
        ),
        migrations.RemoveField(
            model_name="staff",
            name="status",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="work_schedule",
        ),
        migrations.AlterField(
            model_name="staff",
            name="address",
            field=models.TextField(
                default="", help_text="Physical address of residence"
            ),
        ),
        migrations.AlterField(
            model_name="staff",
            name="department",
            field=models.CharField(
                blank=True,
                choices=[
                    ("administration", "Administration"),
                    ("kitchen", "Kitchen"),
                    ("security", "Security"),
                    ("medical", "Medical"),
                    ("library", "Library"),
                    ("other", "Other"),
                ],
                help_text="Department for non-teaching staff",
                max_length=100,
                null=True,
            ),
        ),
    ]