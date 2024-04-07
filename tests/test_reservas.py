from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from base.models import Imovel, Anuncio, Reserva


class ReservaAPITests(APITestCase):
    def setUp(self):
        self.add_reserva_url = reverse("api_reservas:add_reserva")
        self.get_reservas_url = reverse("api_reservas:get_reservas")
        self.del_reserva_url = reverse("api_reservas:del_reserva")

        self.imovel = Imovel.objects.create(
            limite_hospedes=4,
            quantidade_banheiros=1,
            aceita_animais=True,
            valor_limpeza=20.0,
            data_ativacao="2022-01-01",
        )

        self.anuncio = Anuncio.objects.create(
            cod_imovel=self.imovel,
            plataforma="airbnb",
            taxa_plataforma=99.99,
        )

    def test_add_reserva_success(self):
        data = {
            "cod_anuncio": self.anuncio.id,
            "data_checkin": "2024-04-20",
            "data_checkout": "2024-04-23",
            "preco_total": 25.99,
            "comentario": "meu comentario",
            "numero_hospedes": 1,
        }
        response = self.client.post(self.add_reserva_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reservas_success(self):
        reserva = Reserva.objects.create(
            cod_anuncio=self.anuncio,
            data_checkin="2024-04-20",
            data_checkout="2024-04-23",
            preco_total=25.99,
            comentario="meu comentario",
            numero_hospedes=1,
        )
        response = self.client.get(self.get_reservas_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reservas_url_param_success(self):
        reserva = Reserva.objects.create(
            cod_anuncio=self.anuncio,
            data_checkin="2024-04-20",
            data_checkout="2024-04-23",
            preco_total=25.99,
            comentario="meu comentario",
            numero_hospedes=1,
        )
        url_param = self.get_reservas_url + "?id=" + str(reserva.id)
        response = self.client.get(url_param)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_del_reserva_success(self):
        reserva = Reserva.objects.create(
            cod_anuncio=self.anuncio,
            data_checkin="2024-04-20",
            data_checkout="2024-04-23",
            preco_total=25.99,
            comentario="meu comentario",
            numero_hospedes=1,
        )
        data = {"id": reserva.id}
        response = self.client.delete(self.del_reserva_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """

    TESTES DE FALHAS

    """

    # TESTES ADD RESERVA - INICIO - FAILURE
    def test_add_reserva_campo_faltante_failure(self):
        # Campos faltantes para adicionar um reserva
        data = {
            # faltandoo campo preco_total
            "cod_anuncio": self.anuncio.id,
            "data_checkin": "2024-04-20",
            "data_checkout": "2024-04-23",
            # "preco_total": 25.99,
            "comentario": "meu comentario",
            "numero_hospedes": 1,
        }
        response = self.client.post(self.add_reserva_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_reserva_tipo_incorreto_failure(self):
        # Tipo dos dados inválidos para adicionar um reserva
        data = {
            "cod_anuncio": self.anuncio.id,
            "data_checkin": "2024-04-20",
            "data_checkout": "2024-04-23",
            "preco_total": 25.99,
            "comentario": 2,
            "numero_hospedes": "1",
        }
        response = self.client.post(self.add_reserva_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TESTES ADD RESERVA - FIM - FAILURE

    # TESTES GET RESERVA - INICIO - FAILURE
    def test_get_reservas_failure(self):
        # Nenhum reserva no banco de dados
        response = self.client.get(self.get_reservas_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_reservas_url_param_failure(self):
        # ID de reserva inválido
        url_param = self.get_reservas_url + "?id=999999"  # ID que não existe
        response = self.client.get(url_param)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # TESTES GET RESERVA - FIM - FAILURE

    # TESTES DEL RESERVA - INICIO - FAILURE
    def test_del_reserva_failure(self):
        # Tentando excluir um reserva que não existe
        data = {"id": 999999}  # ID que não existe
        response = self.client.delete(self.del_reserva_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_del_reserva_campos_faltantes_failure(self):
        # Tentando excluir um reserva sem passar o id
        data = {"ids": 1}  # ID que não existe
        response = self.client.delete(self.del_reserva_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TESTES DEL RESERVA - FIM - FAILURE
