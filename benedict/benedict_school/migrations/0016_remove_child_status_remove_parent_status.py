# Generated by Django 5.1.1 on 2025-01-10 18:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("benedict_school", "0015_child_alumni_date_child_reason_for_leaving_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="child",
            name="status",
        ),
        migrations.RemoveField(
            model_name="parent",
            name="status",
        ),
    ]