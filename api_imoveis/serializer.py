from rest_framework import serializers
from base.models import Imovel


class ImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imovel
        fields = "__all__"
