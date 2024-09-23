# API Django Rest Framework para Gerenciamento de Pessoas

  

Esta API foi desenvolvida para lidar com o upload e exportação de arquivos Excel contendo dados de pessoas. A API oferece endpoints para fazer upload de arquivos e para exportar dados em formato de planilha Excel.

  

## Endpoints

  

### 1. Upload de Arquivos Excel

  

-  **Endpoint:**  `/upload-excel/`

-  **Método:**  `POST`

-  **Descrição:** Este endpoint é utilizado para fazer upload de arquivos Excel contendo dados de pessoas. O arquivo é validado e os dados são processados para armazenamento no banco de dados.

  

**Requisição:**

  

POST /upload-excel/ HTTP/1.1

Host: example.com

Content-Type: multipart/form-data

  

--boundary

Content-Disposition: form-data; name="file"; filename="pessoas.xlsx"

Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

  

[Arquivo Excel]

--boundary--

  

**Resposta:**

  

-  **Status 200 OK:** Se os dados forem válidos e processados com sucesso.

-  **Status 400 Bad Request:** Se houver erros na validação dos dados.

  

**Exemplo de Resposta Sucesso:**

  

```json

{

"pessoas_ativas": [

{

"Nome":  "João da Silva",

"Email":  "joao@example.com",

"Data de nascimento":  "1990-01-01",

"Valor":  "R$ 150.00"

}

]

}

```

## Exportação de Dados em Planilha Excel

  

-  **Endpoint:**  `/download-planilha/`

-  **Método:**  `GET`

-  **Descrição:** Este endpoint gera e retorna um arquivo Excel contendo as informações de todas as pessoas ativas no banco de dados em um link base64.

  

### Resposta

  

-  **Status 200 OK:** Retorna um link base64 para download do arquivo Excel.

  

### Exemplo de Resposta

  

```json

{

"download_link":  "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,UEsDBBQAAAAI..."

}

```

  

## Implementação

  

### `views.py`

  

Define as views para upload e exportação de arquivos Excel.

  

-  **PessoaUploadView:** Processa o upload de arquivos Excel e valida os dados.

-  **PessoaExportView:** Gera um arquivo Excel com as informações das pessoas ativas e retorna um link base64.

  

### `serializers.py`

  

Define os serializers para upload e exportação de dados.

  

-  **ExcelUploadSerializer:** Valida e processa o arquivo Excel carregado.

-  **ExcelExportSerializer:** Gera uma planilha Excel contendo as informações das pessoas ativas e retorna um link base64.

  

### `models.py`

  

Define o modelo `Pessoa` que armazena informações sobre as pessoas, incluindo nome, e-mail, data de nascimento, valor associado e status de atividade.

  

## Uso de Base64 para Exportação

  

O uso de Base64 para a exportação de arquivos Excel oferece as seguintes vantagens em comparação com o método de attachment:

  

-  **Facilidade de Integração:** Base64 permite a inclusão do arquivo diretamente em uma resposta JSON, facilitando a integração com front-ends que podem manipular strings base64 facilmente.

  

-  **Sem Necessidade de Armazenamento Temporário:** Não é necessário criar arquivos temporários no servidor para fazer o download, o que pode reduzir a carga sobre o servidor e simplificar o gerenciamento de arquivos.

  

-  **Simples de Implementar:** O uso de Base64 pode simplificar a lógica de geração e envio de arquivos, evitando a necessidade de configurar cabeçalhos de resposta específicos para arquivos.

  

No entanto, é importante considerar que o Base64 pode aumentar o tamanho dos dados em comparação com o arquivo binário original, o que pode impactar a performance e o consumo de largura de banda, especialmente para arquivos grandes.

  

## Teste Unitarios

Os testes unitários para a view `PessoaUploadView`, que lida com o upload de arquivos Excel contendo informações de pessoas. Os testes foram implementados usando `APITestCase` do Django REST Framework e validam tanto uploads válidos quanto inválidos.

podem encontrar os teste no arquivo tests,py no app pessoa, que conforme imagem abaixo foi realizado com sucesso

  

![Imagem do teste unitário](tests/teste.jpeg)

  

Além disso, realizamos testes utilizando a biblioteca requests para verificar a funcionalidade da API de maneira mais abrangente.

  

![Imagem do request no post](tests/testerequest.png)

![Imagem do request no get](tests/responseget.png)

  

## Clonando o Repositório e rodando o projeto

  

Primeiro, clone o repositório do GitHub para o seu ambiente local:

  

```bash

git  clone  https://github.com/brunodealmeida17/apipecege

cd  seurepositorio

```

  

## Instalando as Dependências

  

Certifique-se de estar usando um ambiente virtual para gerenciar as dependências. Se você não tiver um ambiente virtual, crie um e ative-o:

  

```bash

python  -m  venv  venv

source  venv/bin/activate

```

  

No Windows, use:

```

virtualenv venv

venv\Scripts\activate

```

  

Instale as dependências do projeto usando o pip:

```

pip install -r requirements.txt

```

## Configurando o Arquivo .env

Crie um arquivo .env na raiz do seu projeto (onde está o manage.py). Adicione o seguinte conteúdo ao arquivo .env, substituindo os valores conforme necessário:  
  ```
SECRET_KEY='
DEBUG=1  adicionar qualquer caracteres para sair do modo debug=True

## Super-User Credentials
SUPER_USER_NAME  =  'root'
SUPER_USER_PASSWORD  =  'root'
SUPER_USER_EMAIL  =  'admin@email.com'  

## Databases
DATABASE_ROOT_PASSWORD=senha_do_banco_root
DATABASE_DB=gerenciarpessoa
DATABASE_USER=usuario_do_banco
DATABASE_PASSWORD=senha_do_banco
```
Certifique-se de que o banco de dados está corretamente configurado e acessível com as credenciais fornecidas.

## Estrutura do Projeto

    gerenciamentoPessoa/	    
	    ├── gerenciamentoPessoa/
			├── nome_do_projeto/
			    ├── __init__.py 
			    ├── asgi.py 
			    ├── settings.py 
			    ├── urls.py 
			    └── wsgi.py
		    ├── pessoas/
			    ├── migrations/
				    ├── __init__.py 
					├──  0001_initial,py
			    ├── __init__.py 
			    ├── admin.py 
			    ├── apps.py 
			    ├── models.py
			    ├── serializers.py
			    ├── tests.py
			    ├── urls.py 
			    └── views.py
		     ├── tests/
			    ├── apps.py 
			    ├── apps.py 
		    ├── manage.py
	    ├── nginx/
		    ├── default.conf
		    ├── Dockerfile
		├── .env
		├── .gitignore
		├── docker-compose.yml
		├── dockerfile
		├── README.md		    
	    └── venv/ (se estiver usando um ambiente virtual)

## Executando o Projeto

  

pós configurar o arquivo .env e instalar todas as dependências necessárias, você pode iniciar o servidor de desenvolvimento do Django com o seguinte comando:

  

```

python manage.py runserver

```

  

O servidor estará acessível em http://127.0.0.1:8000/.

  
  

## Conclusão

  

Esta API oferece uma maneira eficiente de carregar e exportar dados de pessoas usando arquivos Excel. O uso de Base64 para exportação simplifica a implementação e a integração, tornando-a uma solução prática para muitas situações