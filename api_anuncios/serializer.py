from rest_framework import serializers
from base.models import Anuncio


class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = "__all__"
