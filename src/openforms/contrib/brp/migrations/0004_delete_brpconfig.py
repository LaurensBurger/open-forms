# Generated by Django 3.2.21 on 2023-09-23 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("brp", "0003_copy_config_to_haalcentraal"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BRPConfig",
        ),
    ]