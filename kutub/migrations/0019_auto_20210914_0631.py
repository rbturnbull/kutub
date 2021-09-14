# Generated by Django 3.2.7 on 2021-09-14 06:31

from django.db import migrations
import kutub.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kutub', '0018_auto_20210912_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='manuscript',
            name='heading',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A brief description of the manuscript (for example, the title).'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='binding_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the state of the present and former bindings of a manuscript, including information about its material, any distinctive marks, and provenance information.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='catchwords',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='The system used to ensure correct ordering of the quires or similar making up a codex, typically by means of annotations at the foot of the page.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='collation',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the arrangement of the leaves and quires of the manuscript.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='condition',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A summary of the overall physical state of a manuscript, in particular where such information is not recorded elsewhere in the description.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='content_summary',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A summary of the intellectual content in this manuscript. More details can be added below.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='decoration_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the decoration of the manuscript.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='dimensions_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the dimensions of the leaves which can be used if the basic height and width values are not sufficient.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='extent_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the number of leaves in the manuscript.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='foliation',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='The scheme, medium or location of folio, page, column, or line numbers written in the manuscript, frequently including a statement about when and, if known, by whom, the numbering was done.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='hand_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of all the different hands used in the manuscript.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='layout',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='How how text is laid out on the page or surface of the manuscript, including information about any ruling, pricking, or other evidence of page-preparation techniques.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='music_notation',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the type of musical notation.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='seal_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='information about the seal(s) attached to documents to guarantee their integrity, or to show authentication of the issuer or consent of the participants.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='signatures',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the leaf or quire signatures found within a codex.'),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='support_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the physical support for the written part of a manuscript.'),
        ),
    ]