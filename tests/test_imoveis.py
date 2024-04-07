from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from base.models import Imovel


class ImovelAPITests(APITestCase):
    def setUp(self):
        self.add_imovel_url = reverse("api_imoveis:add_imovel")
        self.get_imoveis_url = reverse("api_imoveis:get_imoveis")
        self.del_imovel_url = reverse("api_imoveis:del_imovel")
        self.alter_imovel_url = reverse("api_imoveis:alter_imovel")

    # TESTES ADD IMOVEL - INICIO - SUCCESS
    def test_add_imovel_success(self):
        data = {
            "limite_hospedes": 6,
            "quantidade_banheiros": 2,
            "aceita_animais": True,
            "valor_limpeza": 10.05,
            "data_ativacao": "2020-12-21",
        }
        response = self.client.post(self.add_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TESTES GET IMOVEL - INICIO - SUCCESS
    def test_get_imoveis_success(self):
        imovel = Imovel.objects.create(
            limite_hospedes=4,
            quantidade_banheiros=1,
            aceita_animais=True,
            valor_limpeza=20.0,
            data_ativacao="2022-01-01",
        )
        response = self.client.get(self.get_imoveis_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_imoveis_url_param_success(self):
        imovel = Imovel.objects.create(
            limite_hospedes=4,
            quantidade_banheiros=1,
            aceita_animais=True,
            valor_limpeza=20.0,
            data_ativacao="2022-01-01",
        )
        url_param = self.get_imoveis_url + "?id=" + str(imovel.id)
        response = self.client.get(url_param)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TESTES DEL IMOVEL - INICIO - SUCCESS
    def test_del_imovel_success(self):
        imovel = Imovel.objects.create(
            limite_hospedes=4,
            quantidade_banheiros=1,
            aceita_animais=True,
            valor_limpeza=20.0,
            data_ativacao="2022-01-01",
        )
        data = {"id": imovel.id}
        response = self.client.delete(self.del_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TESTES ALTER IMOVEL - INICIO - SUCCESS
    def test_alter_imovel_success(self):
        imovel = Imovel.objects.create(
            limite_hospedes=4,
            quantidade_banheiros=1,
            aceita_animais=True,
            valor_limpeza=20.0,
            data_ativacao="2022-01-01",
        )
        data = {
            "id": imovel.id,
            "fields": {
                "limite_hospedes": 6,
                "aceita_animais": False,
                "valor_limpeza": 25.0,
            },
        }
        response = self.client.post(self.alter_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Imovel.objects.get(id=imovel.id).limite_hospedes, 6)
        self.assertEqual(Imovel.objects.get(id=imovel.id).aceita_animais, False)
        self.assertEqual(Imovel.objects.get(id=imovel.id).valor_limpeza, 25.0)

    """

    TESTES DE FALHAS

    """

    # TESTES ADD IMOVEL - INICIO - FAILURE
    def test_add_imovel_campo_faltante_failure(self):
        # Campos faltantes para adicionar um imóvel
        data = {
            # Faltando campo "limite_hospedes"
            "quantidade_banheiros": 2,
            "aceita_animais": True,
            "valor_limpeza": 10.05,
            "data_ativacao": "2020-12-21",
        }
        response = self.client.post(self.add_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_imovel_tipo_incorreto_failure(self):
        # Tipo dos dados inválidos para adicionar um imóvel
        data = {
            "limite_hospedes": "4",
            "quantidade_banheiros": 2,
            "aceita_animais": True,
            "valor_limpeza": 10.05,
            "data_ativacao": "2020-12-21",
        }
        response = self.client.post(self.add_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TESTES ADD IMOVEL - FIM - FAILURE

    # TESTES GET IMOVEL - INICIO - FAILURE
    def test_get_imoveis_failure(self):
        # Nenhum imóvel no banco de dados
        response = self.client.get(self.get_imoveis_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_imoveis_url_param_failure(self):
        # ID de imóvel inválido
        url_param = self.get_imoveis_url + "?id=999999"  # ID que não existe
        response = self.client.get(url_param)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # TESTES GET IMOVEL - FIM - FAILURE

    # TESTES DEL IMOVEL - INICIO - FAILURE
    def test_del_imovel_failure(self):
        # Tentando excluir um imóvel que não existe
        data = {"id": 999999}  # ID que não existe
        response = self.client.delete(self.del_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_del_imovel_campos_faltantes_failure(self):
        # Tentando excluir um imóvel sem passar id
        data = {"ids": 1}
        response = self.client.delete(self.del_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TESTES DEL IMOVEL - FIM - FAILURE

    # TESTES ALTER IMOVEL - INICIO - FAILURE
    def test_alter_imovel_not_exist_failure(self):
        # Tentando alterar um imóvel que não existe
        data = {
            "id": 999,  # ID que não existe
            "fields": {
                "limite_hospedes": 6,
                "aceita_animais": False,
                "valor_limpeza": 25.0,
            },
        }
        response = self.client.post(self.alter_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_alter_imovel_campos_faltantes_failure(self):
        # Tentando alterar um imóvel sem passar o id

        data = {
            "fields": {
                "limite_hospedes": 6,
                "aceita_animais": False,
                "valor_limpeza": 25.0,
            },
        }
        response = self.client.post(self.alter_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_alter_imovel_tipos_invalidos_failure(self):
        # passando tipo de dados invalidos ao alterar um imovel
        imovel = Imovel.objects.create(
            limite_hospedes=4,
            quantidade_banheiros=1,
            aceita_animais=True,
            valor_limpeza=20.0,
            data_ativacao="2022-01-01",
        )
        data = {
            "id": imovel.id,
            "fields": {
                "limite_hospedes": "6",
                "aceita_animais": False,
                "valor_limpeza": 25.0,
            },
        }
        response = self.client.post(self.alter_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_alter_imovel_campos_invalidos_failure(self):
        # campos inválidos para alterar um imóvel
        imovel = Imovel.objects.create(
            limite_hospedes=4,
            quantidade_banheiros=1,
            aceita_animais=True,
            valor_limpeza=20.0,
            data_ativacao="2022-01-01",
        )
        # Tentando alterar um campo inexistente
        data = {
            "id": imovel.id,
            "fields": {
                "campo_inexistente": "valor_invalido",
            },
        }
        response = self.client.post(self.alter_imovel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TESTES ALTER IMOVEL - FIM - FAILURE
