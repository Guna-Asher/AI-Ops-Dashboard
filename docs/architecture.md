# Architecture

## System Diagram
[ASCII art diagram]

Components:
- Frontend: Nginx serving static files, calls API
- Backend: FastAPI, async SQLAlchemy, PostgreSQL
- Worker: Consumes RabbitMQ events, calls OpenAI for analysis
- Redis: Token blacklist/cache
- RabbitMQ: Event queue for async processing
- Prometheus & Grafana: Monitoring