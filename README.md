```markdown
# 🤖 AI Ops Dashboard (AI Incident Analyzer)

An enterprise‑grade, real‑time incident management platform powered by **Google Gemini**.  
Built with **FastAPI**, **RabbitMQ**, **PostgreSQL**, **Redis**, **Prometheus/Grafana**, and **Docker Compose**.

<p align="center">
  <img src="docs/screenshots/dashboard.png" alt="Dashboard" width="800" />
</p>

---

## 1. Project Overview

**AI Ops Dashboard** enables engineering teams to:

- **Create, track, and resolve** production incidents.
- **Automatically analyse** incidents using Google Gemini AI (via a RabbitMQ‑based worker).
- **Aggregate logs** and correlate them with ongoing incidents.
- **Monitor system health** with pre‑configured Prometheus metrics and Grafana dashboards.
- **Define custom alert rules** for automated notifications.

The project solves the problem of lengthy incident triage by providing **instant AI‑generated root cause analyses** directly in the incident timeline.

### Why This Project Exists

Modern SRE/Ops teams spend hours correlating logs and metrics to diagnose incidents. This tool shortens the feedback loop by:

- Automatically pulling relevant log data.
- Sending it together with incident metadata to a large language model.
- Injecting the analysis back into the incident, enabling engineers to act immediately.

---

## 2. Project Highlights

- ✅ Production‑grade authentication with JWT access/refresh tokens.
- ✅ Fully asynchronous backend (FastAPI + async SQLAlchemy + asyncpg).
- ✅ Event‑driven architecture via RabbitMQ (incident analysis runs out‑of‑band).
- ✅ AI provider abstraction – supports both Google Gemini (default) and a configurable **dummy mode** for offline testing.
- ✅ Complete monitoring stack – Prometheus metrics exposed by the backend, Grafana dashboard pre‑provisioned.
- ✅ Containerised with Docker Compose, ready for Kubernetes (manifests provided).
- ✅ CI/CD pipeline with GitHub Actions (lint, test, build, deploy to AWS EC2).
- ✅ Database migrations with Alembic.
- ✅ Redis caching layer ready for token blacklisting, session storage, etc.
- ✅ RBAC (superuser/normal user) implemented.

---

## 3. System Architecture

### High‑Level Architecture (Mermaid)

```mermaid
graph TD
  subgraph Client
    FE[Frontend (Nginx + HTML/JS)]
  end

  subgraph Docker Network
    API[Backend (FastAPI)]
    PGSQL[(PostgreSQL)]
    REDIS[(Redis)]
    RABBIT[RabbitMQ]
    WORKER[Worker (Python)]
    PROM[Prometheus]
    GRAFANA[Grafana]
  end

  FE -->|HTTP / REST| API
  API --> PGSQL
  API --> REDIS
  API --> RABBIT
  RABBIT --> WORKER
  WORKER --> PGSQL
  WORKER --> AI[Google Gemini AI]
  PROM --> API
  GRAFANA --> PROM
```

### Request Flow (Incident Analysis)

1. User creates an incident via the frontend (or API).
2. Backend persists the incident to PostgreSQL and publishes an `incident.created` event to RabbitMQ.
3. The worker picks up the event, fetches the incident & related logs, sends them to Google Gemini.
4. The worker writes the AI analysis back to the incident’s `description` field.
5. User sees the analysis in real‑time (refresh the incident detail).

---

## 4. Tech Stack

| Category              | Technology                 | Purpose                                      | Why Chosen |
|-----------------------|----------------------------|----------------------------------------------|------------|
| Backend Framework     | FastAPI                    | REST API, dependency injection, auto‑docs    | High performance, async, OpenAPI built‑in |
| ORM                   | SQLAlchemy (async)         | Database access                              | Mature, async support, Alembic integration |
| Database              | PostgreSQL                 | Persistent storage                           | Reliability, JSON fields, full‑text search |
| Cache                 | Redis                      | Caching, token blacklisting                  | In‑memory, simple integration |
| Message Queue         | RabbitMQ                   | Decouple incident creation from AI analysis  | Reliable, widely adopted, management UI |
| AI Provider           | Google Gemini              | Root‑cause analysis                           | Free tier available, competitive quality |
| Worker                | Python + aio‑pika          | Process AI jobs asynchronously               | Lightweight, same language as backend |
| Frontend              | HTML / CSS / Vanilla JS    | User interface                               | Zero dependencies, fast delivery |
| Monitoring            | Prometheus + Grafana       | Metrics & dashboards                         | Industry standard, pre‑built integrations |
| Containerisation      | Docker, Docker Compose     | Consistent dev/prod environments             | Reproducibility, ease of deployment |
| CI/CD                 | GitHub Actions             | Automated testing & deployment               | Native integration, free for public repos |
| Cloud Deployment      | AWS EC2                    | Production hosting                           | Scalable, customisable |
| Orchestration (opt.)  | Kubernetes                 | Production scaling                           | Manifests provided |

---

## 5. Folder Structure

```
.
├── .github/workflows/          # CI/CD (lint, test, deploy)
├── aws/                        # AWS EC2 user data & CloudFormation snippet
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/                # Database migration scripts
│   ├── app/
│   │   ├── api/v1/             # Route handlers (auth, incidents, logs, dashboards, alerts)
│   │   ├── core/               # Configuration, security (JWT, password hashing)
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── repositories/       # Data access layer (async SQLAlchemy)
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Business logic (auth, incident, AI, alerts, event bus)
│   │   └── utils/              # Redis client, RabbitMQ client
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── css/                    # Styling
│   └── js/                     # Frontend logic (API calls, UI)
├── worker/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/                    # Consumer, handlers, AI client
├── monitoring/
│   ├── prometheus/prometheus.yml
│   └── grafana/provisioning/   # Datasources & dashboards
├── docker/nginx/               # Additional Nginx config (reverse proxy)
├── k8s/                        # Kubernetes manifests
├── docs/                       # Architecture & API documentation
├── .env.example                # Template for environment variables
├── docker-compose.yml
└── README.md
```

---

## 6. Prerequisites

- **OS**: Linux, macOS, Windows (with Docker Desktop)
- **Docker Engine** ≥ 20.10, **Docker Compose** v2
- **Git**
- A Google AI Studio API key (or set `GOOGLE_API_KEY=dummy` for offline mode)
- 2 GB free disk space for Docker images
- Open ports: `8080`, `8000`, `3000`, `9090`, `15672`

---

## 7. Local Development Setup

### 7.1 Clone & Configure

```bash
git clone https://github.com/yourorg/ai-ops-dashboard.git
cd ai-ops-dashboard
cp .env.example .env
```

Edit `.env` and set at least:
- `SECRET_KEY` (generate with `openssl rand -hex 32`)
- `GOOGLE_API_KEY` (or `dummy` for offline mode)

### 7.2 Build and Start All Services

```bash
docker compose up -d --build
```

This will:
- Build the backend, worker, and frontend images.
- Pull official images for PostgreSQL, Redis, RabbitMQ, Prometheus, Grafana.
- Start all containers in detached mode.

### 7.3 Verify

```bash
docker compose ps
```

All 8 containers should show `Up`.

### 7.4 Create a User & Test the Pipeline

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"strongpass"}'

# Login to get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin@example.com&password=strongpass" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Create incident
curl -X POST http://localhost:8000/api/v1/incidents/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"High CPU on prod-01","description":"CPU 99% for 10 min","severity":"high"}'

# Check incident after 5 seconds
curl http://localhost:8000/api/v1/incidents/1 -H "Authorization: Bearer $TOKEN"
```

The description should now contain `[AI Analysis]` with either a dummy or real analysis.

---

## 8. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | `super-secret-key` | Used to sign JWT tokens |
| `GOOGLE_API_KEY` | Yes | `""` | Google AI Studio API key (or `dummy`) |
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...` | Database connection string |
| `REDIS_URL` | Yes | `redis://redis:6379/0` | Redis connection |
| `RABBITMQ_URL` | Yes | `amqp://guest:guest@rabbitmq:5672//` | RabbitMQ connection |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | No | `7` | Refresh token lifetime |
| `CORS_ORIGINS` | No | `["*"]` | Allowed origins (for development) |

Example `.env`:
```env
SECRET_KEY=super-secret-key
GOOGLE_API_KEY=dummy
DATABASE_URL=postgresql+asyncpg://aiops:aiops@postgres:5432/aiops
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672//
```

---

## 9. Database Setup

**Why PostgreSQL?**  
It supports JSON fields, async drivers, full‑text search, and is battle‑tested for production.

### Schema Overview

- `users` – authentication & user profiles.
- `incidents` – core incident data (title, description, status, severity).
- `logs` – log entries linked to incidents.
- `alerts` – configurable alert rules.
- `dashboard_widgets` – user‑customisable widgets.

### Migrations

Alembic migrations are available under `backend/alembic/versions/`.  
On startup, the backend **automatically creates tables** if they don’t exist. For production, you can run migrations manually:

```bash
docker compose exec backend alembic upgrade head
```

### Backup & Restore

```bash
# Backup
docker compose exec postgres pg_dump -U aiops aiops > backup.sql

# Restore
docker compose exec -T postgres psql -U aiops aiops < backup.sql
```

---

## 10. Authentication & Authorization

### Login & Registration Flow

1. User registers with email + password (password is hashed with bcrypt + SHA‑256).
2. On login, an access token (JWT) and a refresh token are returned.
3. All protected endpoints require `Authorization: Bearer <access_token>`.
4. When the access token expires, the client can use the `/auth/refresh` endpoint to obtain a new pair.

### Password Rules

- No length restrictions (bcrypt handles up to 72 bytes, extended by SHA‑256 pre‑hashing).
- Email is validated as a valid email address via `email-validator`.

### User Roles

- `is_superuser` flag – only superusers can delete incidents.

---

## 11. API Documentation

Interactive Swagger UI is available at **`http://localhost:8000/docs`**.

### Endpoints Overview

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login and receive tokens | No |
| POST | `/api/v1/auth/refresh` | Refresh tokens | Refresh token |
| GET | `/api/v1/incidents/` | List incidents | Yes |
| POST | `/api/v1/incidents/` | Create incident | Yes |
| GET | `/api/v1/incidents/{id}` | Get incident detail | Yes |
| PUT | `/api/v1/incidents/{id}` | Update incident | Yes |
| DELETE | `/api/v1/incidents/{id}` | Delete incident | Yes (superuser) |
| GET | `/api/v1/logs/` | List logs (optional filter by incident) | Yes |
| POST | `/api/v1/logs/` | Create log entry | Yes |
| GET | `/api/v1/alerts/` | List alerts | Yes |
| POST | `/api/v1/alerts/` | Create alert | Yes |
| PUT | `/api/v1/alerts/{id}` | Update alert | Yes |
| DELETE | `/api/v1/alerts/{id}` | Delete alert | Yes |
| GET | `/api/v1/dashboards/widgets` | Get user widgets | Yes |
| POST | `/api/v1/dashboards/widgets` | Create widget | Yes |

### Example: Create Incident

**Request**
```bash
curl -X POST http://localhost:8000/api/v1/incidents/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Server down","description":"Server is unreachable","severity":"critical"}'
```
**Response** `201 Created`
```json
{
  "id": 1,
  "title": "Server down",
  "description": "Server is unreachable",
  "status": "open",
  "severity": "critical",
  "assigned_to": 1,
  "created_at": "2026-06-03T12:00:00Z",
  "updated_at": null
}
```

For full details, see `docs/API.md`.

---

## 12. Running with Docker

All services are orchestrated via `docker-compose.yml`.

```bash
docker compose up -d                    # start everything
docker compose build --no-cache backend  # rebuild backend image
docker compose logs backend             # view logs
docker compose down                     # stop and remove containers
docker compose down -v                  # also remove volumes (data)
```

---

## 13. Deployment Guide

### AWS EC2 (Simplified)

1. Launch an Ubuntu EC2 instance (t3.medium or larger).
2. Run the provided `aws/ec2-setup.sh` as user data or manually.
3. Ensure your security group allows inbound traffic on ports 80, 443, 22.
4. Set environment variables (including `GOOGLE_API_KEY`) on the host.
5. Start with `docker compose up -d`.

### Kubernetes

Manifests are provided in `k8s/`. Customise the images and secrets, then apply:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

---

## 14. CI/CD Pipeline

Defined in `.github/workflows/ci.yml` and `deploy.yml`.

- **CI**: runs on every push/PR to `main`/`develop`.  
  - Lints with flake8.  
  - Runs pytest tests against a real PostgreSQL instance.
- **Deploy**: triggered by version tags (`v*`).  
  - Builds and pushes Docker images to Docker Hub.  
  - SSHs into EC2 instance and restarts the stack.

---

## 15. Monitoring & Logging

- **Prometheus** scrapes metrics from the backend’s `/metrics` endpoint (provided by `prometheus-fastapi-instrumentator`).
- **Grafana** dashboard **“AI Ops Overview”** is auto‑provisioned (login `admin/admin`).
- Backend logs are streamed to stdout and can be viewed with `docker compose logs`.
- For production, consider shipping logs to CloudWatch or an ELK stack.

---

## 16. Security Considerations

- **Passwords**: SHA‑256 hashed before bcrypt to avoid bcrypt’s 72‑byte limit and any NULL byte issues.
- **JWT**: signed with HS256, secret stored in environment variable.
- **CORS**: configured to limit origins in production.
- **Input Validation**: Pydantic v2 schemas enforce strict typing.
- **Rate Limiting**: not yet implemented – consider adding with Redis.

---

## 17. Performance Optimizations

- **Async throughout**: asyncpg, async SQLAlchemy, aio‑pika for RabbitMQ.
- **Connection pooling**: backend uses SQLAlchemy’s pool (20 base connections).
- **Caching**: Redis client is ready for use (e.g., token blacklisting, heavy queries).

---

## 18. Troubleshooting Guide

### Problem: Backend crashes with `AttributeError: 'Settings' object has no attribute 'GOOGLE_AI_STUDIO_MODEL'`
**Root Cause**: The worker’s AI client mistakenly used `settings.GOOGLE_AI_STUDIO_MODEL` instead of `settings.GOOGLE_API_KEY`.  
**Solution**: Updated `worker/src/ai_client.py` to use `settings.GOOGLE_API_KEY` and removed the invalid attribute.  
**Prevention**: Always verify config keys against `backend/app/core/config.py`.

### Problem: `ImportError: email-validator is not installed`
**Root Cause**: Pydantic v2’s `EmailStr` requires `email-validator`.  
**Solution**: Added `email-validator>=2.0.0` to `backend/requirements.txt`.  
**Prevention**: When using Pydantic v2 email fields, include this dependency.

### Problem: Bcrypt `ValueError: password cannot be longer than 72 bytes`
**Root Cause**: Passlib’s bcrypt backend is incompatible with bcrypt ≥ 4.0.  
**Solution**: Replaced Passlib with direct bcrypt usage and added SHA‑256 pre‑hashing to ensure input is always ≤ 64 bytes.  
**Prevention**: Pin bcrypt version or avoid Passlib.

### Problem: `Integer = character varying` error during user lookup
**Root Cause**: JWT `sub` is a string, but `users.id` is an integer. SQLAlchemy’s asyncpg driver threw a type mismatch.  
**Solution**: Explicitly cast `token_data.sub` to `int` in `deps.py`.  
**Prevention**: Always ensure JWT payload types match database column types.

### Problem: Worker Docker build failing because of context
**Root Cause**: Worker’s Dockerfile used relative paths (`COPY requirements.txt .`) while build context was set to `./worker`.  
**Solution**: Changed `docker-compose.yml` to set context to `.` and Dockerfile to `worker/Dockerfile`, then adjusted all COPY paths to be relative to project root.  
**Prevention**: When using multi‑stage builds with custom contexts, always check the working directory.

---

## 19. Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed to connect to localhost port 8000` | Backend container not running | `docker compose ps`, check backend logs |
| `ModuleNotFoundError: No module named 'backend'` in worker | Incorrect worker Dockerfile COPY paths | Use full paths relative to project root |
| `GOOGLE_API_KEY is not set` | Missing environment variable | Set in `.env` or Docker Compose environment |
| AI analysis not appearing | Worker not processing or API key invalid | `docker compose logs worker`, verify `GOOGLE_API_KEY` |
| Registration returns `Internal Server Error` | Bcrypt compatibility or missing dependency | Update `security.py` to use bcrypt directly |

---

## 20. Testing

### Run Backend Tests

```bash
docker compose exec backend pytest --asyncio-mode=auto
```

### Manual Testing

- Use the Swagger UI at `/docs` to explore endpoints.
- Monitor worker logs after creating an incident.

---

## 21. Production Readiness Checklist

- [x] JWT authentication with refresh tokens
- [x] Database migration support (Alembic)
- [x] Monitoring (Prometheus + Grafana)
- [x] Containerised deployment (Docker Compose + Kubernetes)
- [x] CI/CD with automated tests
- [x] Environment variable configuration
- [ ] Rate limiting
- [ ] Horizontal scaling (worker replicas)
- [ ] Secrets management (Vault/Cloud Secrets)
- [ ] End‑to‑end tests

---

## 22. Future Improvements

- **Real‑time updates** via WebSockets for live incident feeds.
- **Incident auto‑closing** based on AI confidence.
- **Integrations** with PagerDuty, Slack, Jira.
- **Multi‑tenant** support with organisation isolation.
- **LLM failover** – fallback to another AI provider if Gemini is unavailable.

---

## 23. Lessons Learned

- **Event‑driven architecture** decouples heavy AI calls from the API, improving response times.
- **Async Python** (FastAPI + asyncpg) dramatically reduces latency under load.
- **Docker Compose** makes local development painless but requires careful context management.
- **Bcrypt compatibility** issues with newer library versions can be avoided by using direct bcrypt calls.
- **Pydantic v2** is stricter about email validation; always install `email-validator`.
- **JWT claims** must match the database column types to avoid SQL type errors.

---

## 24. Resume & Interview Talking Points

- **Architecture**: “I designed an event‑driven AI ops platform using FastAPI, RabbitMQ, and PostgreSQL. Incidents are analysed asynchronously by a separate worker that calls Google Gemini.”
- **Production readiness**: “The system includes JWT auth, monitoring with Prometheus/Grafana, Docker/K8s deployment, and a CI/CD pipeline.”
- **Troubleshooting skills**: “I encountered and resolved several production‑grade issues – bcrypt compatibility, type mismatches, Docker context problems – ensuring a stable release.”
- **Scalability**: “The worker can be scaled independently. Redis is ready for caching, and Kubernetes manifests are provided for cluster deployment.”

---

## 25. Screenshots Section

*Add your own screenshots in `docs/screenshots/` and reference them here.*

- `docs/screenshots/login.png` – Login page
- `docs/screenshots/incidents-list.png` – Incident list with status badges
- `docs/screenshots/incident-detail.png` – Incident detail with AI analysis block
- `docs/screenshots/dashboard.png` – Dashboard with widgets
- `docs/screenshots/grafana.png` – Grafana “AI Ops Overview” dashboard

---

## 26. Contributing Guide

- Branch naming: `feature/description`, `fix/description`
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/)
- Pull requests require passing CI and at least one review.

---

## 27. License

MIT License – see `LICENSE` file (if present).

---

**Built with passion by a Senior DevOps/Backend Engineer**  
*Ready for production, interview, and beyond.*
```