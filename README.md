# 🌎 Mapas Culturais – Monte Carmelo

Sistema de mapeamento e gestão de agentes, espaços e eventos culturais desenvolvido para a Secretaria de Cultura de Monte Carmelo – MG.

## Funcionalidades

- Cadastro e aprovação de agentes culturais, espaços e eventos
- Visualização dos espaços em mapa interativo (Leaflet + OpenStreetMap)
- Ligação dinâmica entre lista e marcadores do mapa
- Gerenciamento de permissões por grupo (Administrador, Editor, Usuário)
- Sistema de autenticação e verificação de e-mail
- Backend em Django, API REST pronta para integração com frontend Angular

## Instalação

### Pré-requisitos

- Python 3.10+
- PostgreSQL
- [Poetry](https://python-poetry.org/) **ou** `pip` + `venv`
- [Node.js](https://nodejs.org/) (caso vá integrar com Angular no futuro)
- Git

### Configuração do ambiente

1. **Clone o repositório**

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. **Crie o ambiente virtual**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Instale as dependências**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o banco de dados**

    - Crie um banco no PostgreSQL
    - Defina variáveis no arquivo `.env` (exemplo abaixo):

    ```
    SECRET_KEY=suachavesecreta
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    DB_NAME=nome_do_banco
    DB_USER=usuario
    DB_PASS=senha
    DB_HOST=localhost
    DB_PORT=5432
    EMAIL_HOST_USER=seu@email.com
    EMAIL_HOST_PASSWORD=senha_app
    ```

5. **Rode as migrações**

    ```bash
    python manage.py migrate
    ```

6. **Crie um superusuário**

    ```bash
    python manage.py createsuperuser
    ```

7. **Execute o servidor**

    ```bash
    python manage.py runserver
    ```

8. **Acesse**

    - Painel administrativo: http://127.0.0.1:8000/admin/
    - Plataforma: http://127.0.0.1:8000/

## Organização do Projeto

- `core/` – App principal: models, views, forms, API
- `static/core/js/` – Scripts JavaScript (mapa, máscara de telefone)
- `templates/core/` – Templates Django
- `static/` – CSS, imagens e arquivos estáticos
- `manage.py` – Utilitário Django

## API

Acesse a API RESTful em:  
`/api/spaces/`, `/api/agents/`, `/api/events/`  
Utilize autenticação padrão Django ou Token se configurado.

## Contribuição

1. Fork este repositório
2. Crie sua branch: `git checkout -b minha-feature`
3. Commit suas alterações: `git commit -m 'Minha contribuição'`
4. Push para a branch: `git push origin minha-feature`
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).

---

> Desenvolvido por Arthur Araújo para a Secretaria de Cultura de Monte Carmelo – MG.