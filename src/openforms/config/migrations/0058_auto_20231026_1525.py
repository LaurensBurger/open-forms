# Generated by Django 3.2.21 on 2023-10-26 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("config", "0057_globalconfiguration_recipients_email_digest"),
    ]

    operations = [
        migrations.AddField(
            model_name="cspsetting",
            name="content_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="contenttypes.contenttype",
                verbose_name="content type",
            ),
        ),
        migrations.AddField(
            model_name="cspsetting",
            name="object_id",
            field=models.TextField(blank=True, db_index=True, verbose_name="object id"),
        ),
        migrations.AlterField(
            model_name="cspsetting",
            name="value",
            field=models.CharField(
                help_text="CSP header value", max_length=255, verbose_name="value"
            ),
        ),
    ]