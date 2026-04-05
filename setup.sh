#!/bin/bash
# Disease Prediction System - Setup Script
# This script automates the complete setup process

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║ Disease Prediction System - Setup Script              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}[1] Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python version: $python_version${NC}"

# Create virtual environment
echo -e "\n${YELLOW}[2] Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}[3] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "\n${YELLOW}[4] Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo -e "\n${YELLOW}[5] Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check data files
echo -e "\n${YELLOW}[6] Checking data files...${NC}"
if [ -f "data/Training.csv" ] && [ -f "data/Testing.csv" ]; then
    echo -e "${GREEN}✓ Data files found${NC}"
    echo "  - Training samples: $(wc -l < data/Training.csv)"
    echo "  - Testing samples: $(wc -l < data/Testing.csv)"
else
    echo -e "${RED}✗ Data files not found${NC}"
    echo "  Please copy Training.csv and Testing.csv to the 'data' directory"
    echo "  Current contents of data/:"
    ls -la data/ || echo "  (data directory is empty)"
fi

# Create directories
echo -e "\n${YELLOW}[7] Creating necessary directories...${NC}"
mkdir -p data logs
echo -e "${GREEN}✓ Directories created${NC}"

# Display next steps
echo -e "\n${YELLOW}[8] Setup Complete!${NC}"
echo ""
echo "════════════════════════════════════════════════════════"
echo -e "${GREEN}NEXT STEPS:${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo "1. Ensure data files are in place:"
echo "   cp /path/to/Training.csv data/"
echo "   cp /path/to/Testing.csv data/"
echo ""
echo "2. Train the machine learning model:"
echo "   python train.py"
echo ""
echo "3. Run the Streamlit application:"
echo "   streamlit run app.py"
echo ""
echo "4. Build Docker image:"
echo "   docker build -t disease-predictor:latest ."
echo ""
echo "5. Run with Docker Compose:"
echo "   docker-compose up -d"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""
echo "Virtual environment: source venv/bin/activate"
echo "Deactivate: deactivate"
echo ""
echo -e "${GREEN}Setup completed successfully!${NC}"
