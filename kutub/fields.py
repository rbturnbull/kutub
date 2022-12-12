from django.db import models
from django.core.validators import RegexValidator
from django import forms
from django.utils.text import capfirst


class DescriptionField(models.TextField):
    description = "A text field that can corresponds to a TEI element."

    def __init__(self, tag="", docs="", default="", blank=True, *args, **kwargs):
        """
        tag is the TEI xml tag that corresponds to this field.
        docs is a URL that links to the TEI documentation with a description of the use of this tag in the correct context.
        NB docs does not refer to the reference page for the xml tag. That is found it the `reference` method.
        """
        self.tag = tag
        self.docs = docs
        kwargs['default'] = default
        kwargs['blank'] = blank
        validators = kwargs.get('validators') or []
        if len(validators) == 0: # if there are validators, then we should check if one of the validators is one for XML chars.
            validators.append(
                RegexValidator(u'^[\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]*$', 'Only valid XML characters allowed.')
            )
        kwargs['validators'] = validators
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'widget': forms.Textarea(attrs={'rows':1}),
        }
        formfield = super().formfield(**defaults)
        formfield.docs = self.docs
        formfield.tag = self.tag
        return formfield

    def reference_url(self):
        return f"https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-{self.tag}.html"




class CharField(models.CharField):
    def __init__(self, docs="", default="", blank=True, *args, **kwargs):
        """
        A CharField with docs
        """
        self.docs = docs
        kwargs['default'] = default
        kwargs['blank'] = blank
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        formfield = super().formfield(**kwargs)
        formfield.docs = self.docs
        return formfield
