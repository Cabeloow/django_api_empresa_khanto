# Django Rest API

## Descrição

Demonstração do uso do django rest framework para a criação de 3 APIs com funções básicas de interação com um banco de dados.

## Tecnologias utilizadas

- Python 3.11.9
- Django REST Framework

## Funcionalidades

- API Imóveis: Cadastro, Consulta, Atualização e exclusão;
- API Anuncios: Cadastro, Consulta e atualização;
- API Reservas: Cadastro, Consulta e exclusão;

## Instalação

1. Clone o repositório: `https://github.com/Cabeloow/django_api_empresa_khanto.git`;
2. Na raiz do arquivo abra o cmd;
3. opcional: criar uma venv através do comando `python -m venv nome_da_venv`;
4. Instale as dependenicas necessárias com o comando `pip install -r requirements.txt`;
5. Execute o comando: `py manage.py migrate`;
6. Para popular o banco de dados use os seguintes comandos:
   - `python manage.py loaddata fixtures\imoveis_fixture.json`
   - `python manage.py loaddata fixtures\anuncio_fixture.json`
   - `python manage.py loaddata fixtures\reserva_fixture.json`
7. Execute o servidor através do comando: `py manage.py runserver`

# Uso

## API Imoveis

- Cadastro:
   - Rota: /imoveis/include_imovel/
   - Método: POST
   - payload exemplo:
        ```
        {
            "limite_hospedes": 6, // int
            "quantidade_banheiros": 2, // int
            "aceita_animais": true, // boolean
            "valor_limpeza": 10.05, // float
            "data_ativacao": "2020-12-21" // string (data no formato americano YYYY-MM-DD)
           }
- Consulta:
   - Rota: /imovel/get_imoveis
   - Método: GET
   - Exemplo consulta:
        - para retornar UM ÚNICO item específico:
            caminho_da_api.com/imoveis/get_imoveis?id=5
 
        - para retornar DOIS OU MAIS itens específicos:
            caminho_da_api.com/imoveis/get_imoveis?id=2,6,10

        - para retornar TODOS os itens:
            caminho_da_api.com/imoveis/get_imoveis


- Atualização:
   - Rota: /imovel/alter_imovel/
   - Método: POST
   - payload exemplo:
     ```
        {
            "id":1, // int (obrigatório)
            "fields":{
                "aceita_animais": false,
                "valor_limpeza": 29.99,
               }
           }
- Delete:
   - Rota: /imovel/delete_imovel/  
   - Método DELETE
   - payload exemplo:
     ```
        {
            "id":1 //int (obrigatório)
        }
## API Anuncio

- Cadastro:
   - Rota: /anuncio/include_anuncio/
   - Método: POST
   - payload exemplo:
        ```
        {
            "cod_imovel": 1, // int
            "plataforma": "airbnb", // string
            "taxa_plataforma": 99.99 // float
        }
- Consulta:
   - Rota: /anuncio/get_anuncios
   - Método: GET
   - Exemplo consulta:
        - para retornar UM ÚNICO item específico:
            caminho_da_api.com/anuncio/get_anuncios?id=5
 
        - para retornar DOIS OU MAIS itens específicos:
            caminho_da_api.com/anuncio/get_anuncios?id=2,6,10

        - para retornar TODOS os itens:
            caminho_da_api.com/anuncio/get_anuncios


- Atualização:
   - Rota: /anuncio/alter_anuncio/
   - Método: POST
   - payload exemplo:
     ```
        {
           "id":1, // int
           "fields":{
               "plataforma": "airbnb",
               "taxa_plataforma": 99.99
           }
       }
## API Reserva

- Cadastro:
   - Rota: /reserva/include_reserva/
   - Método: POST
   - payload exemplo:
        ```
        {
            "cod_anuncio": 1, // int
            "data_checkin": "2024-04-20", // string (data no formato americano YYYY-MM-DD)
            "data_checkout": "2024-04-23", // string (data no formato americano YYYY-MM-DD)
            "preco_total": 25.99, // float
            "comentario": "meu comentario", // string
            "numero_hospedes": 1 // int
        }
- Consulta:
   - Rota: /reserva/get_reservas
   - Método: GET
   - Exemplo consulta:
        - para retornar UM ÚNICO item específico:
            caminho_da_api.com/reserva/get_reservas?id=5
 
        - para retornar DOIS OU MAIS itens específicos:
            caminho_da_api.com/reserva/get_reservas?id=2,6,10

        - para retornar TODOS os itens:
            caminho_da_api.com/reserva/get_reservas

- Delete:
   - Rota: /reserva/delete_reserva/  
   - Método DELETE
   - payload exemplo:
     ```
        {
            "id":1 //int (obrigatório)
        }
## Testes

Para executar os testes, na raiz do arquivo execute os seguintes comandos no cmd:
1. para rodar os testes: `coverage run manage.py test`
2. Gerar relatório dos testes: `coverage report`
3. (opcional): Para ter um relatório em uma página web digite: `coverage html`;
   Um arquivo chamado "htmlcov" será criado na raiz do projeto, acesse-o e abra o arquivo "index.html".
   

## Contato

- Nome: João Pedro Guimarães da Silva
- E-mail: jpguimaraes27@hotmail.com
- Celular: 19 99300-7616
- LinkedIn: https://www.linkedin.com/in/jo%C3%A3o-pedro-guimar%C3%A3es-silva-b10ab3186/

