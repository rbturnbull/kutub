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

@register.filter(name='range')
def range(value):
    if value:
        return f"{value.lower}–{value.upper}" if value.upper else str(value.lower)
    return ""

@register.filter(name='dimensions')
def dimensions(manuscript):
    if manuscript.width:
        if manuscript.height:
            return f"{ range(manuscript.width) } ✖️ {range(manuscript.height)} mm"
        return f"Width: { range(manuscript.width) } mm"
    if manuscript.height:
        return f"Height: {range(manuscript.height)} mm"
    return ""
