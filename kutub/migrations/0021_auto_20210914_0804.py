# Generated by Django 3.2.7 on 2021-09-14 08:04

from django.db import migrations
import kutub.fields
import partial_date.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kutub', '0020_contentitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='manuscript',
            name='origin',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='Any descriptive or other information concerning the origin of a manuscript.'),
        ),
        migrations.AddField(
            model_name='manuscript',
            name='origin_date_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='Any form of date, used to identify the date of origin for a manuscript, manuscript part, or other object.'),
        ),
        migrations.AddField(
            model_name='manuscript',
            name='origin_date_earliest',
            field=partial_date.fields.PartialDateField(blank=True, default=None, help_text='The earliest possible date for the origin of the manuscript.', null=True),
        ),
        migrations.AddField(
            model_name='manuscript',
            name='origin_date_latest',
            field=partial_date.fields.PartialDateField(blank=True, default=None, help_text='The latest possible date for the origin of the manuscript.', null=True),
        ),
        migrations.AddField(
            model_name='manuscript',
            name='origin_place',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='Any form of place name, used to identify the place of origin for a manuscript.'),
        ),
    ]