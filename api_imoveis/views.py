from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils.validations import valida_ids_get
from .serializer import ImovelSerializer
from base.models import Imovel
from rest_framework import status
from django.db import IntegrityError


@api_view(["POST"])
def add_imovel(request):
    """
    View para adicionar um imóvel.

    Args:
        request (Request): Requisição HTTP contendo os dados do imóvel a ser adicionado.

    Returns:
        Response: Uma resposta HTTP indicando o resultado da operação.

    Raises:
        Exception: Se ocorrer algum erro durante o processamento do imóvel.

    Examples:
        Um exemplo do formato esperado dos dados de cadastro de imovel:

        imovel_json_example = {
            "limite_hospedes": 6, // int
            "quantidade_banheiros": 2, // int
            "aceita_animais": true, // boolean
            "valor_limpeza": 10.05, // float
            "data_ativacao": "2020-12-21" // string (data no formato americano YYYY-MM-DD)
        }

    """
    try:
        # Obter os dados do imóvel da requisição
        serializer = ImovelSerializer(data=request.data)
        if serializer.is_valid():
            # Se os dados forem válidos, salvar o imóvel
            serializer.save()

        else:
            # Se os dados forem inválidos, retornar uma resposta de erro
            return Response(
                data={
                    "error": "Opa! algo deu errado. Verifique se todos os campos estão corretos e tente novamente."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retornar uma resposta de sucesso
        return Response(
            data={"message": "Imóvel cadastrado com sucesso!"},
            status=status.HTTP_200_OK,
        )

    except Exception as erro:
        # Se ocorrer um erro, retornar uma resposta de erro
        return Response(
            data={"error": str(erro)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def get_imoveis(request):
    """
    View para obter imóveis.

    Args:
        request (Request): Requisição HTTP contendo os parâmetros de filtragem.

    Returns:
        Response: Uma resposta HTTP contendo os registros de imóveis.

    Raises:
        Exception: Se ocorrer algum erro durante a obtenção dos registros.

    """
    try:
        # Obter o parâmetro de consulta "id" da requisição
        param = request.query_params.get("id", None)

        registros = valida_ids_get(Imovel, param)

        # Serializar os registros de imóveis
        serializer = ImovelSerializer(registros, many=True)

        # Retornar uma resposta contendo os dados serializados
        return Response(serializer.data)
    except Exception as erro:
        # Se ocorrer um erro, retornar uma resposta de erro
        return Response(
            data={"error": str(erro)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["DELETE"])
def del_imovel(request):
    """
    View para deletar um imóvel.

    Args:
        request (Request): Requisição HTTP contendo os dados do imóvel a ser deletado.

    Returns:
        Response: Uma resposta HTTP indicando o resultado da operação de deleção.

    Raises:
        KeyError: Se o campo "id" não estiver presente nos dados da requisição.

    Examples:
        Um exemplo do formato esperado dos dados de deletar imovel:

        del_imovel_json_example = {
            "id":1 int
        }

    """
    try:
        # Obter o ID do imóvel a ser deletado dos dados da requisição
        filtro = request.data
        # Filtrar o registro de imóvel com base no ID fornecido
        registro = Imovel.objects.filter(id=filtro["id"])
        if not registro:
            return Response(
                data={"error": f"id do imóvel não encontrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = registro.delete()
        # Retornar uma resposta indicando o resultado da operação de deleção
        return Response(result)
    except KeyError as error:
        # Se o campo "id" não estiver presente nos dados da requisição, retornar uma resposta de erro
        return Response(
            data={"error": error},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def alter_imovel(request):
    """
    View para alterar um imóvel.

    Args:
        request (Request): Requisição HTTP contendo os dados do imóvel a ser alterado.

    Returns:
        Response: Uma resposta HTTP indicando o resultado da operação de alteração.

    Raises:
        Exception: Se ocorrer algum erro durante o processamento do imóvel.

    Examples:
        Um exemplo do formato esperado dos dados de alterar um imovel:
        json_alter_example = {
            "id":1, // int
            "fields":{
                "limite_hospedes":2,
                "aceita_animais": false,
                "valor_limpeza": 29.99,

            }
        }

    """
    try:
        # Obter os dados do imóvel a ser alterado da requisição
        filtro = request.data
        # Obter o registro do imóvel a ser alterado com base no ID fornecido
        registro = Imovel.objects.get(id=filtro["id"])

        # Iterar sobre os campos a serem alterados
        for field in filtro["fields"].keys():
            valor_field = filtro["fields"][field]
            # Atribuir o novo valor ao campo do registro
            setattr(registro, field, valor_field)
            # Salvar as mudanças no registro
            registro.save()

        # Obter novamente o registro de imóvel alterado
        registros = Imovel.objects.filter(id=filtro["id"])

        # Serializar o registro de imóvel alterado
        serializer = ImovelSerializer(registros, many=True)

        # Retornar uma resposta contendo os dados serializados do imóvel alterado
        return Response(serializer.data)
    except Exception as erro:
        # Se ocorrer um erro, retornar uma resposta de erro
        return Response(
            data={"error": str(erro)},
            status=status.HTTP_400_BAD_REQUEST,
        )
