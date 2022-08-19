# Silver Chainsaw [![build](https://github.com/CapybaHub/django-base/actions/workflows/main.yml/badge.svg?branch=deploy)](https://github.com/CapybaHub/django-base/actions/workflows/main.yml) [![codecov](https://codecov.io/gh/CapybaHub/django-base/branch/master/graph/badge.svg?token=70KG8Y2535)](https://codecov.io/gh/CapybaHub/django-base)

A RESTful API built with Django framework.

## Como rodar

Se for a primeira vez:
```bash
make setup_install
```

Depois, apenas:
```bash
make up
```

### Opcional

Criar ambiente virtual:
```bash
make setup_venv
```

Rodar seed do banco:
```bash
make seed
```

## Documentação da API

### Interface gráfica

Usamos a Swagger UI, para exibir a documentação, em formato OpenAPI, numa interface gráfica no navegador. Para rodar localmente apenas o container da documentação, seguir os passos:

1. Rodar `docker-compose up swagger-ui`
2. Acessar *localhost:8080*

### Incrementando a documentação

O arquivo *docs/openapi.json* descreve a API utilizando a especificação OpenAPI. Ele deve ser editado manualmente ao longo do tempo de vida do projeto para deixar a documentação em conformidade com a API. Uma ferramenta que pode acelerar este processo é o comando *genarateschema* do Django REST Framework. Ele pode ser usado para gerar a documentação automática do projeto baseada nas views existentes. No entanto, deve-se ter cuidado pra não sobrescrever o arquivo original *openapi.json*. Para utilizar a ferramenta, seguir o tutorial:

1. Rodar o comando `make generate_schema` para criar o arquivo **docs/temp-schema.json**.
2. Identificar no arquivo gerado a parte desejada (exemplo: alguma *view* nova) e mover para **docs/openapi.json**.
3. Excluir o arquivo **docs/temp-schema.json**.

## Testes unitários

Utilizamos a biblioteca **pytest** para rodar testes unitários. Seu arquivo de configuração é *pytest.ini*.

- Para rodas os testes, usar o comando `make test`.

Como por padrão os testes reutilizam o banco de dados gerado, caso tenha novas migrações é necessário re-criar o banco.

- Para re-criar o banco, utilizar o comando `pytest --create-db`.

### Cobertura de teste

- `make coverage`

ou

- `make coverage_html`, para um relatório HTML.

## Arquitetura

- `apps`: aqui devem estar todas as django apps locais que devem ser criadas ao longo do desenvolvimento do projeto. No projeto base esta pasta conterá apenas a app `user` (e a `tenant`, se for um projeto tenant-based). Para criar uma nova app, deve-se usar o comando *make startapp* na raiz do projeto para criá-la no lugar correto e seguindo o template do projeto base.
- `conf`: módulo que contém arquivos de configuração do projeto.
    - `app_template`: template usado para criação de novas apps. Geralmente, não deve ser alterado.
    - `settings`: pasta com os arquivos settings do django. É modularizado de forma a possuir um arquivo de settings para cada ambiente: local, production, etc.
    - `urls.py`: arquivo de urls do projeto. É preferível deixar apenas incluir as urls das outras apps, deixando a configuração específica de cada módulo em seu próprio arquivo urls.py.
    - `wsgi.py`: arquivo wsgi padrão do Django para deploy.
- `docs`: módulo que contém arquivos relacionados à documentação do projeto.
    - `openapi.json`: arquivo contendo schema da API REST. É usado no container *swagger-ui*.
- `lib`: módulo que contém as classes que devem ser compartilhada por todo o projeto, como por exemplo um model base, uma view genérica, etc.
    - `models.py`: contém models base para o projeto que automaticamente incluem campos de timestamp (created_at ou updated_at) ou safe delete feature.
- `requirements`: contém as dependências do projeto, separadas por ambiente (local, production, etc.).
- `scripts`: contém shell scripts úteis para o projeto.
- `env.example`: arquivo env de exemplo para iniciar o projeto. Deve ser copiado para um arquivo `.env` (não versionado).
- `docker-compose.yml` e `Dockerfile`: arquivos de configuração Docker.
- `Makefile`: contém comandos úteis, como por exemplo entrar num container ou criar uma app.

## Comandos úteis

### Criar uma app

`make startapp [app_name]`

### Entrar em um container

`make enter [service_name]`

### Abrir o django shell

`make shell`

### Resetar o banco de dados

`make reset_db`

### Atualizar traduções do inglês

`make compilemessages`
