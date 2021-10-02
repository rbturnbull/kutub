# Generated by Django 3.2.7 on 2021-10-02 00:04

import django.core.validators
from django.db import migrations, models
import kutub.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kutub', '0034_manuscript_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ('description', 'language_subtag', 'extlang', 'script', 'region')},
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='iiif_manifest_url',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A URL to a IIIF manifest with facsimiles of this manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')], verbose_name='IIIF Manifest URL'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='other_languages',
            field=models.ManyToManyField(blank=True, help_text='Other languages used.', related_name='other_language_set', to='kutub.Language'),
        ),
    ]