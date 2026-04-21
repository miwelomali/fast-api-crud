#!/bin/bash
set -e  # Stop immediately if a command fails

# 0. Configuration
export DAGGER_ENGINE_HOST=docker-container://dagger-engine-v0.20.6
export DOCKER_HOST=unix:///var/run/docker.sock

# 1. Automatic Cleanup Function
# This function runs on any exit (success, error, or Ctrl+C)
cleanup() {
    echo "🧹 Automatically cleaning up environment..."
    # 'deactivate' is a shell function only available when the venv is active
    if command -v deactivate &> /dev/null; then
        deactivate || true
    fi
    rm -rf .venv
    echo "✨ Repository is clean."
}

# Register the cleanup function to trigger on script EXIT
trap cleanup EXIT

# 2. Setup Environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Dependencies (matching Dagger v0.20.6)
echo "🔄 Installing Python dependencies..."
pip install --upgrade pip
pip install dagger-io==0.20.6 pytest httpx anyio

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 4. Handle Docker Permissions
if [ ! -w /var/run/docker.sock ]; then
    echo "🔐 Fixing Docker socket permissions..."
    sudo chmod 666 /var/run/docker.sock
fi

# 5. Run Test Pipeline
echo "🧪 Running Dagger test pipeline..."
python dagger/case_test_pipeline.py

# 6. Run Local Tests
echo "🧪 Running local pytest (stopping on first failure)..."
pytest -x

# The cleanup() function defined in Step 1 will run now automatically.
