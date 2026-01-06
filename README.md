# Kevin AI - SOP to Agentic Automation Platform

## 🎯 Overview

Kevin AI is an enterprise-grade agentic platform that transforms Standard Operating Procedures (SOPs) into intelligent, executable workflows. It provides comprehensive automation opportunities, test scenarios, and production-ready code.

### Key Features

✅ **SOP Ingestion** - PDF, DOCX, Mermaid diagrams, process flow images  
✅ **Current State Analysis** - AI-powered extraction and visualization  
✅ **Future State Generation** - Optimized digital twin with automation  
✅ **Automation Identification** - RPA, agentic AI, and integration opportunities  
✅ **Test Case Generation** - Comprehensive scenarios at each process stage  
✅ **Code Generation** - Production-ready Fast API and agentic workflow code  
✅ **KPI/SLA Analysis** - Efficiency improvements and ROI calculations  

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (optional)
- Azure OpenAI API key (or OpenAI/Anthropic)
- Tesseract OCR (for scanned documents)

### Local Installation

```bash
# Clone repository
git clone https://github.com/xyz-consulting/kevin-ai
cd kevin-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils -y

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run Gradio demo
python kevin_demo.py
```

Open browser to: http://localhost:7860

### Docker Installation

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f kevin-api

# Stop
docker-compose down
```

API available at: http://localhost:8000

---

## 📖 Usage

### Gradio UI Demo

1. **Upload SOP Document** - PDF, DOCX, or Mermaid
2. **Optional: Upload Process Diagram** - PNG, JPG, or Mermaid
3. **Select Domain** - Logistics, Insurance, Finance, Healthcare, etc.
4. **Click "Process SOP"** - Wait ~14 minutes for complete analysis
5. **Review Outputs** - Explore tabs for all generated artifacts

### REST API

```python
import requests

# Upload and process SOP
files = {
    'sop_file': open('sop_document.pdf', 'rb'),
    'diagram_file': open('process_diagram.png', 'rb')  # Optional
}
data = {'domain': 'logistics'}

response = requests.post(
    'http://localhost:8000/api/v1/process/sop',
    files=files,
    data=data
)

result = response.json()
session_id = result['session_id']

# Get current state map
current_state = requests.get(
    f'http://localhost:8000/api/v1/results/{session_id}/current-state-map'
)

# Get future state map
future_state = requests.get(
    f'http://localhost:8000/api/v1/results/{session_id}/future-state-map'
)

# Get automation opportunities
opportunities = requests.get(
    f'http://localhost:8000/api/v1/results/{session_id}/automation-opportunities'
)

# Get test cases
test_cases = requests.get(
    f'http://localhost:8000/api/v1/results/{session_id}/test-cases'
)

# Get generated code
code = requests.get(
    f'http://localhost:8000/api/v1/results/{session_id}/generated-code'
)

# Get KPI analysis
kpi = requests.get(
    f'http://localhost:8000/api/v1/results/{session_id}/kpi-analysis'
)
```

---

## 📊 Output Artifacts

### 1. Current State Process Map
- **Format:** Mermaid flowchart + PNG
- **Contents:** All process steps, decision points, actors, bottlenecks

### 2. Gap Analysis Report
- **Format:** Markdown + DOCX
- **Contents:** Inconsistencies, missing steps, recommendations

### 3. Future State Process Map
- **Format:** Mermaid flowchart + PNG
- **Contents:** Optimized flow, automation points, exception handling

### 4. Automation Opportunities List
- **Format:** Excel + JSON
- **Contents:** Step ID, description, automation type, complexity, ROI, priority

### 5. Requirements Document
- **Format:** DOCX + Markdown
- **Contents:** Functional, non-functional, integration, data, compliance requirements

### 6. Test Case Scenarios
- **Format:** Excel + JSON
- **Contents:** Unit, integration, E2E tests with steps, data, expected results

### 7. Production-Ready Code
- **Format:** Python (FastAPI + LangGraph)
- **Contents:** API endpoints, agent definitions, services, integrations

### 8. KPI/SLA Improvement Report
- **Format:** PowerPoint + Excel
- **Contents:** Cycle time, cost, error rate, SLA compliance, ROI

---

## 🏗️ Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT LAYER                                 │
│  SOP Documents (PDF, DOCX) + Process Diagrams (PNG, Mermaid)   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              DOCUMENT PROCESSING LAYER                          │
│  OCR Engine | Text Extraction | Structure Identification       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                AGENTIC AI LAYER (LangGraph)                     │
│  9 Specialized Agents:                                          │
│  1. Master Orchestrator                                         │
│  2. SOP Analysis                                                 │
│  3. Process Mapping                                              │
│  4. Gap Identification                                           │
│  5. Automation Opportunity                                       │
│  6. Future State Design                                          │
│  7. Test Case Generator                                          │
│  8. Code Generator                                               │
│  9. KPI/SLA Calculator                                           │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT LAYER                                │
│  8 Comprehensive Artifacts (Maps, Reports, Code, Analysis)      │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **AI/ML:** Azure OpenAI (GPT-4o), Anthropic (Claude Sonnet 4.5), LangGraph, LangChain
- **Backend:** FastAPI, Python 3.12
- **Frontend:** Gradio (Demo), React (Production)
- **Database:** FAISS (Vector), PostgreSQL (Metadata)
- **Deployment:** Docker, Kubernetes, Azure App Service

---

## ☁️ Azure Deployment

### Option 1: Azure App Service

```bash
# Set variables
export RESOURCE_GROUP="kevin-ai-rg"
export LOCATION="eastus"
export APP_NAME="kevin-ai-api"
export PLAN_NAME="kevin-ai-plan"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service plan
az appservice plan create \
    --name $PLAN_NAME \
    --resource-group $RESOURCE_GROUP \
    --sku B1 \
    --is-linux

# Create web app
az webapp create \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --plan $PLAN_NAME \
    --runtime "PYTHON:3.12"

# Configure app settings
az webapp config appsettings set \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
        LLM_PROVIDER="azure" \
        AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
        AZURE_OPENAI_API_KEY="your-api-key"

# Deploy
az webapp deployment source config-zip \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --src kevin-ai.zip
```

### Option 2: Azure Container Instances

```bash
# Build and push container
docker build -t kevin-ai:latest .
docker tag kevin-ai:latest yourregistry.azurecr.io/kevin-ai:latest
docker push yourregistry.azurecr.io/kevin-ai:latest

# Deploy container
az container create \
    --name kevin-ai \
    --resource-group $RESOURCE_GROUP \
    --image yourregistry.azurecr.io/kevin-ai:latest \
    --cpu 2 \
    --memory 4 \
    --ports 8000 \
    --dns-name-label kevin-ai \
    --environment-variables \
        LLM_PROVIDER="azure" \
        AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
        AZURE_OPENAI_API_KEY="your-api-key"
```

### Option 3: Azure Kubernetes Service (AKS)

```bash
# Create AKS cluster
az aks create \
    --resource-group $RESOURCE_GROUP \
    --name kevin-ai-aks \
    --node-count 2 \
    --enable-addons monitoring \
    --generate-ssh-keys

# Deploy using Helm or kubectl
kubectl apply -f kubernetes/deployment.yaml
```

---

## 🔐 Security

- **Data Encryption:** AES-256 at rest, TLS 1.3 in transit
- **API Authentication:** API keys, OAuth 2.0, Azure AD
- **PII Detection:** Automatic masking of sensitive data
- **Compliance:** GDPR, SOC 2, HIPAA considerations

---

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run E2E tests
pytest tests/e2e

# Generate coverage report
pytest --cov=. --cov-report=html
```

---

## 📝 API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

---

## 🎯 Demo Scenario: Cars Commerce

Upload the Cars Commerce EDI Order Processing SOP to see Kevin AI in action!

**Expected Results:**
- 15+ automation opportunities
- 50+ test cases
- Production-ready FastAPI code
- 40%+ cycle time improvement
- $500K+ annual savings

---

## 📞 Support

**Project:** Kevin AI - SOP Automation Platform  
**Version:** 2.0.0  
**Client:** Cars Commerce  
**Demo Date:** January 8, 2026  
**Go-Live:** January 16, 2026  

**Contact:**
- **Email:** kevin-ai@xyz-consulting.com
- **Principal Architect:** Sathya
- **Organization:** XYZ Consulting

---

## 📄 License

Copyright © 2026 XYZ Consulting. All rights reserved.

Proprietary and confidential. Unauthorized copying, modification, or distribution is prohibited.
