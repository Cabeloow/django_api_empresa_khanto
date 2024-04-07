from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from utils.validations import valida_ids_get
from .serializer import ReservaSerializer
from base.models import Reserva
from datetime import datetime


@api_view(["POST"])
def add_reserva(request):
    """
    View para adicionar uma reserva.

    Args:
        request (Request): Requisição HTTP contendo os dados da reserva a ser adicionada.

    Returns:
        Response: Uma resposta HTTP indicando o resultado da operação.

    Raises:
        Exception: Se ocorrer algum erro durante o processamento da reserva.

    Examples:
        Um exemplo do formato esperado dos dados de reserva:

        Reserva_json_example = {
            "cod_anuncio": 1, // int
            "data_checkin": "2024-04-20", // string (data no formato americano YYYY-MM-DD)
            "data_checkout": "2024-04-23", // string (data no formato americano YYYY-MM-DD)
            "preco_total": 25.99, // float
            "comentario": "meu comentario", // string
            "numero_hospedes": 1 // int
        }
    """
    try:
        # Recuperar os dados da reserva da requisição
        dados_reserva = request.data

        # Converter as strings de data em objetos de data
        datetime_checkin = datetime.strptime(
            dados_reserva["data_checkin"], "%Y-%m-%d"
        ).date()
        datetime_checkout = datetime.strptime(
            dados_reserva["data_checkout"], "%Y-%m-%d"
        ).date()

        # Verificar se a data de Check-Out é posterior à data de Check-In
        if datetime_checkout < datetime_checkin:
            return Response(
                data={
                    "error": "A data de Check-Out não pode ser inferior a data de Check-In"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validar os dados da reserva usando o serializer
        serializer = ReservaSerializer(data=dados_reserva)
        if serializer.is_valid():
            # Se os dados forem válidos, salvar a reserva
            serializer.save()
        else:
            # Se os dados forem inválidos, retornar uma resposta de erro
            return Response(
                data={"error": "Opa, algo deu errado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retornar uma resposta de sucesso
        return Response(
            data={"message": "Reserva concluída com sucesso!"},
            status=status.HTTP_200_OK,
        )
    except Exception as error:
        # Se ocorrer uma exceção durante o processamento, retornar uma resposta de erro
        return Response(
            data={"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def get_reservas(request):
    """
    View para obter reservas.

    Args:
        request (Request): Requisição HTTP contendo os parâmetros de filtragem.

    Returns:
        Response: Uma resposta HTTP contendo os registros de reserva.

    Raises:
        Exception: Se ocorrer algum erro durante a obtenção dos registros.

    """
    try:
        # Obter o parâmetro de consulta "id" da requisição
        param = request.query_params.get("id", None)

        registros = valida_ids_get(Reserva, param)

        # Serializar os registros de reserva
        serializer = ReservaSerializer(registros, many=True)

        # Retornar uma resposta contendo os dados serializados
        return Response(serializer.data)
    except Exception as error:
        # Se ocorrer um erro, retornar uma resposta de erro
        return Response(
            data={"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["DELETE"])
def del_reserva(request):
    """
    View para deletar uma reserva.

    Args:
        request (Request): Requisição HTTP contendo os dados da reserva a ser deletada.

    Returns:
        Response: Uma resposta HTTP indicando o resultado da operação de deleção.

    Raises:
        KeyError: Se o campo "id" não estiver presente nos dados da requisição.

    Examples:
        Um exemplo do formato esperado dos dados de delete reserva:

        del_reserva_json_example = {
            "id":1 int
        }

    """
    try:
        # Obter o ID da reserva a ser deletada dos dados da requisição
        filtro = request.data
        # Filtrar o registro de reserva com base no ID fornecido
        registro = Reserva.objects.filter(id=filtro["id"])
        if not registro:
            return Response(
                data={"error": f"id da reserva não encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Deletar o registro de reserva
        result = registro.delete()
        # Retornar uma resposta indicando o resultado da operação de deleção
        return Response(result)
    except KeyError as error:
        # Se o campo "id" não estiver presente nos dados da requisição, retornar uma resposta de erro
        return Response(
            data={"error": error},
            status=status.HTTP_400_BAD_REQUEST,
        )
