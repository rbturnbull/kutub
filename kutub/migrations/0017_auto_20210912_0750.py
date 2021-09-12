# Generated by Django 3.2.7 on 2021-09-12 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kutub', '0016_manuscript_support_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manuscript',
            name='binding_description',
            field=models.CharField(blank=True, default='', help_text='A description of the state of the present and former bindings of a manuscript, including information about its material, any distinctive marks, and provenance information.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='catchwords',
            field=models.CharField(blank=True, default='', help_text='The system used to ensure correct ordering of the quires or similar making up a codex, typically by means of annotations at the foot of the page.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='collation',
            field=models.CharField(blank=True, default='', help_text='A description of the arrangement of the leaves and quires of the manuscript.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='condition',
            field=models.CharField(blank=True, default='', help_text='A summary of the overall physical state of a manuscript, in particular where such information is not recorded elsewhere in the description.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='content_summary',
            field=models.CharField(blank=True, default='', help_text='A summary of the intellectual content in this manuscript. More details can be added below.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='decoration_description',
            field=models.CharField(blank=True, default='', help_text='A description of the decoration of the manuscript.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='dimensions_description',
            field=models.CharField(blank=True, default='', help_text='A description of the dimensions of the leaves which can be used if the basic height and width values are not sufficient.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='extent_description',
            field=models.CharField(blank=True, default='', help_text='A description of the number of leaves in the manuscript.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='foliation',
            field=models.CharField(blank=True, default='', help_text='The scheme, medium or location of folio, page, column, or line numbers written in the manuscript, frequently including a statement about when and, if known, by whom, the numbering was done.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='hand_description',
            field=models.CharField(blank=True, default='', help_text='A description of all the different hands used in the manuscript.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='layout',
            field=models.CharField(blank=True, default='', help_text='How how text is laid out on the page or surface of the manuscript, including information about any ruling, pricking, or other evidence of page-preparation techniques.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='music_notation',
            field=models.CharField(blank=True, default='', help_text='A description of the type of musical notation.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='seal_description',
            field=models.CharField(blank=True, default='', help_text='information about the seal(s) attached to documents to guarantee their integrity, or to show authentication of the issuer or consent of the participants.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='signatures',
            field=models.CharField(blank=True, default='', help_text='A description of the leaf or quire signatures found within a codex.', max_length=2047),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='support_description',
            field=models.CharField(blank=True, default='', help_text='A description of the physical support for the written part of a manuscript.', max_length=2047),
        ),
    ]
