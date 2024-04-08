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


## Instalação

1. Clone o repositório: `https://github.com/Cabeloow/django_api_empresa_khanto.git`;
2. Na raiz do arquivo abra o cmd;
3. opcional: criar uma venv através do comando "python -m venv nome_da_venv";
4. Instale as dependenicas necessárias com o comando "pip install -r requirements.txt";
5. Execute o comando: py manage.py migrate;
6. Para popular o banco de dados use os seguintes comandos:
   python manage.py loaddata fixtures\imoveis_fixture.json
   python manage.py loaddata fixtures\anuncio_fixture.json
   python manage.py loaddata fixtures\reserva_fixture.json
7. Execute o servidor através do comando: py manage.py runserver

## Uso

#API Imoveis

- Cadastro:
   - Rota: /imoveis/include_imovel/
   - Método: POST
   - payload exemplo:
        {
            "limite_hospedes": 6, // int
            "quantidade_banheiros": 2, // int
            "aceita_animais": true, // boolean
            "valor_limpeza": 10.05, // float
            "data_ativacao": "2020-12-21" // string (data no formato americano YYYY-MM-DD)
        }


- Consulta:
   - Rota: /imoveis/get_imoveis
   - Método: GET
   - Exemplo consulta:
        - para retornar UM ÚNICO item específico:
            caminho_da_api.com/imoveis/get_imoveis?id=5
 
        - para retornar DOIS OU MAIS itens específicos:
            caminho_da_api.com/imoveis/get_imoveis?id=2,6,10

        - para retornar TODOS os itens:
            caminho_da_api.com/imoveis/get_imoveis


- Atualização:
   - Rota: /imoveis/alter_imovel/
   - Método: POST
   - payload exemplo:
        {
            "id":1, // int (obrigatório)
            "fields":{
                "aceita_animais": false,
                "valor_limpeza": 29.99,

            }
        }

- Delete:
   - Rota: /imoveis/delete_imovel/  
   - Método DELETE
   - payload exemplo:
        {
            "id":1 //int (obrigatório)
        }

## Testes

- Para executar os testes, na raiz do arquivo execute os seguintes comandos no cmd:
1. para rodar os testes: coverage run manage.py test
2. Gerar relatório dos testes: coverage report
3. (opcional): Para ter um relatório em uma página web digite: coverage html;
   Um arquivo chamado "htmlcov" será criado na raiz do projeto, acesse-o e abra o arquivo "index.html".


## Contato

- Nome: João Pedro Guimarães da Silva
- E-mail: jpguimaraes27@hotmail.com
- Celular: 19 99300-7616
- LinkedIn: https://www.linkedin.com/in/jo%C3%A3o-pedro-guimar%C3%A3es-silva-b10ab3186/

