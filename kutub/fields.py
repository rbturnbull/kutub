from django.db import models

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
        super().__init__(*args, **kwargs)

    def reference_url(self):
        return f"https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-{self.tag}.html"