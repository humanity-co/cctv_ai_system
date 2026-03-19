#!/bin/bash

# Kill all background processes on exit
trap "kill 0" EXIT

echo "🚀 Starting AI CCTV Surveillance System..."

# 1. Start Backend
echo "Backend: Starting FastAPI..."
export PYTHONPATH=$PYTHONPATH:.:/Users/devsmac/Library/Python/3.9/lib/python/site-packages
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# 2. Start Dashboard
echo "Dashboard: Starting React..."
cd dashboard && npm start &

# 3. Wait/Run Simulation (Optional)
echo "Simulation: Run 'python simulate.py' in a new terminal to see detections."

wait
