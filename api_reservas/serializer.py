from rest_framework import serializers
from base.models import Reserva


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"
