# Generated by Django 4.1.9 on 2023-06-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_webhook_receiver", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="webhookreceiver",
            name="store_payload",
            field=models.BooleanField(default=True),
        ),
    ]
