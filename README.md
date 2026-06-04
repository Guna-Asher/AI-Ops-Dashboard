# AI Ops Dashboard — Event-Driven Incident Management with AI Root Cause Analysis, JWT Auth, and Full Observability

> Portfolio-grade enterprise README built directly from the repository implementation.

## Executive Summary

AI Ops Dashboard is a multi-service, event-driven platform that demonstrates production-style backend engineering, DevOps/SRE practices, distributed systems patterns, and AI integration.

The system is composed of:

- **Frontend (Nginx + static assets)**: A browser UI that registers users, logs in with JWT, creates incidents, and displays incidents/logs/widgets.
- **Backend (FastAPI)**: REST API for authentication, incidents, logs, alerts, and dashboard widgets.
- **Worker (Python asyncio + aio-pika)**: A background consumer that listens to RabbitMQ events (incident creation) and runs AI analysis (Gemini integration) asynchronously.
- **PostgreSQL**: Source of truth for users, incidents, logs, alerts, and dashboard widget configuration.
- **Redis**: Used by the backend runtime (client exists; implementation is minimal but wired at startup).
- **RabbitMQ**: Event bus for incident processing.
- **Prometheus + Grafana**: Metrics scraping and visualization.
- **Docker + Docker Compose**: Local and integration-friendly container runtime.
- **Kubernetes manifests**: Deployability scaffolding for backend/worker and supporting services.
- **GitHub Actions**: CI (lint + tests) and CD (build/push Docker images + EC2 deployment).

### How the “AI” part works in this repo

- When a user creates an incident via the API, the backend publishes an event to RabbitMQ: **`incident.created`** with payload `{ "incident_id": <id> }`.
- The worker consumes from queue **`incidents.events`**.
- The worker fetches the incident and the most recent 50 log entries for that incident.
- The worker calls an AI client:
  - If `GOOGLE_API_KEY` is empty or set to `"dummy"`, it returns a deterministic **dummy analysis**.
  - Otherwise it calls **Google Generative AI** using model **`gemini-1.5-flash`**.
- The worker persists the AI output by appending it to `Incident.description` under a `[AI Analysis]` marker.

### System complexity (what’s actually in the code)

This is not a toy demo. It includes real engineering surfaces:

- OAuth2-style JWT access token + JWT refresh token.
- Password storage with **SHA-256 pre-hash + bcrypt**.
- Async SQLAlchemy database layer (Async engine + Async sessions).
- RabbitMQ-based asynchronous processing with robust connections.
- Prometheus metrics instrumentation on FastAPI.
- Docker compose with multiple interdependent services.
- Kubernetes manifests and ingress.
- CI/CD pipelines.

---

## Project Title

**AI Ops Dashboard** — Event-Driven Incident Management with AI Root Cause Analysis, Async Backend/Worker, JWT Auth, and Prometheus/Grafana Observability

---

## Why I Built This Project

### Problem statement

Teams spend significant time on:

- Creating and tracking operational incidents.
- Collecting contextual signals (logs) and correlating them to incidents.
- Running analysis—often delayed, manual, or inconsistent.

This project targets the gap between:

- **Synchronous user workflows** (create incident, view details), and
- **Asynchronous enrichment/analysis** (fetch logs, run AI reasoning, update records).

### Real-world motivation

In real incident workflows, the “front door” (user reports/creates an incident) must remain responsive, while expensive computation (AI analysis, summarization, enrichment) must happen in the background.

A robust architecture should:

- Accept requests quickly.
- Publish durable events.
- Process in workers that can be scaled independently.
- Persist results back to the source of truth.
- Provide observability (metrics + health checks).

### Engineering goals (directly aligned with implementation)

1. **Build a working event-driven pipeline**:
   - Backend publishes RabbitMQ events.
   - Worker consumes and processes.
2. **Demonstrate secure auth**:
   - JWT access tokens and refresh tokens.
   - Password hashing that is explicit and testable.
3. **Demonstrate operational readiness**:
   - Docker Compose for repeatable local runs.
   - Prometheus instrumentation.
   - Kubernetes deployment manifests.
4. **Demonstrate AI integration patterns**:
   - Deterministic dummy mode.
   - Real Gemini call when API key is configured.
5. **Maintain a single source of truth**:
   - README maps to actual endpoints, env vars, and data model.

---

## Features

### Authentication & Security

- **User registration**: `POST /api/v1/auth/register`
- **JWT access token issuance**: `POST /api/v1/auth/login`
- **JWT refresh token flow**: `POST /api/v1/auth/refresh`
- **JWT verification dependency** used by protected endpoints (see `backend/app/api/deps.py`)
- **Role/flag support**:
  - `User.is_superuser` and `User.is_active` exist in model.
- **Password hashing strategy**:
  - SHA-256 pre-hash + bcrypt

### Incident Management

- List incidents
- Create incident (publishes RabbitMQ event)
- Get incident
- Update incident
- Delete incident (route/service checks current user; see code)

### Log Management

- List logs with optional `incident_id` filter
- Create log entries
- Get log entry by ID

### Alerts

- List alerts
- Create alerts
- Update alerts
- Delete alerts

### Dashboard Widgets

- List widgets for current user
- Create widget for current user

### Event-Driven AI Analysis

- Worker listens for `incident.created`
- Worker loads incident + last 50 logs
- Worker runs AI analysis (dummy or Gemini)
- Worker appends analysis to incident description

### Observability

- FastAPI instrumentation for Prometheus metrics
- `/metrics` endpoint exposed (via prometheus-fastapi-instrumentator)
- `/health` endpoint

### DevOps & Delivery

- Dockerfile for backend/worker and Nginx for frontend
- Docker Compose for local stack
- Kubernetes manifests for backend/worker and supporting services
- GitHub Actions:
  - CI: lint + pytest
  - CD: build/push images and deploy on EC2 via SSH

---

## Architecture Overview

### System architecture diagram (Mermaid)

```mermaid
graph TD
  User[Operator/User] -->|Browser| Frontend[Nginx Static Frontend]
  Frontend -->|HTTP /api/v1/*| Backend[FastAPI Backend]
  Backend -->|Async SQLAlchemy| Postgres[(PostgreSQL)]
  Backend -->|JWT verification & issuance| Backend
  Backend -->|Publish event| RabbitMQ[RabbitMQ]

  RabbitMQ -->|incidents.events| Worker[Worker Consumer]
  Worker -->|Async SQLAlchemy| Postgres
  Worker -->|Recent logs| Worker
  Worker -->|AI call (dummy or Gemini)| Gemini[Google Generative AI]

  Backend -->|Metrics| Prometheus[Prometheus]
  Prometheus -->|Dashboards| Grafana[Grafana]
```

### Core request/processing responsibilities

- **Frontend**: UI and calling REST APIs. It does token refresh in client-side JS when backend returns 401.
- **Backend**: CRUD endpoints, authentication, event publishing, and metrics.
- **Worker**: Consumes events, runs AI analysis, updates persistence.
- **Prometheus/Grafana**: Provides metrics visibility.

### Incident processing pipeline (Mermaid)

```mermaid
sequenceDiagram
  participant U as User
  participant F as Frontend
  participant B as Backend (FastAPI)
  participant DB as PostgreSQL
  participant MQ as RabbitMQ
  participant W as Worker
  participant AI as Gemini

  U->>F: Create incident (title/description/status/severity)
  F->>B: POST /api/v1/incidents/
  B->>DB: Insert Incident row
  B->>MQ: Publish {event:"incident.created", payload:{incident_id}}
  MQ->>W: Deliver message from queue incidents.events
  W->>DB: Load Incident by id
  W->>DB: Load last 50 LogEntry rows for incident_id
  W->>AI: generate_content(prompt) (only if GOOGLE_API_KEY configured)
  AI-->>W: analysis text
  W->>DB: Append analysis to Incident.description and commit
  B-->>F: GET /api/v1/incidents/{id} reflects updated description
```

---

## System Design

This section maps directly to code-level behavior.

### Request flow (Mermaid)

```mermaid
flowchart LR
  A[Browser] --> B[FastAPI Router /api/v1]
  B --> C[Dependency: get_db()]
  B --> D[Dependency: get_current_user()]
  B --> E[Service layer (IncidentService/LogService/etc.)]
  E --> F[Repository layer (BaseRepository + table-specific repos)]
  F --> G[AsyncSession -> PostgreSQL]
  E --> H[Optional: EventBus.publish_incident_created()]
  H --> I[RabbitMQ queue incidents.events]
  B --> J[Response JSON (Pydantic schemas)]
```

### Authentication flow (Mermaid)

```mermaid
sequenceDiagram
  participant U as User
  participant F as Frontend JS
  participant B as Backend

  U->>F: Enter email + password
  F->>B: POST /api/v1/auth/login (OAuth2PasswordRequestForm)
  B->>B: AuthService.authenticate(email,password)
  B->>B: verify_password (SHA-256 prehash + bcrypt)
  B-->>F: {access_token, refresh_token, token_type}

  Note over F: Token refresh is handled client-side.

  F->>B: Call any protected endpoint with Authorization: Bearer <access_token>
  B->>B: get_current_user() decodes JWT
  B-->>F: 401 if expired/invalid

  F->>B: POST /api/v1/auth/refresh with refresh_token (OAuth2 scheme)
  B-->>F: new {access_token, refresh_token}
```

### Incident processing flow (Mermaid)

```mermaid
sequenceDiagram
  participant API as Backend API
  participant MQ as RabbitMQ
  participant W as Worker
  participant DB as Database

  API->>API: POST /api/v1/incidents/ creates incident
  API->>MQ: event=incident.created payload={incident_id}
  MQ->>W: message delivery
  W->>DB: SELECT incident by PK
  W->>DB: SELECT last 50 LogEntry where incident_id = <id>
  W->>W: AIClient.analyze_incident(incident, log_text)
  W->>DB: UPDATE Incident.description append "[AI Analysis]"\n+ analysis
  W-->>MQ: ack message (via message.process())
```

### AI processing flow (Mermaid)

```mermaid
graph TD
  A[Worker receives incident.created] --> B[Load incident + recent logs]
  B --> C{GOOGLE_API_KEY configured?}
  C -- "empty/dummy" --> D[Return dummy analysis text]
  C -- "real key" --> E[google.generativeai configure(api_key)]
  E --> F[GenerativeModel gemini-1.5-flash]
  F --> G[generate_content(prompt)]
  G --> H[Persist analysis appended to Incident.description]
```


### Monitoring flow (Mermaid)

```mermaid
sequenceDiagram
  participant Prom as Prometheus
  participant B as Backend
  participant G as Grafana

  Prom->>B: Scrape GET /metrics
  B-->>Prom: prometheus-fastapi-instrumentator metrics
  Prom-->>G: Data source queries
  G-->>User: Visualizations from provisioned dashboards
```

---

## Screenshots

All screenshots referenced below are present in this repo under `assets/`.

- Login screen: `assets/Login.png`
- Dashboard screen: `assets/Dashboard.png`
- New incident creation: `assets/New Incident Creation.png`
- AI analysis screen: `assets/AI Analysis.png`
- Docker compose running: `assets/Docker Compose Running.png`
- Swagger UI - page 1: `assets/Swagger UI_page-1.jpg`
- Swagger UI - page 2: `assets/Swagger UI_page-2.jpg`

Markdown references:

- ![Login](assets/Login.png)
- ![Dashboard](assets/Dashboard.png)
- ![New Incident Creation](assets/New%20Incident%20Creation.png)
- ![AI Analysis](assets/AI%20Analysis.png)
- ![Docker Compose Running](assets/Docker%20Compose%20Running.png)
- ![Swagger UI page 1](assets/Swagger%20UI_page-1.jpg)
- ![Swagger UI page 2](assets/Swagger%20UI_page-2.jpg)

---

## Technology Stack

This list is grounded in the code and configuration in the repo.

### Backend: FastAPI

- **What it does**: Hosts API routes under `/api/v1` and provides `/health` plus OpenAPI/Swagger.
- **Why chosen**:
  - Strong async support.
  - Built-in dependency injection.
  - Integrates cleanly with Prometheus instrumentation.
- **Where used**:
  - `backend/app/main.py`
  - `backend/app/api/v1/*.py` route modules

### Async SQLAlchemy

- **What it does**: Async database access via async engine and AsyncSession.
- **Why chosen**:
  - Avoid blocking IO for concurrent API requests.
  - Worker also uses async patterns.
- **Where used**:
  - `backend/app/core/database.py`
  - services/repositories under `backend/app/services` and `backend/app/repositories`

### PostgreSQL

- **What it does**: Persistent storage for all domain tables.
- **Why chosen**:
  - Production-grade relational model.
  - Strong ecosystem for SQLAlchemy.
- **Where used**:
  - `docker-compose.yml`
  - `backend/alembic/*`
  - `backend/app/models/*`

### Redis (runtime wired)

- **What it does**: Provides `redis_client` and connection used at backend startup (`lifespan`).
- **Why chosen**:
  - Enables caching/blacklists/fast ephemeral state patterns (client exists; use can be extended).
- **Where used**:
  - `backend/app/utils/redis.py`
  - `backend/app/main.py` calls `redis_client.ping()` on startup.

### RabbitMQ (event bus)

- **What it does**: Delivers asynchronous events to workers.
- **Why chosen**:
  - Durable event queue for incident processing.
  - Decouples API latency from AI compute.
- **Where used**:
  - `backend/app/utils/queue.py` for publishing
  - `backend/app/services/event_bus.py` for incident.created event
  - `worker/src/consumer.py` for queue consumption

### Worker: aio-pika

- **What it does**: Robust AMQP connection and message consumption.
- **Where used**:
  - `worker/src/consumer.py`

### AI: Google Generative AI (Gemini)

- **What it does**: Produces analysis text from incident + logs.
- **Why chosen**:
  - Natural language generation for root cause and remediation suggestions.
- **Where used**:
  - `worker/src/ai_client.py` (Gemini integration + dummy mode)
  - `backend/app/services/ai.py` also exists but may be unused by current worker flow.

### JWT (via jose)

- **What it does**: Access/refresh token signing and verification.
- **Why chosen**:
  - Compact and standard approach.
- **Where used**:
  - `backend/app/core/security.py`
  - `backend/app/api/deps.py` decodes tokens

### Prometheus + Grafana

- **What they do**:
  - Prometheus scrapes metrics from backend `/metrics`.
  - Grafana uses provisioning to load dashboards.
- **Where used**:
  - `monitoring/prometheus/prometheus.yml`
  - `monitoring/grafana/provisioning/*`
  - `monitoring/grafana/dashboards/ai-ops-overview.json`

### Docker / Docker Compose

- **What they do**: Build and run all services.
- **Where used**:
  - `backend/Dockerfile`, `worker/Dockerfile`, `frontend/Dockerfile`
  - `docker-compose.yml`

### Kubernetes

- **What it does**: Provides deployment scaffolding for backend/worker/services.
- **Where used**:
  - `k8s/*.yaml`

---

## Repository Structure

```text
backend/
  Dockerfile
  requirements.txt
  alembic/                     # schema migrations
  app/
    main.py                    # FastAPI app + lifespan
    api/
      deps.py                  # JWT dependency helpers
      v1/
        auth.py                # register/login/refresh
        incidents.py           # incident CRUD + event publish
        logs.py                # log list/create/get
        alerts.py              # alert CRUD
        dashboards.py         # dashboard widget list/create
    core/
      config.py               # Settings (env vars)
      database.py             # Async SQLAlchemy engine + get_db
      security.py             # JWT + bcrypt password hashing
      exceptions.py
    models/
      base.py                 # Base ORM class
      user.py
      incident.py
      log.py
      alert.py
      dashboard.py
    repositories/
      base.py                 # generic repository patterns
      user.py
      incident.py
      log.py
      alert.py
      dashboard.py
    schemas/
      auth.py
      incident.py
      log.py
      alert.py
      dashboard.py
    services/
      auth.py
      incident.py
      log.py
      alert.py
      dashboard.py
      ai.py                    # Gemini dummy/real integration (not used in current worker flow)
      event_bus.py             # publishes incident.created
    utils/
      queue.py                 # RabbitMQ publisher
      redis.py                 # Redis async client wrapper
      __init__.py
  tests/
    test_auth.py
    test_incidents.py
    test_ai.py

worker/
  Dockerfile
  requirements.txt
  src/
    main.py                    # runs start_consumer
    consumer.py                # aio-pika queue consumer
    handlers.py                # incident.created handler: loads incident, logs, calls AI
    ai_client.py               # dummy mode / Gemini call

frontend/
  Dockerfile
  nginx.conf
  index.html
  css/
  js/

monitoring/
  prometheus/prometheus.yml
  grafana/provisioning/
    datasources/datasource.yml
    dashboards/dashboard.yml
  grafana/dashboards/ai-ops-overview.json

k8s/
  namespace.yaml
  ingress.yaml
  *-deployment.yaml
  *-service.yaml

aws/
  ec2-setup.sh
  deployment.yaml

.github/workflows/
  ci.yml
  deploy.yml

docs/
  API.md
  architecture.md

docker/
  nginx/nginx.conf
```

---

## Prerequisites

### Local machine prerequisites

- Docker Desktop (or Docker Engine + docker-compose plugin)
- Python 3.11 (for running tests or standalone code)
- Network access to pull Docker images

### Credentials prerequisites

- If you want real Gemini analysis:
  - Set `GOOGLE_API_KEY` to a valid Google API key.

### Tooling assumptions (based on repo)

- Lint uses `flake8`
- Tests use `pytest` + `pytest-asyncio`

---

## Local Development Setup

This section provides a complete runbook for local development using **only repo artifacts**.

### 1) Configure environment variables

This repo’s runtime uses environment variables through `backend/app/core/config.py` and docker-compose.

Key runtime env vars in this repo:

- `DATABASE_URL`
- `REDIS_URL`
- `RABBITMQ_URL`
- `SECRET_KEY`
- `GOOGLE_API_KEY`
- `CORS_ORIGINS`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `ENVIRONMENT`

> The repo references `.env` in the Settings config (`env_file = ".env"`).

#### Local `.env` file (recommended)

Create a file at the repo root named `.env`.

```bash
# Identity
SECRET_KEY=change-me

# Datastores (default compose values)
DATABASE_URL=postgresql+asyncpg://aiops:aiops@postgres:5432/aiops
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672//

# AI
GOOGLE_API_KEY=dummy

# CORS
CORS_ORIGINS=*

# Token lifetimes
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment label
ENVIRONMENT=development
```

Notes:
- Use `GOOGLE_API_KEY=dummy` to enable deterministic dummy mode.
- For real Gemini calls, set `GOOGLE_API_KEY` to an actual key.

### 2) Start the full stack with Docker Compose

From repository root:

```bash
docker compose up -d --build
```

This brings up:

- `postgres`
- `redis`
- `rabbitmq`
- `backend`
- `worker`
- `frontend`
- `prometheus`
- `grafana`

### 3) Validate core health endpoints

Backend:

```bash
curl -s http://localhost:8000/health
```

Expected:

```json
{"status":"ok"}
```

Metrics:

```bash
curl -s http://localhost:8000/metrics | head
```

Expected:
- Prometheus metrics text output

### 4) Open UIs

- Frontend (static UI): http://localhost:8080
- Backend Swagger UI: http://localhost:8000/docs
- RabbitMQ management UI: http://localhost:15672
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

### 5) Create test data via UI (recommended)

- Register a user in the UI
- Log in
- Create an incident
- Create logs (if desired) and view incident details

### 6) Run backend-only locally (optional)

If you want to run without Docker, the repo already supports Python requirements.

Backend local run (from repo root):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Important:
- When running backend locally, you must ensure `PYTHONPATH` is correct so `app.*` imports resolve.
- Docker solves this; locally you may need:

```bash
export PYTHONPATH=backend
```

Then:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 7) Run worker locally (optional)

Worker local run:

```bash
cd worker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

Worker expects backend package importable:
- The worker code modifies `sys.path` to include backend root enough to import `app.core.config`.

If you run from a different working dir, replicate Docker’s import context.

---

## Environment Variables

This section lists every environment variable defined or referenced in the repo’s configuration and deployments.

### Backend configuration (`backend/app/core/config.py`)

`Settings` class defines the following variables:

| Variable | Type | Default | Used for | Security considerations |
|---|---:|---|---|---|
| `DATABASE_URL` | str | `postgresql+asyncpg://aiops:aiops@postgres:5432/aiops` | Async SQLAlchemy connection | Use a least-privileged DB user in production |
| `REDIS_URL` | str | `redis://redis:6379/0` | Redis async client | Use protected Redis (ACL/TLS) in production |
| `RABBITMQ_URL` | str | `amqp://guest:guest@rabbitmq:5672//` | aio-pika robust connection | Avoid guest credentials in production |
| `SECRET_KEY` | str | `super-secret-key` | JWT signing key | Must be long + secret; rotate safely |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | 30 | Access token TTL | Short TTL reduces risk |
| `REFRESH_TOKEN_EXPIRE_DAYS` | int | 7 | Refresh token TTL | Refresh token revocation strategy not implemented |
| `GOOGLE_API_KEY` | str | `""` | Gemini integration | Don’t log/ship secrets; use K8s secrets/CI secrets |
| `CORS_ORIGINS` | List[str] | `["*"]` | FastAPI CORS middleware | In production, set explicit origins |
| `ENVIRONMENT` | str | `development` | Runtime label | Not security-critical |

Also note:

- `Settings.Config.env_file = ".env"` means `.env` is expected at repo root.

### Docker Compose env wiring (`docker-compose.yml`)

Compose references `${SECRET_KEY}` and `${GOOGLE_API_KEY}` for the backend container.

Backend container environment:

- `SECRET_KEY: ${SECRET_KEY}`
