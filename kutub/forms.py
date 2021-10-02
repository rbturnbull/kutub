from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from django.forms.models import inlineformset_factory
from django_superform.forms import SuperModelFormMixin
from django_superform import InlineFormSetField

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

class LanguageForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = models.Language

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "identifier",
            "url",
            Row(Column("description"), css_class='form-row'),
            Row(Column("language_subtag"), Column("extlang"), css_class='form-row'),
            Row(Column("script"), Column("region"), css_class='form-row'),
            submit_buttons(),
        )


class ContentItemForm(SuperModelForm):
    class Meta:
        model = models.ContentItem
        fields = "__all__"


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

