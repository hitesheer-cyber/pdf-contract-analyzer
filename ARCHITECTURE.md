# System Architecture & Data Flow

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                    (React.js Dashboard)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ FileUpload   │  │  Analytics   │  │ContractList  │         │
│  │  Component   │  │   Dashboard  │  │  Component   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│          │                  │                  │                │
│          └──────────────────┴──────────────────┘                │
│                             │                                   │
│                      ┌──────▼──────┐                           │
│                      │  API Client │                           │
│                      │   (Axios)   │                           │
│                      └──────┬──────┘                           │
└─────────────────────────────┼──────────────────────────────────┘
                              │ HTTP/REST
                              │
┌─────────────────────────────▼──────────────────────────────────┐
│                    Backend API Layer                           │
│                      (FastAPI)                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  API Endpoints (app/api/contracts.py)                  │   │
│  │  • POST /api/contracts/upload                          │   │
│  │  • GET  /api/contracts                                 │   │
│  │  • GET  /api/contracts/{id}                            │   │
│  │  • GET  /api/analytics                                 │   │
│  └────────┬───────────────────────────┬───────────────────┘   │
│           │                           │                        │
│  ┌────────▼────────┐       ┌─────────▼──────────┐            │
│  │ PDF Service     │       │  NLP Service       │            │
│  │ (PyPDF2)        │       │ (Transformers)     │            │
│  │                 │       │                    │            │
│  │ • Validate PDF  │       │ • Load BERT Model  │            │
│  │ • Extract Text  │       │ • Extract Entities │            │
│  │ • Error Handle  │       │ • Deduplicate      │            │
│  └────────┬────────┘       └─────────┬──────────┘            │
│           │                          │                        │
│           └──────────┬───────────────┘                        │
│                      │                                        │
│           ┌──────────▼──────────┐                            │
│           │  Database Layer     │                            │
│           │  (SQLAlchemy ORM)   │                            │
│           └──────────┬──────────┘                            │
└──────────────────────┼───────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                 PostgreSQL Database                          │
│  ┌────────────────────┐      ┌────────────────────┐         │
│  │  Contracts Table   │      │   Entities Table   │         │
│  │  • id (PK)         │      │   • id (PK)        │         │
│  │  • filename        │      │   • contract_id(FK)│         │
│  │  • upload_date     │      │   • text           │         │
│  │  • file_size       │      │   • entity_type    │         │
│  │  • text_content    │      │   • position       │         │
│  │  • status          │      │   • confidence     │         │
│  └────────────────────┘      └────────────────────┘         │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

### 1. Contract Upload Flow

```
User                Frontend            Backend API         PDF Service       NLP Service       Database
 │                     │                     │                   │                 │               │
 │  Select PDF         │                     │                   │                 │               │
 │────────────────────>│                     │                   │                 │               │
 │                     │                     │                   │                 │               │
 │  Click Upload       │                     │                   │                 │               │
 │────────────────────>│                     │                   │                 │               │
 │                     │                     │                   │                 │               │
 │                     │  POST /api/contracts/upload             │                 │               │
 │                     │────────────────────>│                   │                 │               │
 │                     │                     │                   │                 │               │
 │                     │                     │  Validate PDF     │                 │               │
 │                     │                     │──────────────────>│                 │               │
 │                     │                     │                   │                 │               │
 │                     │                     │  Valid PDF        │                 │               │
 │                     │                     │<──────────────────│                 │               │
 │                     │                     │                   │                 │               │
 │                     │                     │  Create Contract Record             │               │
 │                     │                     │─────────────────────────────────────────────────────>│
 │                     │                     │                   │                 │               │
 │                     │                     │  Extract Text     │                 │               │
 │                     │                     │──────────────────>│                 │               │
 │                     │                     │                   │                 │               │
 │                     │                     │  Extracted Text   │                 │               │
 │                     │                     │<──────────────────│                 │               │
 │                     │                     │                   │                 │               │
 │                     │                     │  Extract Entities │                 │               │
 │                     │                     │───────────────────────────────────>│               │
 │                     │                     │                   │                 │               │
 │                     │                     │  Entity List      │                 │               │
 │                     │                     │<───────────────────────────────────│               │
 │                     │                     │                   │                 │               │
 │                     │                     │  Save Entities                      │               │
 │                     │                     │─────────────────────────────────────────────────────>│
 │                     │                     │                   │                 │               │
 │                     │                     │  Update Contract Status             │               │
 │                     │                     │─────────────────────────────────────────────────────>│
 │                     │                     │                   │                 │               │
 │                     │  Upload Response    │                   │                 │               │
 │                     │<────────────────────│                   │                 │               │
 │                     │                     │                   │                 │               │
 │  Success Message    │                     │                   │                 │               │
 │<────────────────────│                     │                   │                 │               │
```

### 2. Analytics Retrieval Flow

```
User                Frontend            Backend API         Database
 │                     │                     │                   │
 │  View Dashboard     │                     │                   │
 │────────────────────>│                     │                   │
 │                     │                     │                   │
 │                     │  GET /api/analytics │                   │
 │                     │────────────────────>│                   │
 │                     │                     │                   │
 │                     │                     │  Query Contracts  │
 │                     │                     │──────────────────>│
 │                     │                     │                   │
 │                     │                     │  Contract Count   │
 │                     │                     │<──────────────────│
 │                     │                     │                   │
 │                     │                     │  Query Entities   │
 │                     │                     │──────────────────>│
 │                     │                     │                   │
 │                     │                     │  Entity Data      │
 │                     │                     │<──────────────────│
 │                     │                     │                   │
 │                     │                     │  Aggregate Stats  │
 │                     │                     │  Calculate Metrics│
 │                     │                     │                   │
 │                     │  Analytics JSON     │                   │
 │                     │<────────────────────│                   │
 │                     │                     │                   │
 │                     │  Render Charts      │                   │
 │                     │                     │                   │
 │  View Analytics     │                     │                   │
 │<────────────────────│                     │                   │
```

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend Layer                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ FileUpload  │    │  Analytics   │    │ ContractList │  │
│  │             │    │              │    │              │  │
│  │ • Select    │    │ • Pie Chart  │    │ • Table View │  │
│  │ • Validate  │    │ • Bar Chart  │    │ • Status     │  │
│  │ • Upload    │    │ • Stats      │    │ • Pagination │  │
│  └──────┬──────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                  │                    │          │
│         └──────────────────┴────────────────────┘          │
│                            │                                │
│                     ┌──────▼──────┐                        │
│                     │ API Service │                        │
│                     │   (Axios)   │                        │
│                     └──────┬──────┘                        │
└────────────────────────────┼────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                      API Layer                              │
├────────────────────────────┼────────────────────────────────┤
│                     ┌──────▼──────┐                         │
│                     │  FastAPI    │                         │
│                     │  Endpoints  │                         │
│                     └──────┬──────┘                         │
│                            │                                │
│         ┌──────────────────┼──────────────────┐            │
│         │                  │                  │            │
│  ┌──────▼──────┐    ┌──────▼──────┐   ┌──────▼──────┐    │
│  │  Validation │    │  Processing │   │  Analytics  │    │
│  │   Schemas   │    │   Services  │   │   Queries   │    │
│  │  (Pydantic) │    │             │   │             │    │
│  └─────────────┘    └──────┬──────┘   └──────┬──────┘    │
│                            │                  │            │
│                     ┌──────▼──────────────────▼──────┐    │
│                     │      ORM Layer (SQLAlchemy)    │    │
│                     └──────┬────────────────────────┘    │
└────────────────────────────┼────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                     Data Layer                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐              ┌──────────────────┐    │
│  │  Contracts       │              │  Entities        │    │
│  │  ┌────────────┐  │   1     ∞    │  ┌────────────┐ │    │
│  │  │ id         │──┼──────────────┼──│contract_id │ │    │
│  │  │ filename   │  │              │  │ text       │ │    │
│  │  │ status     │  │              │  │ type       │ │    │
│  │  │ date       │  │              │  │ position   │ │    │
│  │  └────────────┘  │              │  └────────────┘ │    │
│  └──────────────────┘              └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Docker Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Host                              │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │            Docker Network (contract-network)          │ │
│  │                                                       │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │ │
│  │  │  Frontend   │  │   Backend    │  │ PostgreSQL │  │ │
│  │  │  (React)    │  │  (FastAPI)   │  │     DB     │  │ │
│  │  │             │  │              │  │            │  │ │
│  │  │  Port 3000  │  │  Port 8000   │  │ Port 5432  │  │ │
│  │  │             │  │              │  │            │  │ │
│  │  │  + Nginx    │  │  + Uvicorn   │  │ + Data Vol │  │ │
│  │  │             │  │  + Models    │  │            │  │ │
│  │  └─────────────┘  └──────────────┘  └────────────┘  │ │
│  │                                                       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Volumes:                                                   │
│  • postgres_data (Database persistence)                     │
│  • nlp_models (Model cache)                                 │
└─────────────────────────────────────────────────────────────┘
```

## Entity Extraction Pipeline

```
┌──────────────┐
│   PDF File   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Validate PDF │
│  • Type      │
│  • Size      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Extract Text │
│  (PyPDF2)    │
│  • Page by   │
│    page      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Chunk Text  │
│  (Max 5000   │
│   chars)     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Load BERT    │
│  NER Model   │
│ (dslim/bert- │
│  base-NER)   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Run NER      │
│ Pipeline     │
│  • Tokenize  │
│  • Predict   │
│  • Aggregate │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Process      │
│ Entities     │
│  • Map types │
│  • Calculate │
│    positions │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Deduplicate  │
│  • By text   │
│  • By pos    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Save to DB   │
│  • Contract  │
│  • Entities  │
└──────────────┘
```

## Request/Response Flow

```
Client Request
     │
     ▼
  Nginx (Frontend Container)
     │
     ├─── Static Files (React) ──────> Browser
     │
     └─── /api/* ────────────────────> FastAPI (Backend)
                                            │
                                            ▼
                                       CORS Middleware
                                            │
                                            ▼
                                       Route Handler
                                            │
                                            ▼
                                       Validation (Pydantic)
                                            │
                                            ▼
                                       Business Logic
                                            │
                                            ▼
                                       Database Query
                                            │
                                            ▼
                                       Response Schema
                                            │
                                            ▼
                                       JSON Response ───> Client
```

This architecture provides:

- **Scalability**: Each service can scale independently
- **Maintainability**: Clear separation of concerns
- **Reliability**: Health checks and error handling
- **Performance**: Caching, connection pooling, async operations
- **Security**: Validation, CORS, environment variables
