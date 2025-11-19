#!/bin/bash

# Script to set up the development environment

set -e

echo "🚀 Setting up Contract Entity Extraction Microservice..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ Please review and update .env with your configuration"
fi

# Backend setup
echo "📦 Setting up backend..."
cd backend
uv venv
source .venv/bin/activate
uv pip install -e ..
cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install Node.js and npm first."
    exit 1
fi
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  Using Docker Compose (recommended):"
echo "    docker-compose up --build"
echo ""
echo "  Manual setup:"
echo "    1. Start PostgreSQL: docker run --name contract-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=contract_db -p 5432:5432 -d postgres:15"
echo "    2. Backend: cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
echo "    3. Frontend: cd frontend && npm start"
echo ""
echo "📚 Access the application at:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
