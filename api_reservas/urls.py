from django.urls import path
from . import views


app_name = "api_reservas"
urlpatterns = [
    path("include_reserva/", views.add_reserva, name="add_reserva"),
    path("get_reservas/", views.get_reservas, name="get_reservas"),
    path("del_reserva/", views.del_reserva, name="del_reserva"),
]
