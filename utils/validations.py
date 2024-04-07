from ast import literal_eval


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
