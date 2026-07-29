# 📱 WhatsApp Message Scheduler

Sistema de **agendamento e envio de mensagens via WhatsApp**, construído com **Domain-Driven Design (DDD)** e **Clean Architecture**, integrado a uma API REST moderna com **Django Ninja** e processamento assíncrono via **Celery**.

![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)
![Django](https://img.shields.io/badge/django-%E2%89%A56.0.7-092E20)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

---

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura](#-arquitetura)
- [Stack Tecnológico](#-stack-tecnológico)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Entidades do Domínio](#-entidades-do-domínio)
- [Casos de Uso](#-casos-de-uso)
- [Endpoints da API](#-endpoints-da-api)
- [Banco de Dados](#-banco-de-dados)
- [Autenticação](#-autenticação)
- [Tarefas Assíncronas (Celery)](#-tarefas-assíncronas-celery)
- [Injeção de Dependências](#-injeção-de-dependências)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Roadmap](#-roadmap)

---

## 🎯 Sobre o Projeto

A ideia central do **WhatsApp Message Scheduler** é simples: permitir que uma mensagem seja escrita hoje e entregue no momento certo, sem depender de alguém abrir o WhatsApp e apertar "enviar" na hora exata. O sistema funciona como um **carteiro assíncrono** — o usuário conecta seu próprio número de WhatsApp à plataforma (via QR code ou código de verificação, através da **Waha API**), agenda uma mensagem para um número e um horário, e o próprio sistema se encarrega de disparar o envio no momento programado, sem intervenção manual.

Por trás dessa proposta simples existe uma preocupação maior: que o núcleo do negócio — *o que é um usuário*, *o que é uma mensagem agendada*, *quando ela deve ser enviada* — não dependa de detalhes técnicos como framework web, banco de dados ou provedor de WhatsApp. Por isso o projeto é construído sobre **DDD** e **Clean Architecture**: as regras de agendamento e envio vivem isoladas no domínio, enquanto Django, PostgreSQL, Redis e a Waha API entram apenas como peças de infraestrutura, substituíveis sem afetar a lógica de negócio.

Na prática, o sistema resolve três problemas:

1. **Identidade e conexão** — cada usuário tem uma conta própria e uma sessão de WhatsApp associada, que precisa ser autenticada (QR code ou código) antes de poder enviar mensagens.
2. **Agendamento** — uma mensagem agendada é um compromisso futuro (`pending`) que precisa ser cumprido, não apenas um registro em uma tabela.
3. **Entrega confiável** — um processo em segundo plano (Celery) monitora continuamente esses compromissos e os transforma em mensagens efetivamente enviadas (`pending → process → sent`), sem exigir que o usuário esteja com o app aberto.

---

## 🏗️ Arquitetura

O projeto segue **Clean Architecture** e **DDD**, com separação clara entre domínio e implementação, organizada em 4 camadas por aplicação:

```
┌─────────────────────┐
│   API (HTTP)         │  ← Schemas: MessageInSchema, UserInSchema
└──────────┬───────────┘
           │
           ▼
┌─────────────────────┐
│ Application Layer    │  ← Use Cases: RegisterMessageUseCase
│ (Casos de Uso)       │  ← DTOs: MessageInDTO → MessageOutDTO
└──────────┬───────────┘
           │
           ▼
┌─────────────────────┐
│  Domain Layer        │  ← Entities: MessageEntity, UserEntity
│ (Regras de Negócio)  │  ← Repositórios (Interfaces)
└──────────┬───────────┘
           │
           ▼
┌─────────────────────┐
│ Infrastructure        │  ← Repository: MessagesRepository
│ (Persistência)        │  ← Models: Message (ORM)
└──────────┬───────────┘
           │
           ▼
┌─────────────────────┐
│   PostgreSQL          │
└─────────────────────┘
```

### Padrões Arquiteturais Implementados

| Padrão | Descrição | Implementação |
|---|---|---|
| **Domain-Driven Design (DDD)** | Separação clara entre domínio e implementação | Domain → Application → Infrastructure → API |
| **Clean Architecture** | Independência de frameworks na lógica de negócio | Cada app segue as 4 camadas |
| **Dependency Injection** | Injeção de dependências automática | `dependency-injector` com Containers |
| **Repository Pattern** | Abstração de persistência | `IMessagesRepository`, `IUserRepository` |
| **DTO Pattern** | Transferência de dados entre camadas | `MessageInDTO`, `UserOutDTO` |
| **Adapter Pattern** | Integração com serviços externos | `IWahaMessageAdapter`, `ITaksSendMessageAdapter` |
| **Task Queue Pattern** | Processamento assíncrono | Celery + Redis |
| **Value Objects** | Objetos com identidade de valor | `ScheduledAtTime` |

---

## 📦 Stack Tecnológico

| Categoria | Tecnologia | Versão | Propósito |
|---|---|---|---|
| Framework Web | Django | ≥ 6.0.7 | Framework web e ORM |
| API REST | Django Ninja | ≥ 1.6.2 | API REST de alta performance |
| Serialização | Pydantic | ≥ 2.13.4 | Validação de dados e schemas |
| Injeção de Dependências | dependency-injector | ≥ 4.49.1 | Container de DI |
| Banco de Dados | PostgreSQL | - | Persistência de dados |
| Driver do BD | psycopg2-binary | ≥ 2.9.12 | Conector PostgreSQL |
| Fila de Tarefas | Celery | ≥ 5.6.3 | Processamento assíncrono |
| Message Broker | Redis | ≥ 8.0.1 | Broker do Celery + cache |
| Autenticação | PyJWT | ≥ 2.13.0 | Tokens JWT |
| Hash de Senhas | Passlib | ≥ 1.7.4 | Hashing bcrypt |
| HTTP Client | Requests | ≥ 2.34.2 | Requisições HTTP (Waha API) |
| Variáveis de Ambiente | python-dotenv | ≥ 0.9.9 | Carregamento de `.env` |
| Formatação | Black + Blue | ≥ 22.1.0 | Code formatting |

> **Requisitos:** Python ≥ 3.12

---

## 🗂️ Estrutura do Projeto

```
agendador_whatsapp/
├── config/                          # Configuração global do projeto
│   ├── settings.py                  # Configurações Django
│   ├── urls.py                      # Roteamento principal
│   ├── api.py                       # Configuração Django Ninja
│   ├── celery.py                    # Configuração Celery
│   ├── app_container.py             # Container DI principal
│   ├── core_container.py            # Container de serviços core
│   └── dependencies.py              # Inicialização de dependências
│
├── app/
│   ├── message/                     # 📧 App de Mensagens
│   │   ├── domain/                  # Entities, Repositories, Value Objects
│   │   ├── application/             # Use Cases e DTOs
│   │   ├── infrastructure/          # Models ORM, Repository, Adapters, Tasks
│   │   ├── api/                     # Views, Schemas, DI
│   │   └── migrations/
│   │
│   └── users/                       # 👤 App de Usuários
│       ├── domain/                  # Entities, Repositories, Services
│       ├── application/             # Use Cases e DTOs
│       ├── infrastructure/          # Models ORM, Repository, Services
│       ├── api/                     # Views, Schemas, AuthCookie, DI
│       └── migrations/
│
├── core/                            # Utilitários compartilhados
│   └── exceptions.py                # BaseDomainException, FieldRequiredException
│
├── manage.py
├── pyproject.toml
├── uv.lock
├── docker-compose.yaml
├── Dockerfile
├── celerybeat-schedule
└── README.md
```

---

## 🧩 Entidades do Domínio

### `MessageEntity`

```python
@dataclass
class MessageEntity:
    id: UUID
    message: str
    scheduled_at: ScheduledAtTime | None
    number: str
    session: str
    status: StatusMessage | str
    created_at: datetime
```

**Métodos:** `change_number()`, `change_message()`, `change_status()`
**Validações:** `message`, `number` e `status` são obrigatórios.

### `UserEntity`

```python
@dataclass
class UserEntity:
    id: UUID
    name: str
    email: str
    password: str
    phone: str | None
    connected: bool
    session: str
    session_started: bool
    access_contacts: bool
    created_at: datetime
    deleted_at: datetime | None
```

**Métodos:** `delete()` (soft delete), `change_connection_status()`, `change_session_status()`, `change_permissions()`
**Atributos:** `access_contacts` controla se o usuário tem permissão de sincronizar contatos do WhatsApp.
A sessão é gerada automaticamente no formato `session_{id}`.

### `RefreshTokenEntity`

```python
@dataclass
class RefreshTokenEntity:
    id: UUID
    token: str
    revoked: bool
    user: UUID | None
    created_at: datetime
    expire_at: datetime | None
```

**Métodos:** `revoked_token()`, `is_valid()`

### `ContactEntity`

```python
@dataclass
class ContactEntity:
    id: UUID
    contact_id: str
    name: str
    number: str
    user: UUID | None
    created_at: datetime
```

**Métodos:** `change_name()`
**Validações:** `name` é obrigatório. Cada contato é associado a um usuário e vinculado ao ID do WhatsApp via `contact_id`.

---

## 🔄 Casos de Uso

Casos de uso descritos em formato resumido (estilo Cockburn): ator, objetivo, pré-condição, cenário de sucesso principal e extensões relevantes.

### Módulo de Mensagens

#### UC01 · Agendar Mensagem — `RegisterMessageUseCase`
- **Ator:** Usuário autenticado
- **Objetivo:** Agendar o envio futuro de uma mensagem para um número de WhatsApp
- **Pré-condição:** Usuário existe e possui sessão Waha associada
- **Cenário principal:**
  1. Usuário informa mensagem, número de destino e data/hora de envio
  2. Sistema valida a existência do usuário
  3. Sistema cria a mensagem com status `pending`, vinculada à sessão do usuário
  4. Sistema persiste a mensagem e confirma o agendamento
- **Extensões:** *2a.* Usuário não encontrado → `UserNotFoundException`

#### UC02 · Listar Mensagens Pendentes — `ListMessagesToSendUseCase`
- **Ator:** Sistema (Celery Beat)
- **Objetivo:** Identificar mensagens que já atingiram o horário de envio
- **Pré-condição:** Existem mensagens com status `pending`
- **Cenário principal:**
  1. Sistema consulta mensagens com `scheduled_at <= agora`
  2. Sistema filtra apenas as mensagens com status `pending`
  3. Sistema retorna a lista para processamento

#### UC03 · Enviar Mensagem — `SendMessageUseCase`
- **Ator:** Sistema (Celery Worker)
- **Objetivo:** Entregar a mensagem agendada via WhatsApp
- **Pré-condição:** Mensagem existe e está com status `process`
- **Cenário principal:**
  1. Sistema busca a mensagem pelo ID
  2. Sistema solicita o envio ao adaptador da Waha API
  3. Sistema atualiza o status da mensagem para `sent`
- **Extensões:** *1a.* Mensagem não encontrada → `MessageNotFoundException`

#### UC04 · Consultar Mensagem por ID — `ResponseMessageByIDUseCase`
- **Ator:** Usuário / Sistema
- **Objetivo:** Obter os dados atuais de uma mensagem agendada
- **Cenário principal:**
  1. Solicitante informa o ID da mensagem
  2. Sistema busca e valida a existência da mensagem
  3. Sistema retorna os dados da mensagem
- **Extensões:** *2a.* Mensagem não encontrada → `MessageNotFoundException`

#### UC05 · Listar Mensagens por Número — `ResponseMessageByNumber`
- **Ator:** Usuário
- **Objetivo:** Consultar o histórico de mensagens agendadas para um número
- **Cenário principal:**
  1. Usuário informa o número de destino
  2. Sistema busca todas as mensagens associadas a esse número
  3. Sistema retorna a lista de mensagens

---

### Módulo de Usuários

#### UC06 · Registrar Usuário — `RegisterUserUseCase`
- **Ator:** Visitante
- **Objetivo:** Criar uma conta e disponibilizar uma sessão de WhatsApp pronta para uso
- **Pré-condição:** E-mail informado ainda não está cadastrado
- **Cenário principal:**
  1. Visitante informa nome, e-mail, senha e telefone
  2. Sistema valida que o e-mail é único
  3. Sistema hasheia a senha (bcrypt)
  4. Sistema cria a sessão Waha correspondente (cria e inicia, se necessário)
  5. Sistema persiste o novo usuário
- **Extensões:** *2a.* E-mail já cadastrado → erro de validação

#### UC07 · Autenticar Usuário — `LoginUseCase`
- **Ator:** Usuário registrado
- **Objetivo:** Obter acesso autenticado ao sistema
- **Pré-condição:** Usuário possui conta ativa
- **Cenário principal:**
  1. Usuário informa e-mail e senha
  2. Sistema localiza o usuário pelo e-mail
  3. Sistema valida a senha informada
  4. Sistema gera `access_token` (30 min) e `refresh_token` (7 dias)
  5. Sistema persiste o refresh token e retorna ambos ao usuário
- **Extensões:** *2a.* Usuário não encontrado → `UserNotFoundException` · *3a.* Senha inválida → `BaseDomainException`

#### UC08 · Consultar Usuário por ID — `ResponseUserByIDUseCase`
- **Ator:** Usuário / Sistema
- **Objetivo:** Obter os dados de um usuário específico
- **Cenário principal:**
  1. Solicitante informa o ID do usuário
  2. Sistema busca, valida existência e verifica se não está deletado
  3. Sistema retorna os dados do usuário
- **Extensões:** *2a.* Usuário não encontrado ou deletado → `UserNotFoundException`

#### UC09 · Consultar Usuário por E-mail — `ResponseUserByEmailUseCase`
- **Ator:** Usuário / Sistema
- **Objetivo:** Localizar um usuário a partir do e-mail cadastrado
- **Cenário principal:**
  1. Solicitante informa o e-mail
  2. Sistema busca e valida a existência do usuário
  3. Sistema retorna os dados do usuário
- **Extensões:** *2a.* Usuário não encontrado → `UserNotFoundException`

#### UC10 · Desativar Usuário — `DeactiveUserUseCase`
- **Ator:** Usuário
- **Objetivo:** Encerrar a conta sem apagar o histórico (soft delete)
- **Pré-condição:** Usuário existe e está ativo
- **Cenário principal:**
  1. Usuário solicita a exclusão da própria conta
  2. Sistema remove a sessão Waha associada
  3. Sistema marca o usuário como deletado (`deleted_at`)
  4. Sistema persiste a alteração

#### UC11 · Gerar QR Code do WhatsApp — `LoginWahaForWhatsAppQrCodeUseCase`
- **Ator:** Usuário autenticado
- **Objetivo:** Conectar o número de WhatsApp à sessão do sistema via leitura de QR code
- **Pré-condição:** Usuário autenticado, sessão Waha ainda não conectada
- **Cenário principal:**
  1. Usuário solicita o QR code de conexão
  2. Sistema requisita a imagem à Waha API
  3. Sistema retorna o QR code em formato de imagem (PNG/base64)

#### UC12 · Gerar Código de Verificação — `RequestCodeLoginWhatsAppUseCase`
- **Ator:** Usuário autenticado
- **Objetivo:** Conectar o número de WhatsApp via código de verificação (alternativa ao QR code)
- **Pré-condição:** Usuário autenticado, sessão Waha ainda não conectada
- **Cenário principal:**
  1. Usuário solicita o código de verificação
  2. Sistema requisita o código à Waha API
  3. Sistema retorna o código para o usuário inserir no WhatsApp

#### UC13 · Habilitar Sincronização de Contatos — `EnableSyncContactsUseCase`
- **Ator:** Usuário autenticado
- **Objetivo:** Permitir que o sistema sincronize os contatos do WhatsApp do usuário
- **Pré-condição:** Usuário autenticado e conectado ao WhatsApp
- **Cenário principal:**
  1. Usuário solicita a ativação da sincronização de contatos
  2. Sistema dispara a tarefa de sincronização via Celery
  3. Sistema atualiza a permissão `access_contacts = True`
  4. Sistema persiste a alteração

#### UC14 · Sincronizar Contatos do Usuário — `SyncContactsUserUseCase`
- **Ator:** Sistema (Celery Worker)
- **Objetivo:** Buscar e armazenar os contatos da sessão de WhatsApp do usuário
- **Pré-condição:** Usuário existe e possui sessão Waha conectada, `access_contacts = True`
- **Cenário principal:**
  1. Sistema requisita a lista de contatos à Waha API
  2. Sistema filtra contatos já existentes no banco
  3. Sistema persiste os novos contatos associando-os ao usuário

#### UC15 · Listar Contatos do Usuário — `ListContactsByUserUseCase`
- **Ator:** Usuário autenticado
- **Objetivo:** Obter a lista de contatos sincronizados do usuário
- **Pré-condição:** Usuário autenticado e com contatos sincronizados
- **Cenário principal:**
  1. Usuário solicita a lista de seus contatos
  2. Sistema busca todos os contatos associados ao usuário
  3. Sistema retorna a lista de contatos

#### UC16 · Consultar Contato por ID — `ResponseContactByIDUseCase`
- **Ator:** Usuário
- **Objetivo:** Obter os dados de um contato específico
- **Cenário principal:**
  1. Solicitante informa o ID do contato
  2. Sistema busca e valida a existência do contato
  3. Sistema retorna os dados do contato
- **Extensões:** *2a.* Contato não encontrado → `ContactNotFoundException`

#### UC17 · Consultar Contato por Número — `ResponsenContactByNumberUseCase`
- **Ator:** Usuário
- **Objetivo:** Localizar um contato a partir do número de telefone
- **Cenário principal:**
  1. Solicitante informa o número de telefone
  2. Sistema busca e valida a existência do contato
  3. Sistema retorna os dados do contato
- **Extensões:** *2a.* Contato não encontrado → `ContactNotFoundException`

---

## 🔌 Endpoints da API

**Base URL:** `/api/v1`
**Documentação Swagger:** `/api/v1/docs`

### Auth (`/auth`)

| Método | Rota | Auth | Status | Descrição |
|---|---|---|---|---|
| POST | `/auth/login` | ❌ | 201 | Login e geração de tokens |
| GET | `/auth/me` | ✅ JWT | 200 | Dados do usuário autenticado |

### Usuários (`/users`)

| Método | Rota | Auth | Status | Descrição |
|---|---|---|---|---|
| POST | `/users/` | ❌ | 201 | Registrar novo usuário |
| GET | `/users/{id}` | ❌ | 200 | Obter usuário por ID |
| GET | `/users/email` | ❌ | 200 | Obter usuário por e-mail |
| DELETE | `/users/{id}` | ❌ | 200 | Deletar usuário (soft delete) |
| PATCH | `/users/{id}` | ❌ | 200 | Habilitar sincronização de contatos |
| GET | `/users/login/qr-code` | ✅ JWT | 200 | Obter QR code do WhatsApp |
| GET | `/users/login/request-code` | ✅ JWT | 200 | Obter código de verificação |

### Mensagens (`/message`)

| Método | Rota | Auth | Status | Descrição |
|---|---|---|---|---|
| POST | `/message/` | ✅ JWT | 201 | Agendar nova mensagem |
| GET | `/message/{id}` | ❌ | 200 | Obter mensagem por ID |
| GET | `/message/list` | ❌ | 200 | Listar mensagens por número |

### Contatos (`/contacts`)

| Método | Rota | Auth | Status | Descrição |
|---|---|---|---|---|
| GET | `/contacts/sync` | ✅ JWT | 200 | Sincronizar contatos do WhatsApp |
| GET | `/contacts/list/sync-contacts` | ✅ JWT | 200 | Listar contatos sincronizados |
| GET | `/contacts/id` | ❌ | 200 | Obter contato por ID |
| GET | `/contacts/` | ❌ | 200 | Obter contato por número | 

### Exemplos de Requisição

<details>
<summary><strong>POST /auth/login</strong></summary>

```json
// Request
{
  "email": "user@example.com",
  "password": "senha123"
}

// Response 201
{
  "access_token": "eyJhbGc...",
  "refresh_token": "uuid-aqui-refresh"
}
```
</details>

<details>
<summary><strong>POST /users/</strong></summary>

```json
// Request
{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123",
  "phone": "5511999999999"
}

// Response 201
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "João Silva",
  "email": "joao@example.com",
  "phone": "5511999999999",
  "connected": true,
  "session": "session_550e8400-e29b-41d4-a716-446655440000",
  "session_started": true,
  "created_at": "2024-07-22T10:30:00",
  "deleted_at": null
}
```
</details>

<details>
<summary><strong>POST /message/</strong></summary>

```json
// Request
// Header: Authorization: Bearer eyJhbGc...
{
  "message": "Olá! Esta é uma mensagem agendada.",
  "scheduled_at": "2024-07-22T15:30:00",
  "number": "5511999999999"
}

// Response 201
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "message": "Olá! Esta é uma mensagem agendada.",
  "scheduled_at": "2024-07-22T15:30:00",
  "number": "5511999999999",
  "session": "session_550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2024-07-22T10:30:00"
}
```
</details>

<details>
<summary><strong>GET /users/login/qr-code</strong></summary>

```json
// Response 200
{
  "connected": false,
  "qr_code_base64": "data:image/png;base64,iVBORw0KGgoAAAA..."
}
```
</details>

<details>
<summary><strong>PATCH /users/{id}</strong></summary>

```json
// Header: Authorization: Bearer eyJhbGc...
// Response 200
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "João Silva",
  "email": "joao@example.com",
  "phone": "5511999999999",
  "connected": true,
  "session": "session_550e8400-e29b-41d4-a716-446655440000",
  "session_started": true,
  "access_contacts": true,
  "created_at": "2024-07-22T10:30:00",
  "deleted_at": null
}
```
</details>

<details>
<summary><strong>GET /contacts/list/sync-contacts</strong></summary>

```json
// Header: Authorization: Bearer eyJhbGc...
// Response 200
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "contact_id": "5511999888888@c.us",
    "name": "Maria Santos",
    "number": "5511999888888",
    "user": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-07-22T11:15:00"
  }
]
```
</details>

---

## 📊 Banco de Dados

### `users`

| Campo | Tipo | Null | Chave | Descrição |
|---|---|---|---|---|
| `id` | UUID | ❌ | PK | Identificador único |
| `name` | VARCHAR(190) | ❌ | - | Nome do usuário |
| `email` | VARCHAR(255) | ❌ | UNIQUE | E-mail de autenticação |
| `password` | VARCHAR(120) | ❌ | - | Senha hasheada (bcrypt) |
| `phone` | VARCHAR(180) | ✅ | - | Telefone |
| `connected` | BOOLEAN | ❌ | - | Status de conexão WhatsApp |
| `session` | VARCHAR(100) | ❌ | - | ID da sessão Waha |
| `session_started` | BOOLEAN | ❌ | - | Sessão iniciada |
| `created_at` | DATETIME | ❌ | - | Data de criação |
| `deleted_at` | DATETIME | ✅ | - | Data de soft delete |

### `refresh_token`

| Campo | Tipo | Null | Chave | Descrição |
|---|---|---|---|---|
| `id` | UUID | ❌ | PK | Identificador único |
| `token` | VARCHAR(255) | ❌ | - | Token hasheado (SHA-256) |
| `user_id` | UUID | ❌ | FK → users.id | Usuário associado |
| `revoked` | BOOLEAN | ❌ | - | Token revogado |
| `created_at` | DATETIME | ❌ | - | Data de criação |
| `expire_at` | DATETIME | ❌ | - | Data de expiração |

### `contacts`

| Campo | Tipo | Null | Chave | Descrição |
|---|---|---|---|---|
| `id` | UUID | ❌ | PK | Identificador único |
| `contact_id` | VARCHAR(100) | ✅ | - | ID do contato no WhatsApp (Waha) |
| `name` | VARCHAR(130) | ❌ | - | Nome do contato |
| `number` | VARCHAR(180) | ❌ | UNIQUE | Número de telefone |
| `user_id` | UUID | ❌ | FK → users.id | Usuário proprietário |
| `created_at` | DATETIME | ❌ | - | Data de sincronização |

### `messages`

| Campo | Tipo | Null | Chave | Descrição |
|---|---|---|---|---|
| `id` | UUID | ❌ | PK | Identificador único |
| `message` | VARCHAR(290) | ❌ | - | Conteúdo da mensagem |
| `scheduled_at` | DATETIME | ✅ | - | Data/hora de envio |
| `number` | VARCHAR(60) | ❌ | - | Número WhatsApp destino |
| `session` | VARCHAR(100) | ✅ | - | Sessão Waha do remetente |
| `status` | VARCHAR(45) | ❌ | - | `pending` \| `process` \| `sent` |
| `created_at` | DATETIME | ❌ | - | Data de criação |

---

## 🔐 Autenticação

O sistema utiliza **JWT (Bearer Token)** para autenticação e **Refresh Token** para renovação de sessão.

| Tipo | Validade | Formato | Observações |
|---|---|---|---|
| Access Token | 30 minutos | JWT | Enviado via `Authorization: Bearer <token>` |
| Refresh Token | 7 dias | SHA-256 hash de UUID | Armazenado no BD, pode ser revogado |

**Payload JWT:**

```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "session": "session_uuid",
  "exp": "timestamp-futuro"
}
```

O middleware `AuthCookie` decodifica o JWT, busca o usuário no banco e injeta o objeto ORM em `request.auth`.

**Endpoints protegidos:**
- `GET /auth/me`
- `GET /users/login/qr-code`
- `GET /users/login/request-code`
- `POST /message/`
- `GET /contacts/sync`
- `GET /contacts/list/sync-contacts`

---

## ⚡ Tarefas Assíncronas (Celery)

**Broker:** Redis · **Agendador:** Celery Beat

### `check_message_schedule`

Executada a cada **60 segundos**. Lista mensagens com `scheduled_at <= agora` e status `pending`, altera o status para `process` e dispara a task `send_message` para cada uma.

```python
CELERY_BEAT_SCHEDULE = {
    'check_message_scheduled': {
        'task': 'check_message_schedule',
        'schedule': 60,
    }
}
```

### `send_message`

Busca a mensagem, envia via `WahaMessageAdapter.send_message()` e atualiza o status para `sent`.

### `sync_contacts`

Executada sob demanda (quando o usuário ativa sincronização). Busca os contatos da sessão Waha do usuário, filtra duplicatas e persiste os novos contatos no banco associando-os ao usuário.

**Trigger:** Chamada via `EnableSyncContactsUseCase` quando usuário ativa essa permissão.

### Fluxo completo de envio automático

```
Celery Beat (a cada 60s)
  └─ check_message_schedule()
       ├─ Lista mensagens pendentes vencidas
       ├─ Para cada mensagem: status → "process"
       └─ Dispara send_message(id)
             ├─ Busca mensagem
             ├─ Envia via Waha API (POST /api/sendText)
             └─ status → "sent"
```

### Fluxo de sincronização de contatos

```
Usuário (POST /users/{id} com ativação)
  └─ EnableSyncContactsUseCase
       ├─ Valida usuário e permissão
       ├─ Dispara sync_contacts via Celery
       └─ status → access_contacts = True

Celery Worker
  └─ sync_contacts(user_id)
       ├─ SyncContactsUserUseCase
       ├─ Busca contatos via Waha API
       ├─ Filtra e salva no banco
       └─ Contatos disponíveis em /contacts/list/sync-contacts
```

---

## 📦 Injeção de Dependências

O projeto utiliza `dependency-injector` com containers hierárquicos:

```python
class AppContainer(DeclarativeContainer):
    core = providers.Container(CoreContainer)          # Serviços core (Waha, Hash)
    messages = providers.Container(MessageContainer)   # Repositórios + Use Cases
    users = providers.Container(UserContainer)         # Repositórios + Use Cases
```

- **`CoreContainer`** – expõe `waha_adapter` e `hash_service` como singletons.
- **`MessageContainer`** – provê repositórios e use cases do módulo de mensagens.
- **`UserContainer`** – provê repositórios, serviços de token/hash e use cases do módulo de usuários.

**Uso em views:**

```python
@router.post('/', response={201: MessageOutSchema}, auth=AuthCookie())
def register_message(request, data: MessageInSchema):
    use_case = container.messages.register_message_use_case()
    message = use_case.execute(data.to_dto(), request.auth.id)
    return 201, MessageOutSchema.from_domain(message)
```

---

## 🚀 Instalação e Configuração

O projeto utiliza **[uv](https://docs.astral.sh/uv/)** como gerenciador de pacotes e ambientes Python, com as dependências e o lockfile definidos em `pyproject.toml` / `uv.lock`.

### Pré-requisitos

- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado
- PostgreSQL
- Redis
- Docker e Docker Compose (opcional, recomendado para subir os serviços de apoio)

### Rodando com uv

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd agendador_whatsapp

# Configure as variáveis de ambiente
cp .env.example .env

# Instale as dependências e crie o ambiente virtual (lê pyproject.toml/uv.lock)
uv sync

# Rode as migrações
uv run manage.py migrate

# Inicie o servidor de desenvolvimento
uv run manage.py runserver

# Em terminais separados, inicie o worker e o beat do Celery
uv run celery -A config worker -l info
uv run celery -A config beat -l info
```

### Rodando com Docker Compose

```bash
# Configure as variáveis de ambiente
cp .env.example .env

# Suba os containers (Django, PostgreSQL, Redis, Celery Worker, Celery Beat)
docker compose up --build
```

A documentação interativa (Swagger) fica disponível em `http://localhost:8000/api/v1/docs`.

---

## ⚙️ Variáveis de Ambiente

```bash
# Django
SECRET_KEY=sua-chave-secreta
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=agendador_whatsapp
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432

# JWT
JWT_ALGORITHIM=HS256

# Celery
CELERY_BROKER_URL=redis://redis:6379/0

# Waha
WAHA_BASE_URL=http://waha-api:3000
WAHA_API_KEY=sua-chave-waha
```

---

## 🗺️ Roadmap

Linha do tempo do desenvolvimento, da fundação do projeto até o estado atual e os próximos passos.

### ✅ Fase 1 — Fundação da arquitetura
- [✅] Definição da arquitetura em camadas (Domain → Application → Infrastructure → API)
- [✅] Estruturação do projeto Django com Django Ninja
- [✅] Configuração do container de injeção de dependências (`dependency-injector`)
- [✅] Definição das exceções de domínio (`BaseDomainException`, `FieldRequiredException`)

### ✅ Fase 2 — Módulo de Usuários
- [✅] Modelagem de `UserEntity` e `RefreshTokenEntity`
- [✅] Cadastro de usuário com hash de senha (bcrypt)
- [✅] Login com geração de `access_token` (JWT) e `refresh_token`
- [✅] Middleware de autenticação (`AuthCookie`)
- [✅] Soft delete de usuários

### ✅ Fase 3 — Integração com WhatsApp (Waha API)
- [✅] Adaptador `WahaMessageAdapter` (criação/início de sessão, status)
- [✅] Geração de QR code para conexão do WhatsApp
- [✅] Geração de código de verificação para conexão alternativa

### ✅ Fase 4 — Módulo de Mensagens
- [✅] Modelagem de `MessageEntity` e `ScheduledAtTime`
- [✅] Agendamento de mensagens (status `pending`)
- [✅] Consulta de mensagens por ID e por número

### ✅ Fase 5 — Processamento Assíncrono
- [✅] Configuração do Celery + Redis como broker
- [✅] Task `check_message_schedule` (verificação periódica via Celery Beat)
- [✅] Task `send_message` (envio efetivo via Waha API)
- [✅] Ciclo de status automático: `pending → process → sent`

### ✅ Fase 6 — Módulo de Contatos
- [✅] Modelagem de `ContactEntity`
- [✅] Sincronização de contatos do WhatsApp via Waha API
- [✅] Filtragem de contatos já existentes (sem duplicatas)
- [✅] Listagem de contatos por usuário
- [✅] Consulta de contato por ID e por número
- [✅] Task `sync_contacts` (sincronização via Celery)

### ✅ Fase 7 — Controle de Permissões
- [✅] Atributo `access_contacts` em UserEntity
- [✅] Caso de uso `EnableSyncContactsUseCase` para ativação de sincronização
- [✅] Endpoints protegidos por JWT para operações de contato

### 🔜 Próximos Passos
- [ ] Testes unitários e de integração para domínio e casos de uso
- [ ] Logging centralizado e estruturado
- [ ] Rate limiting nos endpoints públicos
- [ ] Cache de leitura com Redis
- [ ] Reenvio automático em caso de falha no envio (retry/backoff)
- [ ] Expansão da documentação da API (exemplos e descrições no Swagger)
- [ ] Validação adicional de inputs em endpoints públicos
- [ ] Tratamento de erros melhorado com respostas mais descritivas

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato

- **Autor** — Arthur França Silva
- **E-mail** — arthurfranca.dev@gmail.com
- **GitHub** — [@Thurzinfs](https://github.com/Thurzinfs)

---

<div align="center">
  Desenvolvido com ❤️ por <a href="https://github.com/Thurzinfs">Arthur França Silva</a>
</div>