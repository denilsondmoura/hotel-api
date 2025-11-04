# 🏨 Hotel API

API REST desenvolvida em **Django Rest Framework** para gerenciamento de hotéis, quartos e reservas.  
A aplicação utiliza **Docker** para facilitar a configuração do ambiente e o **Celery** para tarefas assíncronas, como envio de e-mails e verificação automática de reservas concluídas.

---

## 🚀 Tecnologias principais

- [Python 3.12](https://www.python.org/)
- [Django 5+](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryq.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Swagger / Redoc](https://drf-spectacular.readthedocs.io/)

---

## ⚙️ Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/denilsondmoura/hotel-api.git
cd hotel-api
```

### 2. Copiar o arquivo de exemplo e renomear para .env

O projeto já contém um arquivo de exemplo chamado env-dev.
Você pode copiá-lo e renomear para .env com o comando abaixo:

```bash
cp env-dev .env
```

Em seguida, edite o arquivo .env conforme necessário (por exemplo, alterar senha do banco, modo debug, etc.)

### 3. Construir e iniciar os containers Docker

```bash
docker compose build
docker compose up -d
```

Esses comandos:

- Constroem os containers da aplicação (web, db, redis, celery, celery_beat)
- Aplica automaticamente as migrations
- Carrega as fixtures iniciais (usuários e dados de exemplo)
- Inicia o servidor Django em modo de produção

### 4. Acessar a aplicação

Após a inicialização dos containers, acesse:

### Serviço	URL
| Serviço          | URL                                                                                |
| ---------------- | ---------------------------------------------------------------------------------- |
| 🌐 API Principal | [http://localhost:8000/](http://localhost:8000/)                                   |
| 📘 Swagger UI    | [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/) |
| 📗 ReDoc         | [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/)     |
| 🐘 Admin Django  | [http://localhost:8000/admin/](http://localhost:8000/admin/)                       |

### 👤 Usuários de teste
| Tipo              | Usuário   | Senha    |
| ----------------- | --------- | -------- |
| 👥 Cliente        | `cliente` | `123456` |
| 🛠️ Administrador | `admin`   | `123456` |

### 🧩 Estrutura dos containers
| Serviço       | Descrição                         |
| ------------- | --------------------------------- |
| `web`         | API Django (gunicorn)             |
| `db`          | Banco PostgreSQL                  |
| `redis`       | Broker do Celery                  |
| `celery`      | Worker para tarefas assíncronas   |
| `celery_beat` | Scheduler para tarefas periódicas |

### ⏰ Tarefas automáticas (Celery Beat)

O sistema executa periodicamente:

- verifica_reservas_concluidas_task → Atualiza reservas cuja data de checkout já passou, marcando-as como concluídas.

### 🧠 Funcionalidades principais

- Cadastro e gerenciamento de Usuários, Hoteis e Quartos
- Registro de Reservas
- Validação automática de disponibilidade e valores
- Envio de e-mails de confirmação
- Swagger / Redoc integrados para documentação da API
- Tarefas agendadas com Celery Beat
