# AI Ops Dashboard (AI Incident Analyzer)

Real-time incident management dashboard with AI-powered root cause analysis.

## Features
- Incident lifecycle management (create, update, resolve)
- Log aggregation and correlation
- AI-driven analysis using OpenAI GPT
- Customizable dashboards with widgets
- Alert rules and notifications
- JWT authentication
- RabbitMQ event-driven architecture
- Prometheus & Grafana monitoring
- Docker Compose and Kubernetes deployments

## Quick Start
1. Clone repo: `git clone https://github.com/yourorg/ai-ops-dashboard.git`
2. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
3. Run `docker-compose up -d`
4. Access frontend at http://localhost:8080
5. Grafana at http://localhost:3000 (admin/admin)

## Architecture
See `docs/architecture.md`

## API Documentation
See `docs/API.md`