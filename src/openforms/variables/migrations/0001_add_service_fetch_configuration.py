# Generated by Django 3.2.16 on 2022-11-24 08:15

from django.db import migrations, models
import django.db.models.deletion
import openforms.variables.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("zgw_consumers", "0016_auto_20220818_1412"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServiceFetchConfiguration",
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
                (
                    "path",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="path relative to the Service API root",
                        max_length=250,
                        verbose_name="path",
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        choices=[("GET", "GET"), ("POST", "POST")],
                        default="GET",
                        help_text="POST is allowed, but should not be used to mutate data",
                        max_length=4,
                        verbose_name="HTTP method",
                    ),
                ),
                (
                    "headers",
                    models.JSONField(
                        blank=True,
                        help_text="Additions and overrides for the HTTP request headers as defined in the Service.",
                        null=True,
                        validators=[openforms.variables.validators.HeaderValidator()],
                        verbose_name="HTTP request headers",
                    ),
                ),
                (
                    "query_params",
                    models.TextField(
                        blank=True, default="", verbose_name="HTTP query string"
                    ),
                ),
                (
                    "body",
                    models.JSONField(
                        blank=True,
                        help_text='Request body for POST requests (only "application/json" is supported)',
                        null=True,
                        verbose_name="HTTP request body",
                    ),
                ),
                (
                    "data_mapping_type",
                    models.CharField(
                        blank=True,
                        choices=[("JsonLogic", "JsonLogic"), ("jq", "jq")],
                        max_length=10,
                        null=True,
                        verbose_name="mapping expression language",
                    ),
                ),
                (
                    "mapping_expression",
                    models.JSONField(
                        blank=True,
                        help_text="For jq, pass a string containing the filter expression",
                        null=True,
                        verbose_name="mapping expression",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="zgw_consumers.service",
                    ),
                ),
            ],
            options={
                "verbose_name": "service fetch configuration",
                "verbose_name_plural": "service fetch configurations",
            },
        ),
    ]
