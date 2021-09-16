# Generated by Django 3.2.7 on 2021-09-15 22:08

import django.core.validators
from django.db import migrations
import kutub.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kutub', '0025_auto_20210915_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentitem',
            name='author',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text="The normalized form of an author's name, irrespective of how this form of the name is cited in the manuscript.", validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='colophon',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='The colophon of an item: that is, a statement providing information regarding the date, place, agency, or reason for production of the manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='deco_note',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A note describing either a decorative component of a manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='explicit',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='The explicit of the item, that is, the closing words of the text proper, exclusive of any rubric or colophon which might follow it.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='filiation',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text="Information concerning the manuscript or other object's filiation, i.e. its relationship to other surviving manuscripts.", validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='final_rubric',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='the string of words that denotes the end of a text division, often with an assertion as to its author and title.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='incipit',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='the text of any rubric or heading attached to a particular content item.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='locus_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description identify any reference to one or more folios within a manuscript. If it is empty, it will be filled out by the fields to determin the start and end folios.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='note',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A note or annotation.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='quote',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A phrase or passage attributed by the narrator or author to some agency external to the text.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='responsibility_statement',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A statement of responsibility for the intellectual content of a content item, where the author field does not suffice.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='rubric',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='the text of any rubric or heading attached to a particular content item.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='contentitem',
            name='title',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text="A regularized form of the item's title, as distinct from any rubric quoted from the manuscript.", validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='acquisition',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='Any descriptive or other information concerning the process by which the manuscript entered the holding institution.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='binding_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the state of the present and former bindings of a manuscript, including information about its material, any distinctive marks, and provenance information.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='catchwords',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='The system used to ensure correct ordering of the quires or similar making up a codex, typically by means of annotations at the foot of the page.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='collation',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the arrangement of the leaves and quires of the manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='condition',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A summary of the overall physical state of a manuscript, in particular where such information is not recorded elsewhere in the description.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='content_summary',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A summary of the intellectual content in this manuscript. More details can be added below.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='decoration_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the decoration of the manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='dimensions_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the dimensions of the leaves which can be used if the basic height and width values are not sufficient.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='extent_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the number of leaves in the manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='foliation',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='The scheme, medium or location of folio, page, column, or line numbers written in the manuscript, frequently including a statement about when and, if known, by whom, the numbering was done.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='hand_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of all the different hands used in the manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='heading',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A brief description of the manuscript (for example, the title).', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='layout',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='How how text is laid out on the page or surface of the manuscript, including information about any ruling, pricking, or other evidence of page-preparation techniques.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='music_notation',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the type of musical notation.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='origin',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='Any descriptive or other information concerning the origin of a manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='origin_date_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='Any form of date, used to identify the date of origin for a manuscript, manuscript part, or other object.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='origin_place',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='Any form of place name, used to identify the place of origin for a manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='provenance',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='Any description or other information concerning a single identifiable episode during the history of a manuscript, manuscript part, or other object after its creation but before its acquisition. Separated by one or more line breaks.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='seal_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='information about the seal(s) attached to documents to guarantee their integrity, or to show authentication of the issuer or consent of the participants.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='signatures',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the leaf or quire signatures found within a codex.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
        migrations.AlterField(
            model_name='manuscript',
            name='support_description',
            field=kutub.fields.DescriptionField(blank=True, default='', help_text='A description of the physical support for the written part of a manuscript.', validators=[django.core.validators.RegexValidator('^[ -\ud7ff\t\n\r\ue000-�𐀀-\U0010ffff]*$', 'Only valid XML characters allowed.')]),
        ),
    ]