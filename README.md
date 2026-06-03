# 🤖 AI Ops Dashboard (Enterprise Portfolio Edition)

> AI-Powered Incident Management, Root Cause Analysis, Observability, and Event-Driven Operations Platform

## Executive Summary

AI Ops Dashboard is a production-style platform designed to demonstrate modern Backend Engineering, DevOps, SRE, Distributed Systems, and AI integration practices.

The system enables teams to create incidents, collect logs, trigger asynchronous AI-powered analysis using Google Gemini through RabbitMQ workers, and monitor the entire platform using Prometheus and Grafana.

### Key Engineering Areas Demonstrated

- FastAPI Backend Development
- Async Python
- PostgreSQL + SQLAlchemy
- Redis Integration
- RabbitMQ Event-Driven Architecture
- AI Integration (Google Gemini)
- Docker & Docker Compose
- Kubernetes Readiness
- Monitoring & Observability
- CI/CD Automation
- AWS Deployment Patterns
- Production Troubleshooting

---

# Quick Start

```bash
git clone <repository-url>
cd AI-Ops-Dashboard

cp .env.example .env

docker compose up -d --build
```

### Open Services

| Service | URL |
|----------|------|
| Frontend | http://localhost:8080 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| RabbitMQ UI | http://localhost:15672 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

---

# Architecture

```mermaid
graph TD

User --> Frontend

Frontend --> FastAPI

FastAPI --> PostgreSQL
FastAPI --> Redis
FastAPI --> RabbitMQ

RabbitMQ --> Worker

Worker --> Gemini

Prometheus --> FastAPI
Grafana --> Prometheus
```

## Incident Processing Flow

```mermaid
sequenceDiagram

User->>Frontend: Create Incident
Frontend->>Backend: POST Incident
Backend->>PostgreSQL: Save Incident
Backend->>RabbitMQ: Publish Event

RabbitMQ->>Worker: Consume Event
Worker->>PostgreSQL: Fetch Data
Worker->>Gemini: Request Analysis
Gemini-->>Worker: Analysis

Worker->>PostgreSQL: Save Result

User->>Backend: Fetch Incident
Backend-->>User: Incident + AI Analysis
```

---

# Technology Stack

- FastAPI
- SQLAlchemy Async
- AsyncPG
- PostgreSQL
- Redis
- RabbitMQ
- aio-pika
- Google Gemini
- Prometheus
- Grafana
- Docker
- Docker Compose
- Kubernetes
- GitHub Actions
- AWS EC2

---

# Repository Structure

```text
backend/
frontend/
worker/
monitoring/
k8s/
aws/
docker/
.github/
docs/
```

## Backend

Contains:

- Authentication
- Incident Management
- Alert APIs
- Dashboard APIs
- Log APIs
- Event Publishing
- Security Utilities

## Worker

Responsible for:

- Consuming RabbitMQ messages
- Communicating with Gemini
- Updating incidents with AI analysis

---

# Environment Variables

```env
DATABASE_URL=postgresql+asyncpg://aiops:aiops@localhost:5432/aiops
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672//
SECRET_KEY=change-me
GOOGLE_API_KEY=your-key
```

---

# User Authentication

## Registration

```http
POST /api/v1/auth/register
```

### Email Requirements

- Must be valid email
- Unique

Example:

```text
admin@example.com
```

### Password Recommendations

- Minimum 8 characters
- Uppercase
- Lowercase
- Number
- Special Character

Example:

```text
StrongPassword123!
```

---

# Core Features

## Incident Management

- Create incidents
- Update incidents
- Delete incidents
- Severity tracking
- Status tracking

## AI Analysis

- Root Cause Analysis
- Suggested Remediation
- Context Enrichment

## Alert Management

- Create alerts
- Update alerts
- Delete alerts

## Dashboard Widgets

- Personalized dashboard configuration

---

# Docker Operations

Start:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

View Logs:

```bash
docker compose logs backend
docker compose logs worker
```

Rebuild:

```bash
docker compose up -d --build
```

---

# Monitoring

## Prometheus

Metrics endpoint:

```text
/metrics
```

## Grafana

Default Login:

```text
Username: admin
Password: admin
```

---

# Health Checks

Backend:

```bash
curl http://localhost:8000/health
```

Postgres:

```bash
docker compose exec postgres pg_isready
```

Redis:

```bash
docker compose exec redis redis-cli ping
```

RabbitMQ:

```bash
docker compose exec rabbitmq rabbitmqctl status
```

---

# Troubleshooting Runbook

## AI Analysis Not Appearing

### Investigation

```bash
docker compose logs worker
```

Check RabbitMQ:

```text
http://localhost:15672
```

Verify API Key:

```bash
docker compose exec worker env | grep GOOGLE
```

---

## Backend Fails To Start

Check:

```bash
docker compose logs backend
```

Common Causes:

- Missing SECRET_KEY
- Invalid DATABASE_URL
- PostgreSQL unavailable

---

## Worker Cannot Consume Messages

Possible Causes:

- RabbitMQ unavailable
- Wrong queue configuration
- Invalid credentials

---

# Known Issues Fixed During Development

### email-validator Missing

Fixed by adding:

```text
email-validator>=2.x
```

### JWT Integer/String Mismatch

Fixed by converting JWT subject values to integer before database queries.

### Worker Docker Context Errors

Fixed by changing build context to project root.

### Bcrypt Compatibility Issues

Fixed through direct bcrypt implementation and SHA256 pre-hashing strategy.

---

# Security Architecture

Authentication:
- JWT Access Tokens
- Refresh Tokens

Authorization:
- Role-Based Access Control

Data Protection:
- Password Hashing
- Environment Variables

Future:
- MFA
- OAuth2
- Vault Integration

---

# Scaling Strategy

Current:

- 1 API
- 1 Worker

Production:

- Multiple API Replicas
- Multiple Worker Replicas
- Load Balancer
- Managed PostgreSQL
- Managed Redis

---

# CI/CD

GitHub Actions:

- Lint
- Test
- Build
- Deploy

Deployment Target:

- AWS EC2

---

# Resume Highlights

This project demonstrates:

✅ Backend Engineering

✅ Distributed Systems

✅ Event-Driven Architecture

✅ AI Integration

✅ Monitoring & Observability

✅ Docker & Kubernetes

✅ Cloud Deployment

✅ Authentication & Authorization

✅ Production Troubleshooting

---

# Interview Talking Points

1. Why RabbitMQ instead of direct AI calls?
2. How does async improve performance?
3. How would you scale workers?
4. How would you handle Gemini downtime?
5. Why Redis?
6. How would you implement rate limiting?
7. How would you deploy on Kubernetes?

---

# Future Roadmap

- WebSockets
- Slack Integration
- Jira Integration
- PagerDuty Integration
- Multi-Tenancy
- AI Provider Failover
- Audit Logs
- Rate Limiting
- SSO

---

# License

MIT

---

Built to showcase Backend Engineering, DevOps, SRE, Cloud, and AI-powered Operations workflows.
