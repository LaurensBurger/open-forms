# Generated by Django 4.2.11 on 2024-07-04 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("kvk", "0001_initial"),
        ("kvk", "0002_remove_kvkconfig_use_operation"),
        ("kvk", "0003_auto_20211217_1234"),
        ("kvk", "0004_auto_20220203_1709"),
        ("kvk", "0005_normalize_kvk_service_config"),
        ("kvk", "0006_remove_refactored_service_config_fields"),
        ("kvk", "0007_kvkconfig_profile_service_kvkconfig_search_service"),
        ("kvk", "0008_remove_kvkconfig_service"),
    ]

    dependencies = [
        ("zgw_consumers", "0012_auto_20210104_1039"),
    ]

    operations = [
        migrations.CreateModel(
            name="KVKConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profile_service",
                    models.OneToOneField(
                        help_text="Service for API used to retrieve basis profielen.",
                        limit_choices_to={"api_type": "orc"},
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="zgw_consumers.service",
                        verbose_name="KvK API Basisprofiel",
                    ),
                ),
                (
                    "search_service",
                    models.OneToOneField(
                        help_text="Service for API used for validation of KvK, RSIN and vestigingsnummer's.",
                        limit_choices_to={"api_type": "orc"},
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="zgw_consumers.service",
                        verbose_name="KvK API Zoeken",
                    ),
                ),
            ],
            options={
                "verbose_name": "KvK configuration",
            },
        ),
    ]