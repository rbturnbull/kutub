from django import template
from django.utils.safestring import mark_safe

from classytags.core import Tag, Options
from classytags.arguments import Argument

from .. import maps, models

register = template.Library()

class RepositoryMap(Tag):
    name = 'repository_map'
    options = Options(
        Argument('repository'),
    )

    def render_tag(self, context, repository):
        if repository.has_coords:
            r = maps.repositories_map(models.Repository.objects.filter(id=repository.id))
            return mark_safe(r.to_html(as_string=True))
        return ""


register.tag(RepositoryMap)


class AllRepositorysMap(Tag):
    name = 'all_repositories_map'
    def render_tag(self, context):
        r = maps.repositories_map( models.Repository.objects.exclude(latitude=None).exclude(longitude=None) )
        return mark_safe(r.to_html(as_string=True))

register.tag(AllRepositorysMap)


@register.filter(name='range')
def range(value):
    if value:
        return f"{value.lower}–{value.upper}" if value.upper else str(value.lower)
    return ""

@register.filter(name='dimensions')
def dimensions(manuscript):
    if manuscript.width:
        if manuscript.height:
            return f"{ manuscript.height } ✖️ {manuscript.width} mm"
        return f"Width: { manuscript.width } mm"
    if manuscript.height:
        return f"Height: {manuscript.height} mm"
    return ""

@register.filter(name='help_text')
def help_text(obj, field_name):
    return obj.field_help(field_name)

@register.filter(name='help_text_tooltip')
def help_text_tooltip(obj, field_name, placement="bottom"):
    text = help_text(obj, field_name=field_name)
    return mark_safe(f' data-toggle="tooltip" data-placement="{placement}" title="{text}" ')

@register.inclusion_tag('kutub/attribute_row.html')
def attribute_row(object, field_name, suffix="", header=""):
    header = header or field_name.replace("_", " ").title()
    return {
        'object': object,
        'field_name': field_name,
        'value': getattr(object, field_name),
        'placement': "bottom",
        "help_text": object.field_help(field_name),
        "suffix": suffix,
        "header": header,
    }


@register.inclusion_tag('kutub/grid_attribute.html')
def grid_attribute(object, field_name, suffix="", header="", cols=None, url="", blanktext=""):
    header = header or object.field_attr(field_name, "verbose_name").title()
    value = getattr(object, field_name) or blanktext
    if not url and hasattr(value, "get_absolute_url"):
        url = value.get_absolute_url()

    return {
        'object': object,
        'field_name': field_name,
        'value': value,
        'placement': "bottom",
        "help_text": object.field_help(field_name),
        "docs": object.field_docs(field_name),
        "tag": object.field_tag(field_name),
        "suffix": suffix,
        "header": header,
        "cols": cols,
        "url": url,
    }

@register.inclusion_tag('kutub/grid_attribute_form.html')
def grid_attribute_form(form, field_name, cols=None, header="", suffix="", url="", blanktext=""):
    """
    header and suffix are ignored. They are defined just to make the arguments compatible with grid_attribute
    """
    field = form[field_name]
    docs = getattr(field.field, 'docs') if hasattr(field.field, 'docs') else ""
    return {
        'field': field,
        'cols': cols,
        'docs': docs,
        'placement': "bottom",
    }

