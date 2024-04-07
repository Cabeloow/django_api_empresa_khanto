# Django Rest API

## Descrição

Demonstração do uso do django rest framework para a criação de 3 APIs com funções básicas de interação com um banco de dados.

## Funcionalidades

- Cadastro, Consulta, Atualização e exclusão de Imóveis
- Cadastro, Consulta e Atualização de Anuncios
- Cadastro, Consulta, e exclusão de Reservas

## Estrutura do banco de dados
TODO


## Tecnologias utilizadas

- Python 3.11.9
- Django REST Framework
- 

## Instalação

1. Clone o repositório: `https://github.com/Cabeloow/django_api_empresa_khanto.git`
2. Na raiz do arquivo abra o cmd
3. opcional: criar uma venv através do comando "python -m venv nome_da_venv"
4. Instale as dependenicas necessárias com o comando "pip install -r requirements.txt"
5. Para popular o banco de dados use os seguintes comandos:
   python manage.py loaddata fixtures\imoveis_fixture.json
   python manage.py loaddata fixtures\anuncio_fixture.json
   python manage.py loaddata fixtures\reserva_fixture.json
6. Execute o servidor através do comando: py manage.py runserver

## Uso

Rotas e payloads;

- Cadastro: 
    - Método POST
    - payload exemplo:
        {"cpf": "99988877700", 
        "dados_pessoa":{"nome":  "jp", "sobrenome": "silva", "idade": "20", "pais": "brasil"}}


- Consulta: 
    - Método GET
    - Exemplo consulta:
        para retornar um item específico:
            caminho_da_api.com/desafio/consulta?cpf=99988877700

        para retornar todos os itens:
            caminho_da_api.com/desafio/consulta


- Atualiza: 
    - Método PATCH
    - payload exemplo:
        {"cpf":"99988877700", 
        "update_itens":{"nome":  "jp", "idade": "3"}}

- Delete: 
    - Método DELETE
    - payload exemplo:
        {"cpf": "99988877700"}

## Testes

- Para executar os testes, na raiz do arquivo 
1. import a biblioteca pytest
1. Acesse a pasta "tests"
2. Execute o comando python -m pytest test_backend.py -v

- Para executar o teste de cobertura.
1. import a biblioteca coverage
1. Acesse a pasta "tests"
2. Execute os seguintes comandos:
    - python -m coverage run meu_teste.py
    - python -m coverage report -m
    - python -m coverage html
3. em seguida acesse o arquivo tests\htmlcov\index.html

## Contato

- Nome: João Pedro Guimarães da Silva
- E-mail: jpguimaraes27@hotmail.com
- Celular: 19 99300-7616
- LinkedIn: https://www.linkedin.com/in/jo%C3%A3o-pedro-guimar%C3%A3es-silva-b10ab3186/

