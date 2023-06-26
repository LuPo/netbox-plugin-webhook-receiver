# Generated by Django 4.1.9 on 2023-06-26 09:16

from django.db import migrations, models
import taggit.managers
import utilities.json
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("extras", "0092_delete_jobresult"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebhookMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("received_at", models.DateTimeField()),
                ("payload", models.JSONField(default=None, null=True)),
            ],
            options={
                "ordering": ["received_at"],
            },
        ),
        migrations.CreateModel(
            name="WebhookReceiver",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("webhook_origin", models.CharField(max_length=30)),
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                ("token", models.CharField(max_length=50)),
                (
                    "token_name",
                    models.CharField(default="X-Gitlab-Token", max_length=50),
                ),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "ordering": ("name", "webhook_origin"),
            },
        ),
        migrations.AddIndex(
            model_name="webhookmessage",
            index=models.Index(
                fields=["received_at"], name="netbox_webh_receive_6a2187_idx"
            ),
        ),
    ]
