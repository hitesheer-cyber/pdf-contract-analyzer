# AI-Powered Contract Entity Extraction & Analytics Microservice

An enterprise solution to automate contract review for legal and financial stakeholders. This system ingests PDF contracts, extracts key entities using NLP, stores results in PostgreSQL, and provides analytics via REST API with a React.js dashboard.

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Project Summary](PROJECT_SUMMARY.md)** - Overview and features checklist
- **[Architecture Diagrams](ARCHITECTURE.md)** - System design and data flow
- **[API Examples](API_EXAMPLES.md)** - Sample API calls and usage
- **[Project Structure](PROJECT_STRUCTURE.md)** - Complete file organization
- **[Full Documentation](DOCUMENTATION.md)** - Detailed technical docs

## Features

- 📄 **PDF Document Ingestion**: Upload and process PDF contracts
- 🤖 **AI-Powered Entity Extraction**: Extract parties, dates, amounts, and clauses using Hugging Face Transformers
- 💾 **PostgreSQL Storage**: Store extracted entities with metadata
- 📊 **Analytics API**: Get insights on entity counts, frequent entities, and missing fields
- 🎨 **React Dashboard**: Visualize analytics in an intuitive interface
- 🐳 **Dockerized**: Easy deployment with Docker and Docker Compose

## Architecture

```
├── backend/               # FastAPI microservice
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── database.py   # Database configuration
│   │   └── main.py       # Application entry point
│   └── Dockerfile
├── frontend/             # React.js dashboard
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API integration
│   │   └── App.js
│   └── Dockerfile
├── docker-compose.yml
└── pyproject.toml       # UV dependency management
```

## Tech Stack

- **Backend**: Python 3.9+, FastAPI, SQLAlchemy
- **NLP**: Hugging Face Transformers (dslim/bert-base-NER)
- **Database**: PostgreSQL
- **Frontend**: React.js
- **Package Management**: UV
- **Containerization**: Docker, Docker Compose

## Prerequisites

- Python 3.9 or higher
- Node.js 16+ and npm
- Docker and Docker Compose
- UV package manager

### Installing UV

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd python-pdf-interview
```

2. Create environment file:

```bash
cp .env.example .env
```

3. Start all services:

```bash
docker-compose up --build
```

4. Access the application:
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Frontend Dashboard: http://localhost:3000

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ..
```

3. Set up PostgreSQL database:

```bash
# Using Docker
docker run --name contract-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=contract_db -p 5432:5432 -d postgres:15
```

4. Run database migrations:

```bash
python -m app.database
```

5. Start the backend server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

## API Documentation

### Endpoints

#### 1. Upload Contract PDF

```bash
POST /api/contracts/upload
Content-Type: multipart/form-data

curl -X POST "http://localhost:8000/api/contracts/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@contract.pdf"
```

**Response:**

```json
{
  "id": "uuid-string",
  "filename": "contract.pdf",
  "upload_date": "2025-11-19T10:30:00",
  "entities_extracted": 25,
  "status": "processed"
}
```

#### 2. Get Contract Details

```bash
GET /api/contracts/{contract_id}

curl -X GET "http://localhost:8000/api/contracts/uuid-string" \
  -H "accept: application/json"
```

**Response:**

```json
{
  "id": "uuid-string",
  "filename": "contract.pdf",
  "upload_date": "2025-11-19T10:30:00",
  "entities": [
    {
      "id": 1,
      "text": "ABC Corporation",
      "type": "ORG",
      "position": 150,
      "confidence": 0.95
    }
  ]
}
```

#### 3. Get Analytics

```bash
GET /api/analytics

curl -X GET "http://localhost:8000/api/analytics" \
  -H "accept: application/json"
```

**Response:**

```json
{
  "total_contracts": 10,
  "total_entities": 250,
  "entity_type_distribution": {
    "ORG": 45,
    "PERSON": 30,
    "DATE": 25,
    "MONEY": 15,
    "LOC": 10
  },
  "most_frequent_entities": [
    { "text": "ABC Corporation", "count": 5 },
    { "text": "John Doe", "count": 3 }
  ],
  "contracts_missing_key_entities": [
    {
      "id": "uuid-string",
      "filename": "incomplete_contract.pdf",
      "missing_types": ["MONEY", "DATE"]
    }
  ]
}
```

#### 4. List All Contracts

```bash
GET /api/contracts

curl -X GET "http://localhost:8000/api/contracts?skip=0&limit=10" \
  -H "accept: application/json"
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
uv pip install -e "..[dev]"
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Format code
black backend/

# Lint code
flake8 backend/

# Type checking
mypy backend/
```

## Configuration

Key configuration options in `.env`:

- `DATABASE_URL`: PostgreSQL connection string
- `NLP_MODEL_NAME`: Hugging Face model for entity extraction
- `MAX_UPLOAD_SIZE`: Maximum PDF file size in bytes
- `CORS_ORIGINS`: Allowed CORS origins for frontend

## Entity Types Extracted

The NLP model extracts the following entity types:

- **PERSON**: Individual names (e.g., signatories, parties)
- **ORG**: Organization names (e.g., companies, institutions)
- **DATE**: Dates (e.g., contract dates, deadlines)
- **MONEY**: Monetary amounts (e.g., contract values)
- **LOC**: Locations (e.g., jurisdictions)
- **MISC**: Other relevant entities

## Troubleshooting

### Database Connection Issues

Ensure PostgreSQL is running:

```bash
docker ps | grep postgres
```

### Model Download Issues

The first run will download the NLP model (~400MB). Ensure stable internet connection.

### Port Conflicts

If ports 8000 or 3000 are in use, modify the ports in `docker-compose.yml` or `.env`.

## Performance Considerations

- PDF processing time depends on document size and complexity
- First entity extraction will be slower due to model loading
- Consider using model caching for production deployments
- Database indexing on entity types and text for faster analytics

## Security Notes

- Input validation for PDF files (size, type)
- SQL injection protection via SQLAlchemy ORM
- CORS configuration for frontend access
- Environment variables for sensitive data
- Rate limiting recommended for production

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions, please open an issue on GitHub.
