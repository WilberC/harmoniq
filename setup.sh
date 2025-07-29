#!/bin/bash

# Harmoniq Project Setup Script

echo "🎵 Setting up Harmoniq Music Streaming Application..."
echo ""

# Check if Python 3.9+ is available
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    echo "   Please install Node.js from https://nodejs.org/"
    exit 1
fi

node_version=$(node --version)
echo "✅ Node.js version: $node_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Initialize database
echo "🗄️  Initializing database..."
cd backend
python init_db.py
cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "To start the application, run:"
echo "   ./start.sh"
echo ""
echo "Or start services individually:"
echo "   Backend:  cd backend && python run.py"
echo "   Frontend: cd frontend && npm run dev"
echo ""
echo "Access points:"
echo "   Frontend:    http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs:    http://localhost:8000/docs" 