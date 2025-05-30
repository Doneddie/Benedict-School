# Generated by Django 5.1.1 on 2025-01-10 18:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("benedict_school", "0014_alter_subject_options_remove_staff_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="child",
            name="alumni_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="reason_for_leaving",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="child",
            name="status",
            field=models.CharField(
                choices=[("active", "Active"), ("alumni", "Alumni")],
                default="active",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="parent",
            name="alumni_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="parent",
            name="reason_for_leaving",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="parent",
            name="status",
            field=models.CharField(
                choices=[("active", "Active"), ("alumni", "Alumni")],
                default="active",
                max_length=20,
            ),
        ),
    ]
