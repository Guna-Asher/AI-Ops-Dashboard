#!/usr/bin/env bash
# Create directory structure
mkdir -p backend/app/api/v1/endpoints
mkdir -p backend/app/core
mkdir -p backend/app/db/models
mkdir -p backend/app/schemas
mkdir -p backend/app/services
mkdir -p backend/worker
mkdir -p backend/tests
mkdir -p backend/alembic/versions

mkdir -p frontend/pages/incidents
mkdir -p frontend/components
mkdir -p frontend/public
mkdir -p frontend/styles

mkdir -p .github/workflows
mkdir -p scripts

# Backend __init__.py files (make them Python packages)
touch backend/app/__init__.py
touch backend/app/api/__init__.py
touch backend/app/api/v1/__init__.py
touch backend/app/api/v1/endpoints/__init__.py
touch backend/app/core/__init__.py
touch backend/app/db/__init__.py
touch backend/app/db/models/__init__.py
touch backend/app/schemas/__init__.py
touch backend/app/services/__init__.py

# Backend core files (empty, will fill later)
touch backend/app/core/config.py
touch backend/app/core/security.py

# Backend db files
touch backend/app/db/base.py
touch backend/app/db/session.py
touch backend/app/db/models/incident.py
touch backend/app/db/models/user.py

# Backend schemas files
touch backend/app/schemas/incident.py
touch backend/app/schemas/user.py

# Backend services
touch backend/app/services/incident_service.py
touch backend/app/services/ai_service.py

# Main FastAPI app
touch backend/app/main.py

# Worker
touch backend/worker/consumer.py
touch backend/worker/ai_analyzer.py

# Backend root files
touch backend/requirements.txt
touch backend/Dockerfile
touch backend/.env.example

# Frontend files
touch frontend/next.config.js
touch frontend/pages/_app.js
touch frontend/pages/index.js
touch frontend/pages/incidents/index.js
touch frontend/pages/incidents/[id].js
touch frontend/components/Layout.js
touch frontend/public/favicon.ico
touch frontend/styles/globals.css
touch frontend/Dockerfile
touch frontend/package.json

# Root files
touch .github/workflows/deploy.yml
touch scripts/start-dev.sh
touch docker-compose.yml
touch .gitignore

