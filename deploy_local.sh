#!/bin/bash

# Kevin AI - Local Deployment Script
# Version: 2.0
# Date: January 6, 2026

set -e  # Exit on error

echo "=================================================="
echo "Kevin AI - Local Deployment"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.12.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo -e "${RED}Error: Python 3.12+ required. Found: $python_version${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $python_version${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check for Tesseract OCR
echo -e "${YELLOW}Checking for Tesseract OCR...${NC}"
if ! command -v tesseract &> /dev/null; then
    echo -e "${RED}Warning: Tesseract OCR not found${NC}"
    echo "Install with: sudo apt-get install tesseract-ocr (Ubuntu/Debian)"
    echo "             brew install tesseract (macOS)"
else
    tesseract_version=$(tesseract --version 2>&1 | head -n1)
    echo -e "${GREEN}✓ $tesseract_version${NC}"
fi

# Check for environment file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env with your API keys${NC}"
    echo "Required keys:"
    echo "  - AZURE_OPENAI_API_KEY or OPENAI_API_KEY or ANTHROPIC_API_KEY"
    read -p "Press Enter after updating .env file..."
fi

# Create necessary directories
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p uploads outputs vectordb logs
echo -e "${GREEN}✓ Directories created${NC}"

# Test import
echo -e "${YELLOW}Testing Kevin AI import...${NC}"
python3 -c "from kevin_agents import MasterOrchestratorAgent; print('Import successful')" 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Kevin AI modules loaded successfully${NC}"
else
    echo -e "${RED}Error: Failed to import Kevin AI modules${NC}"
    exit 1
fi

echo ""
echo "=================================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=================================================="
echo ""
echo "To start the demo:"
echo "  python kevin_demo.py"
echo ""
echo "Or start the API:"
echo "  uvicorn kevin_api:app --host 0.0.0.0 --port 8000"
echo ""
echo "Demo will be available at: http://localhost:7860"
echo "API will be available at: http://localhost:8000"
echo "API Docs: http://localhost:8000/api/docs"
echo ""
