# Generated by Django 4.2.16 on 2024-12-02 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0012_alter_submission_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="submission",
            name="previous_submission",
        ),
    ]