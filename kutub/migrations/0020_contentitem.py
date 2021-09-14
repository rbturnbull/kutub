# Generated by Django 3.2.7 on 2021-09-14 07:28

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import kutub.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kutub', '0019_auto_20210914_0631'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('locus_description', kutub.fields.DescriptionField(blank=True, default='', help_text='A description identify any reference to one or more folios within a manuscript. If it is empty, it will be filled out by the fields to determin the start and end folios.')),
                ('start_folio', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('start_folio_side', models.CharField(choices=[('', 'Unknown'), ('r', 'Recto'), ('v', 'Verso')], default='', max_length=1)),
                ('end_folio', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('end_folio_side', models.CharField(blank=True, choices=[('', 'Unknown'), ('r', 'Recto'), ('v', 'Verso')], default='', max_length=1)),
                ('defective', models.BooleanField(blank=True, default=None, help_text='Whether the content item is incomplete through loss or damage.', null=True)),
                ('author', kutub.fields.DescriptionField(blank=True, default='', help_text="The normalized form of an author's name, irrespective of how this form of the name is cited in the manuscript.")),
                ('responsibility_statement', kutub.fields.DescriptionField(blank=True, default='', help_text='A statement of responsibility for the intellectual content of a content item, where the author field does not suffice.')),
                ('title', kutub.fields.DescriptionField(blank=True, default='', help_text="A regularized form of the item's title, as distinct from any rubric quoted from the manuscript.")),
                ('rubric', kutub.fields.DescriptionField(blank=True, default='', help_text='the text of any rubric or heading attached to a particular content item.')),
                ('incipit', kutub.fields.DescriptionField(blank=True, default='', help_text='the text of any rubric or heading attached to a particular content item.')),
                ('quote', kutub.fields.DescriptionField(blank=True, default='', help_text='A phrase or passage attributed by the narrator or author to some agency external to the text.')),
                ('explicit', kutub.fields.DescriptionField(blank=True, default='', help_text='The explicit of the item, that is, the closing words of the text proper, exclusive of any rubric or colophon which might follow it.')),
                ('final_rubric', kutub.fields.DescriptionField(blank=True, default='', help_text='the string of words that denotes the end of a text division, often with an assertion as to its author and title.')),
                ('colophon', kutub.fields.DescriptionField(blank=True, default='', help_text='The colophon of an item: that is, a statement providing information regarding the date, place, agency, or reason for production of the manuscript.')),
                ('deco_note', kutub.fields.DescriptionField(blank=True, default='', help_text='A note describing either a decorative component of a manuscript.')),
                ('filiation', kutub.fields.DescriptionField(blank=True, default='', help_text="Information concerning the manuscript or other object's filiation, i.e. its relationship to other surviving manuscripts.")),
                ('note', kutub.fields.DescriptionField(blank=True, default='', help_text='A note or annotation.')),
                ('manuscript', models.ForeignKey(help_text='The manuscript in which this item is found.', on_delete=django.db.models.deletion.CASCADE, to='kutub.manuscript')),
            ],
            options={
                'ordering': ['manuscript', 'start_folio', 'end_folio_side', 'end_folio', 'end_folio_side', 'author', 'title'],
            },
        ),
    ]
