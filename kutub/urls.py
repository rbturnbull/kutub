from django.urls import path
from . import views

app_name = "kutub"
urlpatterns = [
    path("repositories/", views.RepositoryListView.as_view(), name="repository-list"),
    path("repositories/map/", views.AllRepositoriesMapView.as_view(), name="all-repositories-map"),
    path("repositories/create/", views.RepositoryCreateView.as_view(), name="repository-create"),
    path("repositories/<str:slug>/map/", views.RepositoryMapView.as_view(), name="repository-map"),
    path("repositories/<str:slug>/update/", views.RepositoryUpdateView.as_view(), name="repository-update"),
    path("repositories/<str:slug>/", views.RepositoryDetailView.as_view(), name="repository-detail"),

    path("", views.ManuscriptListView.as_view(), name="index"),
    path("mss/", views.ManuscriptListView.as_view(), name="manuscript-list"),
    path("mss/create/", views.ManuscriptCreateView.as_view(), name="manuscript-create"),
    path("mss/<str:slug>/", views.ManuscriptDetailView.as_view(), name="manuscript-detail"),
    path("mss/<str:slug>/tei/", views.ManuscriptTEIView.as_view(), name="manuscript-tei"),
    path("mss/<str:slug>/iiif/", views.ManuscriptIIIFManifestView.as_view(), name="manuscript-iiif"),
    path("mss/<str:slug>/update/", views.ManuscriptUpdateView.as_view(), name="manuscript-update"),

    path("languages/", views.LanguageListView.as_view(), name="language-list"),
    path("languages/create/", views.LanguageCreateView.as_view(), name="language-create"),
    path("languages/<str:slug>/", views.LanguageDetailView.as_view(), name="language-detail"),
    path("languages/<str:slug>/update/", views.LanguageUpdateView.as_view(), name="language-update"),

    path("tags/", views.TagListView.as_view(), name="tag-list"),
    path("tags/<str:slug>/", views.TagDetailView.as_view(), name="tag-detail"),

]
