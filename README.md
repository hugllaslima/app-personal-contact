# Gerenciador de Contatos Pessoais

Uma aplicação web completa para gerenciar seus contatos pessoais, construída com uma arquitetura moderna de microserviços utilizando Flask, PostgreSQL e Nginx.

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
┌─────────────┐        ┌─────────────┐        ┌──────────────┐
│  Frontend   │        │   Backend   │        │   Database   │
│  (Nginx)    │ ────▶  │   (Flask)   │  ────▶ │ (PostgreSQL) │
└─────────────┘        └─────────────┘        └──────────────┘
```

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.9**
- **Flask**: Framework web
- **Flask-SQLAlchemy**: ORM para interação com o banco de dados
- **PostgreSQL**: Banco de dados relacional
- **Gunicorn**: Servidor WSGI para produção
- **Prometheus Client**: Monitoramento e métricas
- **Flask-JWT-Extended**: Autenticação e autorização via tokens JWT

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript** (ES6+)
- **Nginx**: Servidor web e proxy reverso

### DevOps
- **Docker & Docker Compose**: Containerização e orquestração
- **GitHub Actions**: CI/CD para deploy automático
- **AWS**: Infraestrutura em nuvem para produção
 

## 🔧 Requisitos

- Docker
- Docker Compose
- Git
- Acesso à AWS (para deploy em produção)

## 📦 Instalação e Execução

### Configuração Inicial

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/app-personal-contact.git
   cd app-personal-contact
   ```

### ⚙️ Configuração do Frontend com Nginx (configuração fixa)

O frontend usa um `nginx.conf` fixo copiado para `/etc/nginx/conf.d/default.conf` (sem templates em `/etc/nginx/templates` e sem `envsubst`). O proxy reverso do Nginx aponta para `http://app:5000` dentro da rede do Compose, roteando:

- `location /api/` → `http://app:5000/`
- `location /health` → `http://app:5000/health`
- `location /metrics` → `http://app:5000/metrics`

Arquivo de configuração: `frontend/nginx.conf` (copiado pelo `Dockerfile` para o container).

Exemplo com `docker run` direto (sem variáveis de ambiente):

```bash
docker run -d --name contacts-frontend \
  -p 80:80 \
  ghcr.io/hugllaslima/contacts-frontend:latest
```

No Docker Compose, o serviço `frontend` já está configurado para comunicar-se com o serviço `app` na porta `5000`.

2. Crie um arquivo `.env` baseado no `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Configure as variáveis de ambiente no arquivo `.env` (veja a seção "Variáveis de Ambiente")

### Execução Local com Docker

1. Execute a aplicação com Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

2. Acesse a aplicação:
   - Frontend: http://localhost
   - API: http://localhost/api/contacts

### Verificação da Instalação

Para verificar se todos os serviços estão funcionando corretamente:

```bash
docker-compose ps
```

## 🔒 Variáveis de Ambiente

A aplicação utiliza variáveis de ambiente para configuração. Crie um arquivo `.env` baseado no `.env.example` fornecido.

### Variáveis Essenciais

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| POSTGRES_DB | Nome do banco de dados | contacts_db |
| POSTGRES_USER | Usuário do PostgreSQL | app_user |
| POSTGRES_PASSWORD | Senha do PostgreSQL | *****secure_password***** |
| DATABASE_URL | URL de conexão com o banco | postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB} |
| JWT_SECRET | Chave para assinatura de tokens JWT | *****chave_secreta_gerada***** |
| FLASK_ENV | Ambiente de execução (development/production) | production |
| FLASK_DEBUG | Modo debug (0/1) | 0 |

### Variáveis para CI/CD e Deploy

#### Ambiente de Desenvolvimento (Proxmox VE)

| Variável | Descrição | Uso |
|----------|-----------|-----|
| PAT_TOKEN_DEV | Token de acesso pessoal para desenvolvimento | GitHub Secrets |
| BACKEND_PORT_DEV | Porta do backend em desenvolvimento | GitHub Secrets |
| POSTGRES_USER_DEV | Usuário do PostgreSQL para desenvolvimento | GitHub Secrets |
| POSTGRES_PASSWORD_DEV | Senha do PostgreSQL para desenvolvimento | GitHub Secrets |
| POSTGRES_DB_DEV | Nome do banco de dados para desenvolvimento | GitHub Secrets |
| JWT_SECRET_DEV | Chave JWT para desenvolvimento | GitHub Secrets |
| JWT_EXPIRES_IN_DEV | Tempo de expiração do JWT em desenvolvimento | GitHub Secrets |

#### Ambiente de Produção (AWS)

| Variável | Descrição | Uso |
|----------|-----------|-----|
| PAT_TOKEN_PROD | Token de acesso pessoal para produção | GitHub Secrets |
| AWS_ACCESS_KEY_ID_PROD | Chave de acesso AWS para produção | GitHub Secrets |
| AWS_SECRET_ACCESS_KEY_PROD | Chave secreta AWS para produção | GitHub Secrets |
| AWS_REGION_PROD | Região AWS para produção | GitHub Secrets |
| ECR_REPOSITORY_BACKEND_PROD | Repositório ECR para backend em produção | GitHub Secrets |
| ECR_REPOSITORY_FRONTEND_PROD | Repositório ECR para frontend em produção | GitHub Secrets |
| EC2_HOST_PROD | Host EC2 para produção | GitHub Secrets |
| BACKEND_PORT_PROD | Porta do backend em produção | GitHub Secrets |
| POSTGRES_USER_PROD | Usuário do PostgreSQL para produção | GitHub Secrets |
| POSTGRES_PASSWORD_PROD | Senha do PostgreSQL para produção | GitHub Secrets |
| POSTGRES_DB_PROD | Nome do banco de dados para produção | GitHub Secrets |
| JWT_SECRET_PROD | Chave JWT para produção | GitHub Secrets |
| JWT_EXPIRES_IN_PROD | Tempo de expiração do JWT em produção | GitHub Secrets |

### Geração de Chaves Seguras

O JWT_SECRET é uma chave crítica para segurança. Gere valores fortes usando:

**Método 1: Com OpenSSL (Linux/macOS)**
```bash
openssl rand -hex 64
```

**Método 2: Com Python**
```bash
python3 -c "import secrets; print(secrets.token_hex(64))"
```

## 📚 API Endpoints

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/contacts` | Lista todos os contatos | Requerida |
| GET | `/api/contacts?name=termo` | Pesquisa contatos por nome | Requerida |
| GET | `/api/contacts/{id}` | Obtém um contato específico | Requerida |
| POST | `/api/contacts` | Cria um novo contato | Requerida |
| PUT | `/api/contacts/{id}` | Atualiza um contato existente | Requerida |
| DELETE | `/api/contacts/{id}` | Remove um contato | Requerida |
| POST | `/api/auth/login` | Autenticação de usuário | Não requerida |
| POST | `/api/auth/register` | Registro de novo usuário | Não requerida |

### Exemplo de Requisição (POST)

```json
{
  "name": "João Silva",
  "phone": "11 99999-9999",
  "email": "joao@exemplo.com"
}
```

### Autenticação

A API utiliza autenticação JWT. Para acessar endpoints protegidos:

1. Obtenha um token via `/api/auth/login`
2. Inclua o token no header de requisições:
   ```
   Authorization: Bearer seu_token_jwt
   ```

## 📊 Monitoramento

A aplicação inclui métricas do Prometheus acessíveis em:
```
http://localhost/api/metrics
```

Métricas disponíveis:
- `http_requests_total`: Total de requisições HTTP por método, endpoint e código de status
- `contacts_total`: Número total de contatos no banco de dados
- `http_request_duration_seconds`: Tempo de resposta das requisições
- `http_request_exceptions_total`: Total de exceções ocorridas

## 🚢 CI/CD e Deploy

O projeto utiliza GitHub Actions para integração contínua e deploy automático.

### Workflows Disponíveis

- **deploy-develop.yml**: Deploy para ambiente de desenvolvimento
  - Gatilho: Push para branch `develop`
  - Infraestrutura: VM no Proxmox VE
  - Ações: Testes, build de imagens Docker, deploy para ambiente de desenvolvimento

- **deploy-production.yml**: Deploy para ambiente de produção
  - Gatilhos: Pull Request para branch `main` (validações) e Push para branch `main` (deploy)
  - Infraestrutura: AWS (ECR + EC2)
  - Ações: Testes, build de imagens Docker, deploy para AWS

### Fluxo de Aprovação e Deploy (produção)

- Ao abrir um Pull Request para `main`, o pipeline executa apenas validações (build e testes). As etapas sensíveis que utilizam secrets da AWS (configurar credenciais, login no ECR, build/push das imagens e deploy na EC2) ficam condicionadas a `if: github.event_name == 'push'` e não executam em `pull_request`.
- Após aprovação pelo tech lead e merge do PR, o evento `push` para `main` dispara o deploy completo: configuração de credenciais AWS, login no ECR, build e push das imagens `contacts-backend` e `contacts-frontend` com tag `latest`, e execução do deploy na instância EC2.
- Recomenda-se proteger a branch `main` no GitHub (Branch protection rules) exigindo Pull Requests e aprovações antes do merge.

### Configuração para Deploy

Para configurar o deploy automático:

1. Configure os secrets necessários no GitHub para **desenvolvimento**:
   - PAT_TOKEN_DEV
   - BACKEND_PORT_DEV
   - POSTGRES_USER_DEV
   - POSTGRES_PASSWORD_DEV
   - POSTGRES_DB_DEV
   - JWT_SECRET_DEV
   - JWT_EXPIRES_IN_DEV

2. Configure os secrets necessários no GitHub para **produção**:
   - PAT_TOKEN_PROD
   - AWS_ACCESS_KEY_ID_PROD
   - AWS_SECRET_ACCESS_KEY_PROD
   - AWS_REGION_PROD
   - ECR_REPOSITORY_BACKEND_PROD
   - ECR_REPOSITORY_FRONTEND_PROD
   - EC2_HOST_PROD
   - BACKEND_PORT_PROD
   - POSTGRES_USER_PROD
   - POSTGRES_PASSWORD_PROD
   - POSTGRES_DB_PROD
   - JWT_SECRET_PROD
   - JWT_EXPIRES_IN_PROD

3. Certifique-se de que as permissões AWS estão corretamente configuradas

4. Proteja a branch `main` com regras de proteção (Settings → Branches → Branch protection rules):
   - `Require a pull request before merging`
   - `Require approvals` (ex.: aprovação por tech lead)
   - Opcional: bloquear commits diretos na `main`

 

## 🛡️ Segurança

### Boas Práticas Implementadas

1. **Variáveis de Ambiente**: Todas as credenciais e configurações sensíveis são armazenadas em variáveis de ambiente
2. **Autenticação JWT**: Proteção de endpoints com tokens JWT
3. **HTTPS**: Configuração de HTTPS em produção
4. **Sanitização de Inputs**: Validação e sanitização de todas as entradas de usuário
5. **Logs Seguros**: Logs estruturados sem informações sensíveis

### Recomendações para Produção

1. Configure um domínio personalizado com certificado SSL
2. Implemente rate limiting para prevenir ataques de força bruta
3. Configure backups automáticos do banco de dados
4. Monitore logs e métricas regularmente

## 🧪 Desenvolvimento

### Ambiente Local

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

### Testes

Execute os testes automatizados:

```bash
docker-compose exec backend pytest
```

### Fluxo de Trabalho Git

1. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```

2. Faça commits seguindo o padrão Conventional Commits:
   ```bash
   git commit -m "feat: adiciona nova funcionalidade"
   ```

3. Envie para o repositório remoto:
   ```bash
   git push origin feature/nome-da-feature
   ```

4. Crie um Pull Request para a branch `develop`

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

Por favor, certifique-se de atualizar os testes conforme apropriado e seguir o código de conduta do projeto.

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

Desenvolvido por Hugllas Lima

---

Feito com ❤️ e ☕
