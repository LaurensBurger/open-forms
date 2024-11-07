# Generated by Django 4.2.14 on 2024-08-05 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial_to_v270"),
    ]

    operations = [
        migrations.AddField(
            model_name="submissionpayment",
            name="provider_payment_id",
            field=models.CharField(
                blank=True,
                help_text="The ID assigned to the payment by the payment provider.",
                max_length=128,
                verbose_name="provider payment ID",
            ),
        ),
    ]