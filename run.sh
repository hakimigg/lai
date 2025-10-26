#!/data/data/com.termux/files/usr/bin/bash
# CodeMaster AI - Termux Edition Launcher

echo "🚀 Starting CodeMaster AI - Termux Edition..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Installing..."
    pkg install python -y
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Installing..."
    pkg install python-pip -y
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Setting up virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

# Run the application
echo "✅ Launching CodeMaster AI..."
echo ""
python main.py

# Deactivate virtual environment on exit
deactivate
