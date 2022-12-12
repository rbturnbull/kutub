from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from django.forms.models import inlineformset_factory
from django_superform.forms import SuperModelFormMixin
from django_superform import InlineFormSetField

from language_tags import data as language_data
registry = language_data.get('registry')

from django_select2 import forms as s2forms

from . import models


class ModelFormWithInlineFormsetMixin(object):
    '''
    Allow nested forms to be automatically saved.

    If a form containing an InlineFormset is dynamically created on the
    client the forms in the formset will not have an id of their parent
    (because it doesn't have one yet). This means that we first need to save
    the parent form and only then the child form can be saved. However, by
    default, the forms first saves its children, and only then saves the
    parent. This is why this class has to be used to save children an
    additional time after the parent has been saved.

    Deleted forms should not be saved, since their instance would already be
    deleted by super().save().

    Taken from https://github.com/Chirurgus/cookbox
    '''

    def save(self, commit=True):
        '''
        (Re)saves the related formsets, so that newly created
        nested formsets are also saved.
        '''
        # Save the parent
        ret = super().save(commit)
        if hasattr(self, 'formsets'):
            for formset in self.formsets.values():
                for form in formset.forms:
                    if not form in formset.deleted_forms:
                        form.save(commit)
        return ret


class SuperModelForm( ModelFormWithInlineFormsetMixin, SuperModelFormMixin, forms.ModelForm ):
    pass


def submit_buttons():
    return Row( 
        Submit("submit", "Save"), 
        HTML('<a class="btn btn-danger" style="margin-left: 10px;" href="../">Cancel</a>'),
    )


class RepositoryForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = models.Repository

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "identifier",
            "url",
            Row(Column("location_description"), Column("settlement"), css_class='form-row'),
            Row(Column("latitude"), Column("longitude"), css_class='form-row'),
            submit_buttons(),
        )

language_subtag_choices = sorted( 
    [(language['Subtag'],language['Description'][0]) for language in filter(lambda x: x['Type'] == "language", registry) ],
    key=lambda x: x[1],
)



class ChoiceWidget(s2forms.Select2Widget):
    def build_attrs(self, base_attrs, extra_attrs=None):
        base_attrs = super().build_attrs(base_attrs, extra_attrs)
        base_attrs.update(
            {
                "data-minimum-input-length": 0, 
                "data-placeholder": self.empty_label,
                # "data-theme": "bootstrap4",
            }
        )
        return base_attrs

    @property
    def media(self):
        media = super().media
        
        js = [x if x != "django_select2/django_select2.js" else "kutub/js/django_select2.js" for x in list(media._js)]
        css = dict(media._css)
        css['screen'] += ["https://cdn.jsdelivr.net/npm/@ttskch/select2-bootstrap4-theme/dist/select2-bootstrap4.min.css"]
        return forms.Media(
            css=css,
            js=js,
        )


class LanguageForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = models.Language
        widgets = {
            "language_subtag": ChoiceWidget,
            "extlang": ChoiceWidget,
            "script": ChoiceWidget,
            "region": ChoiceWidget,
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("description"), css_class='form-row'),
            Row(Column("language_subtag"), Column("extlang"), css_class='form-row'),
            Row(Column("script"), Column("region"), css_class='form-row'),
            submit_buttons(),
        )


class LanguageWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "description__icontains",
    ]

    def build_attrs(self, base_attrs, extra_attrs=None):
        base_attrs = super().build_attrs(base_attrs, extra_attrs)
        base_attrs.update(
            {
                "data-minimum-input-length": 0, 
                "data-placeholder": self.empty_label,
                "theme": "bootstrap4",
            }
        )
        return base_attrs


class ContentItemForm(SuperModelForm):
    class Meta:
        model = models.ContentItem
        fields = "__all__"
        widgets = {
            "other_languages": LanguageWidget,
        }


ContentItemFormSet = inlineformset_factory(
    model=models.ContentItem,
    parent_model=models.Manuscript,
    form=ContentItemForm,
    extra=0,
    can_delete=True
)


class ManuscriptForm(SuperModelForm):
    content_items = InlineFormSetField(formset_class=ContentItemFormSet)

    class Meta:
        fields = "__all__"
        model = models.Manuscript
        widgets = {
            "other_languages": LanguageWidget,
        }
