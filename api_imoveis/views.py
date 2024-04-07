from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils.validations import *
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
        dict_campos_obrigatorios = {
            "limite_hospedes": int,
            "quantidade_banheiros": int,
            "aceita_animais": bool,
            "valor_limpeza": float,
            "data_ativacao": str,
        }
        campos_faltantes = valida_campos_obrigatorios(
            dict_campos_obrigatorios.keys(), request.data.keys()
        )
        if campos_faltantes:
            # Se os dados forem inválidos, retornar uma resposta de erro
            return Response(
                data={
                    "error": f"Os campos a seguir são obrigatórios e não foram preenchidos.\
                    {str(list(campos_faltantes))[1:][:-1]}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        tipos_incorretos = valida_var_tipos(dict_campos_obrigatorios, request.data)
        if tipos_incorretos:
            return Response(
                data={"error": tipos_incorretos},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        if param == None and not registros:
            return Response(
                data={"error": "Opa! Não há nenhum registro de imoveis salvo."},
                status=status.HTTP_404_NOT_FOUND,
            )
        elif param != None and not registros:
            return Response(
                data={"error": "Opa! Não há nenhum registro de imoveis com esse ID."},
                status=status.HTTP_404_NOT_FOUND,
            )
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
            "id":1 //int
        }

    """
    try:
        # Obter o ID do imóvel a ser deletado dos dados da requisição
        filtro = request.data
        if "id" not in filtro.keys():
            return Response(
                data={"error": "O campo id é obrigatório para essa operação."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Filtrar o registro de imóvel com base no ID fornecido
        registro = Imovel.objects.filter(id=filtro["id"])

        if not registro:
            return Response(
                data={"error": "id do imóvel não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
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
        if "id" not in filtro.keys():
            return Response(
                data={"error": "O campo id é obrigatório para essa operação."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Obter o registro do imóvel a ser alterado com base no ID fornecido
        registro = Imovel.objects.get(id=filtro["id"])

        dict_campos_validos = {
            "limite_hospedes": int,
            "quantidade_banheiros": int,
            "aceita_animais": bool,
            "valor_limpeza": float,
            "data_ativacao": str,
        }

        # valida há campos invalidos no payload
        campos_invalidos_imovel = valida_campos_validos(
            dict_campos_validos.keys(), filtro["fields"].keys()
        )

        if campos_invalidos_imovel:
            return Response(
                data={
                    "error": f"Registro não atualizado! Os campos a seguir não existem na tabela Imovel: {str(list(campos_invalidos_imovel))[1:][:-1]}. Campos permitidos: {str(list(dict_campos_validos))[1:][:-1]}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # valida o tipo dos valores para cada campo, buscando tipos invalidos
        tipos_incorretos = valida_var_tipos(dict_campos_validos, request.data["fields"])
        if tipos_incorretos:
            return Response(
                data={"error": tipos_incorretos},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
