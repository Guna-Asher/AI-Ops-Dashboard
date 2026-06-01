#!/bin/bash
# Run as user data or manually on Ubuntu EC2
apt-get update
apt-get install -y docker.io docker-compose git
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu
git clone https://github.com/yourorg/ai-ops-dashboard.git /opt/aiops
cd /opt/aiops
echo "OPENAI_API_KEY=your-key" > .env
docker-compose up -d