from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from base.models import Anuncio, Imovel


class AnuncioAPITests(APITestCase):
    def setUp(self):
        self.add_anuncio_url = reverse("api_anuncios:add_anuncio")
        self.get_anuncios_url = reverse("api_anuncios:get_anuncios")
        self.alter_anuncio_url = reverse("api_anuncios:alter_anuncio")

        self.imovel = Imovel.objects.create(
            limite_hospedes=4,
            quantidade_banheiros=1,
            aceita_animais=True,
            valor_limpeza=20.0,
            data_ativacao="2022-01-01",
        )

    def test_add_anuncio_success(self):
        data = {
            "cod_imovel": self.imovel.id,
            "plataforma": "airbnb",
            "taxa_plataforma": 99.99,
        }
        response = self.client.post(self.add_anuncio_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_anuncios_success(self):
        anuncio = Anuncio.objects.create(
            cod_imovel=self.imovel,
            plataforma="airbnb",
            taxa_plataforma=99.99,
        )
        response = self.client.get(self.get_anuncios_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_anuncios_url_param_success(self):
        anuncio = Anuncio.objects.create(
            cod_imovel=self.imovel,
            plataforma="airbnb",
            taxa_plataforma=99.99,
        )
        url_param = self.get_anuncios_url + "?id=" + str(anuncio.id)
        response = self.client.get(url_param)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_alter_anuncio_success(self):
        anuncio = Anuncio.objects.create(
            cod_imovel=self.imovel,
            plataforma="airbnb",
            taxa_plataforma=99.99,
        )
        data = {
            "id": anuncio.id,
            "fields": {
                "plataforma": "outra plataforma",
            },
        }
        response = self.client.post(self.alter_anuncio_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Anuncio.objects.get(id=anuncio.id).plataforma, "outra plataforma"
        )

    """

    TESTES DE FALHAS

    """

    # TESTES ADD ANUNCIO - INICIO - FAILURE
    def test_add_anuncio_campo_faltante_failure(self):
        # campos faltante para adicionar um anuncio
        data = {
            # Faltando campo "plataforma"
            "cod_imovel": self.imovel.id,
            # "plataforma": True,
            "taxa_plataforma": 10.05,
        }
        response = self.client.post(self.add_anuncio_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_anuncio_tipo_incorreto_failure(self):
        # tipo do dados inválidos para adicionar um anuncio
        data = {
            "cod_imovel": self.imovel.id,
            "plataforma": True,
            "taxa_plataforma": 10.05,
        }
        response = self.client.post(self.add_anuncio_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TESTES ADD ANUNCIO - FIM - FAILURE

    # TESTES GET ANUNCIO - INICIO - FAILURE
    def test_get_anuncios_failure(self):
        # Nenhum anuncio no banco de dados
        response = self.client.get(self.get_anuncios_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_anuncios_url_param_failure(self):
        # ID de anuncio inválido
        url_param = self.get_anuncios_url + "?id=999999"  # ID que não existe
        response = self.client.get(url_param)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # TESTES GET ANUNCIO - FIM - FAILURE

    # TESTES ALTER ANUNCIO - INICIO - FAILURE
    def test_alter_anuncio_not_exist_failure(self):
        # Tentando alterar um anuncio que não existe
        data = {
            "id": 999,
            "fields": {
                "plataforma": "outra plataforma",
            },
        }
        response = self.client.post(self.alter_anuncio_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_alter_anuncio_campos_faltantes_failure(self):
        # Tentando alterar um anuncio sem passar o id

        anuncio = Anuncio.objects.create(
            cod_imovel=self.imovel,
            plataforma="airbnb",
            taxa_plataforma=99.99,
        )
        data = {
            "fields": {
                "plataforma": "outra plataforma",
            },
        }
        response = self.client.post(self.alter_anuncio_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_alter_anuncio_tipos_invalidos_failure(self):
        # Tipo dos dados inválidos para alterar um anuncio
        anuncio = Anuncio.objects.create(
            cod_imovel=self.imovel,
            plataforma="airbnb",
            taxa_plataforma=99.99,
        )
        data = {
            "id": anuncio.id,
            "fields": {
                "taxa_plataforma": "99.99",
            },
        }
        response = self.client.post(self.alter_anuncio_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_alter_anuncio_campos_invalidos_failure(self):

        # campos inválidos para alterar um anuncio
        data = {
            "id": self.imovel.id,
            "fields": {
                "campo_inexistente": "valor_invalido",
            },
        }
        response = self.client.post(self.alter_anuncio_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TESTES ALTER ANUNCIO - FIM - FAILURE
