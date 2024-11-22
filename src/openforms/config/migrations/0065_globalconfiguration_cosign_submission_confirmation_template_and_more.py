# Generated by Django 4.2.16 on 2024-11-15 10:26

import functools

from django.conf import settings
from django.db import migrations, models
from django.db.migrations.state import StateApps
from django.utils import translation
from django.utils.translation import gettext

import tinymce.models

import openforms.config.models.config
import openforms.template.validators
import openforms.utils.translations


def update_translated_defaults(apps: StateApps, _):
    """
    Set the properly translated default config field values.

    Workaround for https://github.com/open-formulieren/open-forms/issues/4826
    """
    GlobalConfiguration = apps.get_model("config", "GlobalConfiguration")
    config = GlobalConfiguration.objects.first()
    if config is None:
        return

    for field in (
        "cosign_submission_confirmation_template",
        "cosign_submission_confirmation_title",
        "submission_confirmation_title",
    ):
        for lang, _ in settings.LANGUAGES:
            with translation.override(lang):
                default_callback = config._meta.get_field(field).default
                assert isinstance(default_callback, functools.partial)
                if default_callback.func is openforms.utils.translations.get_default:
                    default_callback = functools.partial(
                        gettext, *default_callback.args
                    )
                setattr(config, f"{field}_{lang}", default_callback())
    config.save()


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0064_alter_globalconfiguration_submissions_removal_limit"),
    ]

    operations = [
        migrations.AddField(
            model_name="globalconfiguration",
            name="cosign_submission_confirmation_template",
            field=tinymce.models.HTMLField(
                default=functools.partial(
                    openforms.config.models.config._render,
                    *("config/default_cosign_submission_confirmation.html",),
                    **{},
                ),
                help_text="The content of the submission confirmation page for submissions requiring cosigning. The variables 'public_reference' and 'cosigner_email' are available. We strongly advise you to include the 'public_reference' in case users need to contact the customer service.",
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="cosign submission confirmation template",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="cosign_submission_confirmation_template_en",
            field=tinymce.models.HTMLField(
                default=functools.partial(
                    openforms.config.models.config._render,
                    *("config/default_cosign_submission_confirmation.html",),
                    **{},
                ),
                help_text="The content of the submission confirmation page for submissions requiring cosigning. The variables 'public_reference' and 'cosigner_email' are available. We strongly advise you to include the 'public_reference' in case users need to contact the customer service.",
                null=True,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="cosign submission confirmation template",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="cosign_submission_confirmation_template_nl",
            field=tinymce.models.HTMLField(
                default=functools.partial(
                    openforms.config.models.config._render,
                    *("config/default_cosign_submission_confirmation.html",),
                    **{},
                ),
                help_text="The content of the submission confirmation page for submissions requiring cosigning. The variables 'public_reference' and 'cosigner_email' are available. We strongly advise you to include the 'public_reference' in case users need to contact the customer service.",
                null=True,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="cosign submission confirmation template",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="cosign_submission_confirmation_title",
            field=models.CharField(
                default=functools.partial(
                    openforms.utils.translations.get_default,
                    *("Request not complete yet",),
                    **{},
                ),
                help_text="The content of the confirmation page title for submissions requiring cosigning.",
                max_length=200,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="cosign submission confirmation title",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="cosign_submission_confirmation_title_en",
            field=models.CharField(
                default=functools.partial(
                    openforms.utils.translations.get_default,
                    *("Request not complete yet",),
                    **{},
                ),
                help_text="The content of the confirmation page title for submissions requiring cosigning.",
                max_length=200,
                null=True,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="cosign submission confirmation title",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="cosign_submission_confirmation_title_nl",
            field=models.CharField(
                default=functools.partial(
                    openforms.utils.translations.get_default,
                    *("Request not complete yet",),
                    **{},
                ),
                help_text="The content of the confirmation page title for submissions requiring cosigning.",
                max_length=200,
                null=True,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="cosign submission confirmation title",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="submission_confirmation_title",
            field=models.CharField(
                default=functools.partial(
                    openforms.utils.translations.get_default,
                    *("Confirmation: {{ public_reference }}",),
                    **{},
                ),
                help_text="The content of the confirmation page title. You can (and should) use the 'public_reference' variable so the users have a reference in case they need to contact the customer service.",
                max_length=200,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="submission confirmation title",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="submission_confirmation_title_en",
            field=models.CharField(
                default=functools.partial(
                    openforms.utils.translations.get_default,
                    *("Confirmation: {{ public_reference }}",),
                    **{},
                ),
                help_text="The content of the confirmation page title. You can (and should) use the 'public_reference' variable so the users have a reference in case they need to contact the customer service.",
                max_length=200,
                null=True,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="submission confirmation title",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="submission_confirmation_title_nl",
            field=models.CharField(
                default=functools.partial(
                    openforms.utils.translations.get_default,
                    *("Confirmation: {{ public_reference }}",),
                    **{},
                ),
                help_text="The content of the confirmation page title. You can (and should) use the 'public_reference' variable so the users have a reference in case they need to contact the customer service.",
                max_length=200,
                null=True,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="submission confirmation title",
            ),
        ),
        migrations.RunPython(update_translated_defaults, migrations.RunPython.noop),
    ]
