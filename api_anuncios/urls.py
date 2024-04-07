from django.urls import path
from . import views

app_name = "api_anuncios"

urlpatterns = [
    path("include_anuncio/", views.add_anuncio, name="add_anuncio"),
    path("get_anuncios/", views.get_anuncios, name="get_anuncios"),
    path("alter_anuncio/", views.alter_anuncio, name="alter_anuncio"),
]
