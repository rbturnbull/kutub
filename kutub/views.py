from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
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


