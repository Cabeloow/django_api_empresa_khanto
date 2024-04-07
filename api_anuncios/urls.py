from django.urls import path
from . import views

urlpatterns = [
    path("include_anuncio/", views.add_anuncio),
    path("get_anuncios/", views.get_anuncios),
    path("alter_anuncio/", views.alter_anuncio),
]
