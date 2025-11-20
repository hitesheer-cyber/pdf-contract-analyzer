# Quick Start Guide

This guide will help you get the Contract Entity Extraction & Analytics Microservice up and running quickly.

## Prerequisites

- Docker and Docker Compose (recommended)
- OR: Python 3.9+, Node.js 16+, PostgreSQL, and UV

## Quick Start with Docker (Recommended)

1. **Clone the repository**:

   ```bash
   cd pdf-contract-analyzer
   ```

2. **Create environment file**:

   ```bash
   cp .env.example .env
   ```

3. **Start all services**:

   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend Dashboard: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

That's it! The application is now running.

## Quick Start without Docker

1. **Run the setup script**:

   ```bash
   ./setup.sh
   ```

2. **Start PostgreSQL**:

   ```bash
   docker run --name contract-db \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=contract_db \
     -p 5432:5432 -d postgres:15
   ```

3. **Start the backend** (in one terminal):

   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn app.main:app --reload
   ```

4. **Start the frontend** (in another terminal):

   ```bash
   cd frontend
   npm run dev
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Testing the Application

### Upload a Test Contract

1. Open http://localhost:3000
2. Click "Choose File" and select a PDF contract
3. Click "Upload"
4. View extracted entities and analytics

### Test via API (using curl)

```bash
# Upload a contract
curl -X POST "http://localhost:8000/api/contracts/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/contract.pdf"

# Get analytics
curl -X GET "http://localhost:8000/api/analytics" \
  -H "accept: application/json"

# List contracts
curl -X GET "http://localhost:8000/api/contracts" \
  -H "accept: application/json"
```

## Stopping the Application

### Docker:

```bash
docker-compose down
```

### Manual:

- Press `Ctrl+C` in each terminal
- Stop PostgreSQL: `docker stop contract-db`

## Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are in use, modify them in `docker-compose.yml` or when starting manually.

### Database Connection Error

Ensure PostgreSQL is running:

```bash
docker ps | grep postgres
```

### Frontend Can't Connect to Backend

Check that CORS origins in `.env` include your frontend URL.

### NLP Model Download

First run downloads ~400MB model. Ensure stable internet connection.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DOCUMENTATION.md](DOCUMENTATION.md) for architecture details
- Explore API at http://localhost:8000/docs
- Customize `.env` for your needs

## Support

For issues, check the README troubleshooting section or open an issue.
