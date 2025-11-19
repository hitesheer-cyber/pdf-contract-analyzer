# Project Structure

```
python-pdf-interview/
├── README.md                           # Main project documentation
├── QUICKSTART.md                       # Quick start guide
├── DOCUMENTATION.md                    # Detailed technical documentation
├── API_EXAMPLES.md                     # Sample API calls and examples
├── LICENSE                             # MIT License
├── .gitignore                          # Git ignore patterns
├── .env.example                        # Environment variables template
├── setup.sh                            # Setup script (executable)
├── pyproject.toml                      # UV dependency management configuration
├── docker-compose.yml                  # Docker Compose orchestration
│
├── backend/                            # FastAPI Backend Service
│   ├── Dockerfile                      # Backend Docker configuration
│   ├── .dockerignore                   # Docker ignore patterns
│   │
│   ├── app/                            # Main application package
│   │   ├── __init__.py                 # Package initialization
│   │   ├── main.py                     # FastAPI application entry point
│   │   ├── config.py                   # Configuration settings (Pydantic)
│   │   ├── database.py                 # Database connection & session mgmt
│   │   │
│   │   ├── api/                        # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── contracts.py            # Contract endpoints (upload, list, analytics)
│   │   │
│   │   ├── models/                     # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   └── contract.py             # Contract & Entity models
│   │   │
│   │   ├── schemas/                    # Pydantic validation schemas
│   │   │   ├── __init__.py
│   │   │   └── contract.py             # Request/Response schemas
│   │   │
│   │   └── services/                   # Business logic services
│   │       ├── __init__.py
│   │       ├── pdf_service.py          # PDF text extraction (PyPDF2)
│   │       └── nlp_service.py          # Entity extraction (Transformers)
│   │
│   └── tests/                          # Unit & integration tests
│       ├── __init__.py
│       ├── conftest.py                 # Pytest configuration & fixtures
│       ├── test_api.py                 # API endpoint tests
│       └── test_services.py            # Service layer tests
│
└── frontend/                           # React.js Frontend Dashboard
    ├── Dockerfile                      # Frontend Docker configuration
    ├── .dockerignore                   # Docker ignore patterns
    ├── nginx.conf                      # Nginx configuration for production
    ├── package.json                    # NPM dependencies
    ├── README.md                       # Frontend documentation
    │
    ├── public/                         # Static files
    │   └── index.html                  # HTML template
    │
    └── src/                            # React source code
        ├── index.js                    # React entry point
        ├── App.js                      # Main application component
        ├── App.css                     # Application styles
        ├── App.test.js                 # Application tests
        ├── setupTests.js               # Test configuration
        │
        ├── components/                 # React components
        │   ├── FileUpload.js           # PDF upload component
        │   ├── FileUpload.css          # Upload component styles
        │   ├── Analytics.js            # Analytics dashboard component
        │   ├── Analytics.css           # Analytics component styles
        │   ├── ContractList.js         # Contract listing component
        │   └── ContractList.css        # Contract list styles
        │
        └── services/                   # API integration
            └── api.js                  # Axios API client
```

## Key Files Description

### Configuration Files

- **pyproject.toml**: UV package manager configuration with all Python dependencies
- **docker-compose.yml**: Orchestrates PostgreSQL, Backend, and Frontend services
- **.env.example**: Template for environment variables
- **setup.sh**: Automated setup script for local development

### Backend Files

- **app/main.py**: FastAPI app initialization, CORS, and startup events
- **app/config.py**: Pydantic Settings for environment configuration
- **app/database.py**: SQLAlchemy engine, session management, and database initialization
- **app/api/contracts.py**: All API endpoints (upload, list, get, analytics)
- **app/models/contract.py**: Database models (Contract & Entity)
- **app/schemas/contract.py**: Pydantic schemas for validation
- **app/services/pdf_service.py**: PDF text extraction using PyPDF2
- **app/services/nlp_service.py**: NER using Hugging Face Transformers

### Frontend Files

- **src/App.js**: Main React component with state management
- **src/components/FileUpload.js**: PDF file upload with error handling
- **src/components/Analytics.js**: Charts and analytics visualization (Recharts)
- **src/components/ContractList.js**: Table view of all contracts
- **src/services/api.js**: Axios-based API client with endpoints

### Docker Files

- **backend/Dockerfile**: Multi-stage Docker build for Python backend
- **frontend/Dockerfile**: Multi-stage build (Node build + Nginx serve)
- **frontend/nginx.conf**: Production Nginx configuration with proxy
- **docker-compose.yml**: Complete stack orchestration

## Technology Stack

### Backend

- FastAPI 0.104+
- SQLAlchemy 2.0+
- PostgreSQL 15
- PyPDF2 3.0+
- Transformers 4.35+ (Hugging Face)
- PyTorch 2.1+
- Pydantic 2.4+
- Uvicorn (ASGI server)

### Frontend

- React 18.2
- Recharts 2.10 (Charts)
- Axios 1.6 (HTTP client)
- React Scripts 5.0

### DevOps

- Docker & Docker Compose
- UV (Python package manager)
- Nginx (Production server)

## Data Flow

1. **Upload**: User uploads PDF → Backend validates → PDF text extracted → NLP processes text → Entities stored in DB
2. **Analytics**: Frontend requests analytics → Backend queries DB → Aggregates data → Returns JSON → Frontend visualizes
3. **Listing**: Frontend requests contracts → Backend paginates results → Returns summaries → Frontend displays table

## Environment Variables

See `.env.example` for all configuration options:

- Database connection
- Application settings
- NLP model configuration
- CORS origins
- File size limits

## Running Tests

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

## Building for Production

### Docker (All services)

```bash
docker-compose up --build
```

### Backend only

```bash
cd backend
docker build -t contract-backend .
docker run -p 8000:8000 contract-backend
```

### Frontend only

```bash
cd frontend
docker build -t contract-frontend .
docker run -p 3000:80 contract-frontend
```
