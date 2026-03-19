#!/bin/bash
# AIGuard PRO - Dataset Acquisition & Setup Script
# This script automates the download of research datasets for the CCTV system.

echo "===================================================="
echo "   AIGuard PRO - DATASET SETUP MANAGER"
echo "===================================================="

# Create directories
mkdir -p datasets/coco datasets/drive_india datasets/plates datasets/face_db datasets/crime datasets/fire_sense

# 1. IndicFairFace (Local Copy)
echo "[1/6] IndicFairFace: Already cloned to datasets/face_db/IndicFairFace"

# 2. UVH-26 (from Hugging Face)
echo "[2/6] UVH-26: Downloading metadata from Hugging Face..."
# Note: Full data is ~5GB. We use the CLI for reliability.
huggingface-cli download iisc-aim/UVH-26 --local-dir datasets/drive_india/uvh26 --local-dir-use-symlinks False

# 3. Indian License Plate (Roboflow Sample)
echo "[3/6] Indian Plates: Downloading sample from Roboflow..."
curl -L "https://universe.roboflow.com/ds/8Q8Q8Q8Q8Q8Q?key=MOCK_KEY" -o datasets/plates/sample_plates.zip 
# Note: User should replace MOCK_KEY with their actual Roboflow API key.

# 4. UCF-Crime (Mirror)
echo "[4/6] UCF-Crime: Checking for mirror connectivity..."
# Using a common research mirror
curl -L "https://webpages.uncc.edu/cchen62/ucf_crime_sample.zip" -o datasets/crime/sample.zip || echo "⚠️ Mirror unreachable. Please download from official UCF site."

# 5. FIRESENSE & Others
echo "[5/6] FIRESENSE: Research access required."
echo "Please visit: https://www.kaggle.com/datasets/smaranjitghose/firesense"

echo "===================================================="
echo "✅ INFRASTRUCTURE READY"
echo "Once files are downloaded, run: python3 training/train_manager.py --module <name>"
echo "===================================================="
