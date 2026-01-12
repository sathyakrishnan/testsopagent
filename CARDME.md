# Claims API Platform

> Enterprise-grade insurance claims processing platform with multi-tenant architecture and hybrid AI orchestration.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4.svg)](https://azure.microsoft.com/)

---

## 🎯 Overview

A multi-tenant API platform for automated insurance claims processing, featuring:

- **Hybrid AI Orchestration**: GPT-4o + Claude Sonnet 4 for 85-95% estimation accuracy
- **Multi-Client Architecture**: Client-agnostic core with pluggable adapters (Mendix, Salesforce, REST)
- **Enterprise Security**: OAuth 2.0, PII masking, HIPAA/GDPR compliant
- **Production-Ready**: PostgreSQL, Redis, rate limiting, structured logging, audit trails

**Current Clients:**
- ✅ **Mendix** - FNOL submission API (Production)
- 🔜 **Salesforce** - Claims management integration
- 🔜 **REST API** - Generic client access

---

## 🏗️ Architecture

### Hexagonal Architecture (Ports & Adapters)
```
┌─────────────────────────────────────────────────────────┐
│                    Client Adapters                       │
│  ┌──────────┐  ┌────────────┐  ┌────────────┐         │
│  │  Mendix  │  │ Salesforce │  │  REST API  │         │
│  └────┬─────┘  └──────┬─────┘  └──────┬─────┘         │
└───────┼────────────────┼────────────────┼──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
        ┌────────────────▼─────────────────┐
        │         Core Domain              │
        │  ┌────────────────────────────┐  │
        │  │  Claims Processing Engine  │  │
        │  │  - Business Logic          │  │
        │  │  - Domain Models           │  │
        │  │  - Services                │  │
        │  └────────────────────────────┘  │
        │                                   │
        │  ┌────────────────────────────┐  │
        │  │   AI Orchestration Layer   │  │
        │  │  - GPT-4o Provider         │  │
        │  │  - Claude Provider         │  │
        │  │  - Hybrid Orchestrator     │  │
        │  │  - Consensus Evaluator     │  │
        │  └────────────────────────────┘  │
        └───────────────┬──────────────────┘
                        │
        ┌───────────────▼──────────────────┐
        │       Infrastructure             │
        │  ┌──────┐ ┌───────┐ ┌────────┐  │
        │  │ PSQL │ │ Redis │ │  Blob  │  │
        │  └──────┘ └───────┘ └────────┘  │
        └──────────────────────────────────┘
```

### Key Principles

- **Core Domain**: Business logic is client-agnostic and reusable
- **Adapters**: Each client has its own adapter (API contract, auth, mappers)
- **Single AI Engine**: Shared hybrid orchestration serves all clients
- **Scalability**: Add new clients without touching core domain

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- OpenAI API key (GPT-4o)
- Anthropic API key (Claude)

### 1. Clone & Setup
```bash
# Clone repository
git clone https://github.com/xyz-consulting/claims-api-platform.git
cd claims-api-platform

# Run setup script (handles Rust, dependencies, etc.)
bash scripts/setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements/base.txt
pip install -r requirements/mendix.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your keys
nano .env

# Required:
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
SECRET_KEY=your-secret-key-min-32-chars
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/claims_db
REDIS_URL=redis://localhost:6379/0
```

### 3. Start Infrastructure
```bash
# Start PostgreSQL + Redis
docker-compose -f deployments/docker/docker-compose.yml up -d

# Verify
docker ps  # Should see postgres and redis containers
```

### 4. Run Mendix API
```bash
# Start API
uvicorn src.apps.mendix_api:app --reload --port 8000

# Access Swagger UI
open http://localhost:8000/docs
```

### 5. Test
```bash
# Health check
curl http://localhost:8000/api/health

# Get auth token
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -d "username=mendix_client&password=secret"

# Submit FNOL
curl -X POST "http://localhost:8000/api/v1/claims/fnol" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d @tests/fixtures/fnol_us_accident.json
```

---

## 📂 Project Structure
```
claims-api-platform/
├── src/
│   ├── core/                   # Core domain (client-agnostic)
│   │   ├── domain/            # Business logic & models
│   │   ├── infrastructure/    # Database, cache, storage
│   │   ├── ai/                # AI orchestration layer
│   │   └── shared/            # Utilities, config, logging
│   ├── adapters/              # Client-specific adapters
│   │   ├── mendix/            # Mendix integration
│   │   ├── salesforce/        # Salesforce (future)
│   │   └── rest_api/          # Generic REST (future)
│   └── apps/                  # Application entry points
│       ├── mendix_api.py      # Mendix FastAPI app
│       └── internal_api.py    # Admin API
├── tests/                     # Comprehensive test suite
├── deployments/               # Docker, K8s, Azure configs
├── docs/                      # Documentation
└── scripts/                   # Utility scripts
```

**Key Files:**
- `src/core/domain/services/claim_service.py` - Core claims logic
- `src/core/ai/orchestrators/hybrid_orchestrator.py` - GPT-4o + Claude
- `src/adapters/mendix/api/v1/fnol.py` - Mendix FNOL endpoint
- `src/apps/mendix_api.py` - Mendix FastAPI application

---

## 🔧 Development

### Install Development Tools
```bash
pip install -r requirements/dev.txt
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/
pylint src/

# Type checking
mypy src/

# Security scan
bandit -r src/
```

### Testing
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# E2E tests
pytest tests/e2e/ -v

# Coverage
pytest --cov=src --cov-report=html
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Add claims table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 📊 API Documentation

### Mendix API

**Base URL:** `https://xyz-claims-api-production.azurewebsites.net/api/v1`

**Authentication:** OAuth 2.0 Client Credentials

**Key Endpoints:**

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| POST | `/auth/token` | Get access token | 100/min |
| POST | `/claims/fnol` | Submit FNOL | 100/min |
| GET | `/claims/fnol/{id}` | Retrieve claim | 500/min |
| POST | `/claims/fnol/estimate-only` | Get estimation | 100/min |

**Interactive Docs:**
- Swagger UI: https://xyz-claims-api-production.azurewebsites.net/docs
- ReDoc: https://xyz-claims-api-production.azurewebsites.net/redoc

**Full Documentation:** [docs/api/mendix-integration.md](docs/api/mendix-integration.md)

---

## 🤖 AI Capabilities

### Hybrid Orchestration

**GPT-4o + Claude Sonnet 4**
- Runs both models in parallel
- Combines results for consensus estimation
- 85-95% accuracy (vs 80-85% single model)
- Variance analysis for confidence scoring

**Cost per Claim:**
- Hybrid Mode: ~$0.02 (recommended)
- GPT-4o Only: ~$0.01 (faster)

**Example Response:**
```json
{
  "estimated_total_cost": {
    "amount": 12500.00,
    "currency": "USD",
    "range": {"min": 8750, "max": 18750}
  },
  "severity_assessment": "MODERATE",
  "confidence_score": 0.87,
  "consensus_details": {
    "gpt4o_estimate": 12000,
    "claude_estimate": 13000,
    "variance_percent": 8.0
  }
}
```

---

## 🔐 Security

### Authentication & Authorization

- **OAuth 2.0** Client Credentials Flow
- **JWT Tokens** (30-min expiry)
- **Scope-Based Access** (claims:read, claims:write)
- **API Key Support** (optional)

### Data Protection

- **PII Masking** before AI processing
- **TLS 1.3** encryption in transit
- **AES-256** field-level encryption at rest
- **Zero AI Training** (OpenAI & Anthropic policies)

### Compliance

- ✅ **HIPAA** compliant (BAA available)
- ✅ **GDPR** compliant (DPA available)
- ✅ **SOC 2 Type II** ready
- ✅ **FCA Guidelines** (UK)

### Rate Limiting
```python
RATE_LIMIT_TEXT_CLAIMS = 100   # per minute
RATE_LIMIT_STATUS = 500        # per minute
```

---

## ☁️ Deployment

### Docker (Local/Dev)
```bash
cd deployments/docker
docker-compose up -d

# Access API
curl http://localhost:8000/api/health
```

### Azure (Production)
```bash
# Deploy infrastructure
cd deployments/azure/bicep
az deployment group create \
  --resource-group xyz-claims-rg \
  --template-file main.bicep

# Deploy application
az webapp up \
  --name xyz-claims-api-production \
  --resource-group xyz-claims-rg
```

### Kubernetes
```bash
cd deployments/kubernetes
kubectl apply -k overlays/production
```

**Deployment Guide:** [docs/deployment/azure-setup.md](docs/deployment/azure-setup.md)

---

## 📈 Monitoring

### Metrics (Prometheus)
```
fnol_submissions_total
estimation_duration_seconds
ai_provider_calls_total
consensus_variance_percent
database_query_duration_seconds
```

### Logging (Structured JSON)
```json
{
  "event": "fnol_submission_completed",
  "claim_id": "uuid",
  "claim_number": "FNOL-2026-US-ABC123",
  "estimated_amount": 12500.00,
  "confidence": 0.87,
  "timestamp": "2026-01-10T10:30:00Z",
  "level": "info"
}
```

### Health Checks

- `/api/health` - Basic status
- `/api/health/detailed` - Full system check

---

## 🧪 Testing

### Test Coverage
```bash
pytest --cov=src --cov-report=term-missing
```

**Current Coverage:** 85%+

### Example Tests
```bash
# Unit tests
pytest tests/unit/core/domain/test_claim_service.py

# Integration tests
pytest tests/integration/test_database.py
pytest tests/integration/test_ai_providers.py

# E2E tests
pytest tests/e2e/test_mendix_fnol_flow.py
```

---

## 🔄 Adding New Clients

### Example: Adding Salesforce Integration

1. **Create Adapter**
```bash
mkdir -p src/adapters/salesforce/{api,auth,mappers}
```

2. **Implement API Contract**
```python
# src/adapters/salesforce/api/claims.py
from src.core.domain.services.claim_service import ClaimService

@router.post("/cases")
async def create_case(salesforce_case: SalesforceCase):
    # Map Salesforce model to core domain
    core_claim = SalesforceToCoreMapper.map(salesforce_case)
    
    # Use core service (no changes needed!)
    result = await ClaimService.process_claim(core_claim)
    
    # Map back to Salesforce response
    return CoreToSalesforceMapper.map(result)
```

3. **Create Application**
```python
# src/apps/salesforce_api.py
from fastapi import FastAPI
from src.adapters.salesforce.api import claims

app = FastAPI(title="Claims API - Salesforce")
app.include_router(claims.router)
```

4. **Deploy**
```bash
docker build -f deployments/docker/Dockerfile.salesforce-api
```

**Core domain remains untouched!** ✅

---

## 📚 Documentation

- **API Integration**: [docs/api/](docs/api/)
- **Architecture**: [docs/architecture/](docs/architecture/)
- **Deployment**: [docs/deployment/](docs/deployment/)
- **ADRs**: [docs/architecture/adr/](docs/architecture/adr/)

---

## 🛠️ Troubleshooting

### Common Issues

**Connection Refused (Port 8000)**
```bash
# Check services
docker ps
uvicorn src.apps.mendix_api:app --reload --port 8000
```

**Database Connection Failed**
```bash
# Verify PostgreSQL
docker exec -it postgres-claims psql -U postgres -c "\l"
```

**AI Provider Errors**
```bash
# Check API keys in .env
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
```

**Full Guide**: [docs/troubleshooting.md](docs/troubleshooting.md)

---

## 🤝 Contributing

### Development Workflow

1. Create feature branch: `git checkout -b feature/new-client`
2. Make changes following style guide
3. Add tests (maintain 85%+ coverage)
4. Run quality checks: `black`, `flake8`, `mypy`
5. Submit PR with description

### Style Guide

- **Code**: PEP 8, Black formatting
- **Docstrings**: Google style
- **Commits**: Conventional Commits

---

## 📞 Support

### Internal Teams

- **API Support**: api-support@xyzconsulting.com
- **Slack**: #xyz-claims-api
- **PagerDuty**: 24/7 on-call

### Business Hours

- **Response Time**: < 4 hours (8am-8pm EST)
- **Emergency**: < 30 minutes (24/7)

---

## 📋 Roadmap

### Q1 2026
- ✅ Mendix FNOL API (Production)
- 🔄 Salesforce Integration (In Progress)
- 📅 Multi-language Support (Spanish, French)

### Q2 2026
- 📅 Photo Analysis (Vehicle damage)
- 📅 Fraud Probability Scoring
- 📅 GraphQL API

### Q3 2026
- 📅 Mobile SDKs (iOS, Android)
- 📅 Real-time Claim Tracking
- 📅 ML Model Retraining Pipeline

---

## 📜 License

**Proprietary** - © 2026 XYZ Consulting. All rights reserved.

For licensing inquiries: legal@xyzconsulting.com

---

## 🙏 Acknowledgments

- **AI Providers**: OpenAI (GPT-4o), Anthropic (Claude Sonnet 4)
- **Infrastructure**: Microsoft Azure
- **Frameworks**: FastAPI, SQLAlchemy, Pydantic

---

**Version**: 1.1.0  
**Last Updated**: January 10, 2026  
**Status**: Production Ready  

**Target Go-Live (Mendix)**: January 16, 2026 ✅
