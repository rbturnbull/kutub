from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse

from reversion.views import RevisionMixin

from . import models, forms

PAGINATION = 30

class TitleFromObjectMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        context['title'] = str(object)
        
        if isinstance(self, UpdateView):
            context['title'] += " Update"
        
        return context


######################## 
##      Repository
######################## 

class RepositoryView(PermissionRequiredMixin):
    model = models.Repository
    permission_required = "kutub.view_repository"


class RepositoryListView(RepositoryView, ListView):
    paginate_by = PAGINATION

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_map'] = (models.Repository.objects.exclude(latitude=None).exclude(longitude=None).count() > 0)
        return context

class RepositoryDetailView(TitleFromObjectMixin, RepositoryView, DetailView):
    pass


class RepositoryMapView(RepositoryDetailView):
    template_name = "kutub/repository_map.html"


class RepositoryUpdateView(TitleFromObjectMixin, RevisionMixin, RepositoryView, UpdateView):
    permission_required = "kutub.update_repository"
    form_class = forms.RepositoryForm
    template_name = "kutub/form.html"
    extra_context = dict(form_title="Update Repository")


class RepositoryCreateView(RevisionMixin, RepositoryView, CreateView):
    permission_required = "kutub.add_repository"
    form_class = forms.RepositoryForm
    template_name = "kutub/form.html"
    extra_context = dict(form_title="Add Repository")


class AllRepositoriesMapView(TemplateView):
    template_name = "kutub/all_repositories_map.html"



######################## 
##      Manuscript
######################## 

class ManuscriptView(PermissionRequiredMixin):
    model = models.Manuscript
    permission_required = "kutub.view_manuscript"


class ManuscriptListView(ManuscriptView, ListView):
    paginate_by = PAGINATION
    extra_context = dict(title="Manuscript List")


class ManuscriptDetailView(TitleFromObjectMixin, ManuscriptView, DetailView):
    pass


class ManuscriptTEIView(ManuscriptDetailView):
    def get(self, request, *args, **kwargs):
        object = self.get_object()
        return HttpResponse(object.xml_pretty_print(), content_type='text/xml')


class ManuscriptIIIFManifestView(ManuscriptDetailView):
    template_name = "kutub/iiif_manifest.html"


class ManuscriptUpdateView(TitleFromObjectMixin, RevisionMixin, ManuscriptView, UpdateView):
    permission_required = "kutub.update_manuscript"
    form_class = forms.ManuscriptForm
    template_name = "kutub/manuscript_form.html"
    extra_context = dict(form_title="Update Manuscript")


class ManuscriptCreateView(RevisionMixin, ManuscriptView, CreateView):
    permission_required = "kutub.add_manuscript"
    form_class = forms.ManuscriptForm
    template_name = "kutub/manuscript_form.html"
    extra_context = dict(form_title="Add Manuscript")


######################## 
##      Language
######################## 

class LanguageView(PermissionRequiredMixin):
    model = models.Language
    permission_required = "kutub.view_language"
    slug_field = 'tag'


class LanguageListView(LanguageView, ListView):
    paginate_by = PAGINATION
    extra_context = dict(title="Language List")


class LanguageDetailView(TitleFromObjectMixin, LanguageView, DetailView):
    pass


class LanguageUpdateView(TitleFromObjectMixin, RevisionMixin, LanguageView, UpdateView):
    permission_required = "kutub.update_language"
    form_class = forms.LanguageForm
    template_name = "kutub/language_form.html"
    extra_context = dict(form_title="Update Language")


class LanguageCreateView(RevisionMixin, LanguageView, CreateView):
    permission_required = "kutub.add_language"
    form_class = forms.LanguageForm
    template_name = "kutub/language_form.html"
    extra_context = dict(form_title="Add Language")    


######################## 
##      Tag
######################## 

class TagView(PermissionRequiredMixin):
    model = models.Tag
    permission_required = "kutub.view_documenttag"


class TagListView(TagView, ListView):
    paginate_by = PAGINATION
    context_object_name = "tag"
    extra_context = dict(title="Tags")


class TagDetailView(TagView, DetailView):
    context_object_name = "tag"    