from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from utils.validations import valida_ids_get
from .serializer import AnuncioSerializer
from base.models import Anuncio


@api_view(["POST"])
def add_anuncio(request):
    """
    View para adicionar um novo anúncio.

    Args:
        request (Request): Requisição HTTP contendo os dados do novo anúncio.

    Returns:
        Response: Uma resposta HTTP indicando o resultado da operação de adição.

    Raises:
        Exception: Se ocorrer uma exceção durante o processamento.

    Examples:
        Um exemplo do formato esperado dos dados de cadastro de um anuncio:

        anuncio_json_example = {
            "cod_imovel": 1, // int
            "plataforma": "airbnb", // string
            "taxa_plataforma": 99.99 // float
        }


    """
    try:
        # Validar e salvar os dados do anúncio
        serializer = AnuncioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                data={"error": "Opa, algo deu errado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retornar uma resposta de sucesso
        return Response(
            data={"message": "Anúncio salvo com sucesso!"},
            status=status.HTTP_200_OK,
        )
    except Exception as error:
        # Se ocorrer uma exceção durante o processamento, retornar uma resposta de erro
        return Response(
            data={"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def get_anuncios(request):
    """
    View para obter anúncios.

    Args:
        request (Request): Requisição HTTP contendo os parâmetros de filtragem.

    Returns:
        Response: Uma resposta HTTP contendo os registros de anúncios.

    Raises:
        Exception: Se ocorrer uma exceção durante o processamento.

    """
    try:
        # Obter o parâmetro de consulta "id" da requisição
        param = request.query_params.get("id", None)

        registros = valida_ids_get(Anuncio, param)

        # Serializar os registros de anúncios
        serializer = AnuncioSerializer(registros, many=True)

        # Retornar uma resposta contendo os dados serializados
        return Response(serializer.data)
    except Exception as error:
        # Se ocorrer uma exceção durante o processamento, retornar uma resposta de erro
        return Response(
            data={"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def alter_anuncio(request):
    """
    View para alterar um anúncio.

    Args:
        request (Request): Requisição HTTP contendo os dados do anúncio a ser alterado.

    Returns:
        Response: Uma resposta HTTP indicando o resultado da operação de alteração.

    Raises:
        Exception: Se ocorrer uma exceção durante o processamento.

    Examples:
        Um exemplo do formato esperado dos dados de alteração de um anuncio:

        json_alter_example = {
        "id":1, // int
        "fields":{
            "plataforma": "airbnb",
            "taxa_plataforma": "99.99"
        }
    }

    """
    try:
        # Obter os dados do anúncio a ser alterado da requisição
        filtro = request.data
        # Obter o registro do anúncio a ser alterado com base no ID fornecido
        registro = Anuncio.objects.get(id=filtro["id"])

        # Iterar sobre os campos a serem alterados
        for field in filtro["fields"].keys():
            valor_field = filtro["fields"][field]
            # Atribuir o novo valor ao campo do registro
            setattr(registro, field, valor_field)
            # Salvar as mudanças no registro
            registro.save()

        # Obter novamente o registro de anúncio alterado
        registros = Anuncio.objects.filter(id=filtro["id"])

        # Serializar o registro de anúncio alterado
        serializer = AnuncioSerializer(registros, many=True)

        # Retornar uma resposta contendo os dados serializados do anúncio alterado
        return Response(serializer.data)
    except Exception as error:
        # Se ocorrer uma exceção durante o processamento, retornar uma resposta de erro
        return Response(
            data={"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )
