from django.urls import path
from . import views

app_name = "api_imoveis"
urlpatterns = [
    path("include_imovel/", views.add_imovel, name="add_imovel"),
    path("get_imoveis/", views.get_imoveis, name="get_imoveis"),
    path("del_imovel/", views.del_imovel, name="del_imovel"),
    path("alter_imovel/", views.alter_imovel, name="alter_imovel"),
]
