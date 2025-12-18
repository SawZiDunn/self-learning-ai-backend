#!/bin/bash

# Issa Compass Setup Script
# Automates the setup process

set -e

echo "🧭 Issa Compass Setup Script"
echo "=============================="
echo ""

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi
echo "✅ Python found: $(python3 --version)"
echo ""

# Check pip
echo "Checking pip..."
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip not found. Please install pip."
    exit 1
fi
echo "✅ pip found"
echo ""

# Create .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env created"
    echo "⚠️  Please edit .env and add your API keys!"
    echo ""
else
    echo "✅ .env already exists"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Test imports
echo "Testing imports..."
python3 -c "from config import Config; from database import supabase; from llm_integration import groq_client" 2>/dev/null && echo "✅ All imports successful" || echo "⚠️  Some imports failed - check your .env"
echo ""

# Initialize database (if possible)
echo "Initializing database..."
python3 -c "from database import init_database; init_database()" 2>/dev/null && echo "✅ Database initialized" || echo "⚠️  Database initialization failed - check your Supabase credentials"
echo ""

echo "=============================="
echo "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys (if not done)"
echo "2. Run: python3 app.py"
echo "3. Visit: http://localhost:5000"
echo ""
echo "For full instructions, see README.md"
echo "=============================="
