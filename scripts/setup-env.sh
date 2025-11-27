#!/bin/bash
# setup-env.sh - Set up project-local Python virtual environment
#
# Purpose: Create isolated Python environment within project directory
# Usage: ./scripts/setup-env.sh

set -e

PLUGIN_ROOT="$(cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")" && pwd)"
VENV_DIR="${PLUGIN_ROOT}/venv"

echo "🔧 Setting up Project Catalyst Python environment..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "Found Python ${PYTHON_VERSION}"
echo ""

# Create virtual environment if it doesn't exist
if [ -d "${VENV_DIR}" ]; then
    echo "✅ Virtual environment already exists at: ${VENV_DIR}"
    echo ""
else
    echo "Creating virtual environment at: ${VENV_DIR}"
    python3 -m venv "${VENV_DIR}"

    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi

    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
if [ -f "${VENV_DIR}/Scripts/activate" ]; then
    # Windows (Git Bash)
    source "${VENV_DIR}/Scripts/activate"
elif [ -f "${VENV_DIR}/bin/activate" ]; then
    # Unix/Mac
    source "${VENV_DIR}/bin/activate"
else
    echo "❌ Could not find activate script"
    exit 1
fi

echo "Activated virtual environment"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet

if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Failed to upgrade pip (continuing anyway)"
else
    echo "✅ pip upgraded"
fi
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r "${PLUGIN_ROOT}/requirements.txt" --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Verify installation
echo "Verifying installation..."
python -c "import yaml; print('  ✅ PyYAML:', yaml.__version__)"
python -c "import pytest; print('  ✅ pytest:', pytest.__version__)"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in your terminal:"
echo "  Windows (Git Bash): source venv/Scripts/activate"
echo "  Unix/Mac:           source venv/bin/activate"
echo ""
echo "To deactivate:"
echo "  deactivate"
echo ""
echo "Python location:"
which python
