from ast import literal_eval
from datetime import datetime


def valida_ids_get(model, param):
    if param:
        # Converter o parâmetro para uma lista de IDs
        param = literal_eval(param) if len(param.split(",")) > 1 else [int(param)]
        # Filtrar os registros da tabela com base nos IDs fornecidos
        registros = model.objects.filter(id__in=param)
    else:
        # Se nenhum parâmetro fornecido, obter todos os registros da tabela
        registros = model.objects.all()

    return registros


def valida_campos_obrigatorios(campos_obrigatorios, payload):
    # Convertendo as listas em conjuntos
    set_campos_obrigatorios = set(campos_obrigatorios)
    set_payload = set(payload)

    # Encontrando a diferença entre os conjuntos
    diferenca = set_campos_obrigatorios.difference(set_payload)
    return list(diferenca)


def valida_campos_validos(campos_validos, payload):
    lista_campos_invalidos = []
    for campo_payload in payload:
        if campo_payload not in campos_validos:
            lista_campos_invalidos.append(campo_payload)

    return lista_campos_invalidos


def valida_var_tipos(tipos_validos, payload):
    dict_tipo_invalido = {}
    for payload_key in payload.keys():
        if type(payload[payload_key]) != tipos_validos[payload_key]:
            dict_tipo_invalido[payload_key] = (
                f"Tipo de dado incorreto! Esperado: {tipos_validos[payload_key]}. "
            )

    return dict_tipo_invalido


def valida_data_checkin_checkout(dados_reserva):
    # Converter as strings de data em objetos de data
    datetime_checkin = datetime.strptime(
        dados_reserva["data_checkin"], "%Y-%m-%d"
    ).date()
    datetime_checkout = datetime.strptime(
        dados_reserva["data_checkout"], "%Y-%m-%d"
    ).date()

    # Verificar se a data de Check-Out é posterior à data de Check-In
    if datetime_checkout < datetime_checkin:
        return True
