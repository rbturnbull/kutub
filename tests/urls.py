from django.urls import include, path

urlpatterns = [
    path("kutub/", include("kutub.urls")),
]