# Generated by Django 4.1.9 on 2023-07-04 11:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_webhook_receiver", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="webhookreceiver",
            name="hash_algorithm",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
