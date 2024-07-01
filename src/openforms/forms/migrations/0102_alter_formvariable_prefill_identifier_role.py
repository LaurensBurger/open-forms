# Generated by Django 4.2.11 on 2024-07-02 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0101_objecttype_url_to_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formvariable",
            name="prefill_identifier_role",
            field=models.CharField(
                choices=[("main", "Main"), ("authorised_person", "Authorizee")],
                default="main",
                help_text="In case that multiple identifiers are returned (in the case of eHerkenning bewindvoering and DigiD Machtigen), should the prefill data related to the main identifier be used, or that related to the authorised person?",
                max_length=100,
                verbose_name="prefill identifier role",
            ),
        ),
    ]
