from django.urls import path
from . import views

urlpatterns = [
    path("include_reserva/", views.add_reserva),
    path("get_reservas/", views.get_reservas),
    path("del_reserva/", views.del_reserva),
]
