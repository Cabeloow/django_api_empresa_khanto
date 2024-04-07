from django.urls import path
from . import views

urlpatterns = [
    path("include_imovel/", views.add_imovel),
    path("get_imoveis/", views.get_imoveis),
    path("del_imovel/", views.del_imovel),
    path("alter_imovel/", views.alter_imovel),
]
