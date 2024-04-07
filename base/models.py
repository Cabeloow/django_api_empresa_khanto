from django.db import models
from django.utils import timezone
import uuid

# Create your models here.


class Imovel(models.Model):
    cod_imovel = models.Index(fields=["Sequence"])
    limite_hospedes = models.IntegerField()
    quantidade_banheiros = models.IntegerField()
    aceita_animais = models.BooleanField(default=False)
    valor_limpeza = models.DecimalField(max_digits=10, decimal_places=2)
    data_ativacao = models.DateField()
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)


class Anuncio(models.Model):
    cod_anuncio = models.Index(fields=["Sequence"])
    cod_imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    plataforma = models.CharField(max_length=100)
    taxa_plataforma = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)


class Reserva(models.Model):
    cod_reserva = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    cod_anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE)
    data_checkin = models.DateField()
    data_checkout = models.DateField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    comentario = models.TextField(blank=True)
    numero_hospedes = models.IntegerField()
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)
