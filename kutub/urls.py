from django.urls import path
from . import views

app_name = "kutub"
urlpatterns = [
    # path("languages/", views.LanguageListView.as_view(), name="language-list"),
    # path("languages/<str:slug>/", views.LanguageDetailView.as_view(), name="language-detail"),

    # path("scripts/", views.ScriptListView.as_view(), name="script-list"),
    # path("scripts/<str:slug>/", views.ScriptDetailView.as_view(), name="script-detail"),

    # path("materials/", views.MaterialListView.as_view(), name="material-list"),
    # path("materials/<str:slug>/", views.MaterialDetailView.as_view(), name="material-detail"),

    path("repositories/", views.RepositoryListView.as_view(), name="repository-list"),
    path("repositories/map/", views.AllRepositoriesMapView.as_view(), name="all-repositories-map"),
    path("repositories/create/", views.RepositoryCreateView.as_view(), name="repository-create"),
    path("repositories/<str:slug>/map/", views.RepositoryMapView.as_view(), name="repository-map"),
    path("repositories/<str:slug>/update/", views.RepositoryUpdateView.as_view(), name="repository-update"),
    path("repositories/<str:slug>/", views.RepositoryDetailView.as_view(), name="repository-detail"),

    # path("", views.DocumentListView.as_view(), name="index"),
    # path("documents/", views.DocumentListView.as_view(), name="document-list"),
    # path("documents/create/", views.DocumentCreateView.as_view(), name="document-create"),
    # path("documents/<str:slug>/", views.DocumentDetailView.as_view(), name="document-detail"),
    # path("documents/<str:slug>/iiif/", views.DocumentIIIFManifestView.as_view(), name="document-iiif"),
    # path("documents/<str:slug>/update/", views.DocumentUpdateView.as_view(), name="document-update"),

    # path("tags/", views.DocumentTagListView.as_view(), name="documenttag-list"),
    # path("tags/<str:slug>/", views.DocumentTagDetailView.as_view(), name="documenttag-detail"),

    # path("info/", views.InfoCategoryListView.as_view(), name="infocategory-list"),
    # path("info/<str:slug>/", views.InfoCategoryDetailView.as_view(), name="infocategory-detail"),

]
