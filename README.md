# Gerenciador de Contatos Pessoais

Uma aplicação web completa para gerenciar seus contatos pessoais, construída com uma arquitetura moderna de microserviços utilizando Flask, PostgreSQL e Nginx.

![Gerenciador de Contatos](https://via.placeholder.com/800x400?text=Gerenciador+de+Contatos+Pessoais)

## 📋 Sobre o Projeto

Este projeto é um gerenciador de contatos pessoais que permite:

- Adicionar novos contatos com nome, telefone e e-mail
- Visualizar todos os seus contatos em uma lista organizada
- Pesquisar contatos pelo nome
- Editar informações de contatos existentes
- Excluir contatos

A aplicação foi desenvolvida com uma arquitetura de microserviços, separando o backend (API RESTful) do frontend (interface web), e utilizando um banco de dados PostgreSQL para armazenamento persistente.

## 🏗️ Arquitetura

O projeto segue uma arquitetura de três camadas:

1. **Frontend**: Interface de usuário construída com HTML, CSS e JavaScript puro
2. **Backend**: API RESTful desenvolvida com Flask (Python)
3. **Banco de Dados**: PostgreSQL para armazenamento persistente

### Diagrama de Arquitetura

```
┌─────────────┐       ┌─────────────┐      ┌─────────────┐
│   Frontend  │       │   Backend   │      │  Database   │
│    (Nginx)  │ ────▶│   (Flask)   │ ────▶│ (PostgreSQL)│
└─────────────┘       └─────────────┘      └─────────────┘
```

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.9**
- **Flask**: Framework web
- **Flask-SQLAlchemy**: ORM para interação com o banco de dados
- **PostgreSQL**: Banco de dados relacional
- **Gunicorn**: Servidor WSGI para produção
- **Prometheus Client**: Monitoramento e métricas

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript** (ES6+)
- **Nginx**: Servidor web e proxy reverso

### DevOps
- **Docker & Docker Compose**: Containerização e orquestração
- **GitHub Actions**: CI/CD para deploy automático

## 🔧 Requisitos

- Docker
- Docker Compose

## 📦 Instalação e Execução

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/app-personal-contact.git
   cd app-personal-contact
   ```

2. Execute a aplicação com Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

3. Acesse a aplicação:
   - Frontend: http://localhost
   - API: http://localhost/api/contacts

## 📚 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/contacts` | Lista todos os contatos |
| GET | `/api/contacts?name=termo` | Pesquisa contatos por nome |
| GET | `/api/contacts/{id}` | Obtém um contato específico |
| POST | `/api/contacts` | Cria um novo contato |
| PUT | `/api/contacts/{id}` | Atualiza um contato existente |
| DELETE | `/api/contacts/{id}` | Remove um contato |

### Exemplo de Requisição (POST)

```json
{
  "name": "João Silva",
  "phone": "11 99999-9999",
  "email": "joao@exemplo.com"
}
```

## 📊 Monitoramento

A aplicação inclui métricas do Prometheus acessíveis em:
```
http://localhost/api/metrics
```

Métricas disponíveis:
- `http_requests_total`: Total de requisições HTTP por método, endpoint e código de status
- `contacts_total`: Número total de contatos no banco de dados

## 🔒 Variáveis de Ambiente

As seguintes variáveis de ambiente podem ser configuradas no arquivo `.env`:

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| POSTGRES_DB | Nome do banco de dados | contacts_db |
| POSTGRES_USER | Usuário do PostgreSQL | myuser |
| POSTGRES_PASSWORD | Senha do PostgreSQL | mysupersecretpassword |
| DATABASE_URL | URL de conexão com o banco | postgresql://myuser:mysupersecretpassword@db:5432/contacts_db |

## 🚢 Deploy

O projeto inclui workflows do GitHub Actions para deploy automático:

- `.github/workflows/deploy-develop.yml`: Deploy para ambiente de desenvolvimento
- `.github/workflows/deploy-production.yml`: Deploy para ambiente de produção

## 🧪 Desenvolvimento

Para desenvolvimento local:

1. Inicie os containers:
   ```bash
   docker-compose up --build
   ```

2. Para parar os containers:
   ```bash
   docker-compose down
   ```

3. Para visualizar logs:
   ```bash
   docker-compose logs -f
   ```

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

Desenvolvido por [Seu Nome/Organização]

---

Feito com ❤️ e ☕
