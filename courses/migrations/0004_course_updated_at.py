# Generated by Django 5.1.4 on 2025-01-29 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0003_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
