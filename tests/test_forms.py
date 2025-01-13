from kutub.forms import ManuscriptForm

def test_manuscript_form_class():
    assert str(ManuscriptForm.__class__) == "<class 'django_superform.forms.SuperModelFormMetaclass'>"


def test_manuscript_form_registration():
    assert isinstance(ManuscriptForm.base_composite_fields, dict)    


def test_manuscript_form_base_composite_fields():
    form = ManuscriptForm()
    assert isinstance(form.base_composite_fields, dict)