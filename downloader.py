import os
import subprocess
import requests

def download_hf_dataset(dataset_id, target_dir):
    """Downloads a dataset from Hugging Face using huggingface-cli."""
    print(f"📥 Downloading from Hugging Face: {dataset_id}...")
    try:
        # Use huggingface-cli to download (assumes user might not be logged in, so public only)
        subprocess.run([
            "huggingface-cli", "download", dataset_id, 
            "--local-dir", target_dir, 
            "--local-dir-use-symlinks", "False"
        ], check=True)
        print(f"✅ Success: {dataset_id} -> {target_dir}")
    except Exception as e:
        print(f"❌ Failed to download {dataset_id}: {e}")

def download_roboflow_dataset(model_id, target_dir):
    """
    Downloads from Roboflow Universe.
    Note: Requires ROBOFLOW_API_KEY if private, but many are public.
    """
    print(f"📥 Downloading from Roboflow: {model_id}...")
    # This usually requires the 'roboflow' python package.
    # For now, I'll provide a placeholder or use CURL if I have a direct link.
    print("⚠️ Roboflow downloads often require an API key. Please set ROBOFLOW_API_KEY.")

if __name__ == "__main__":
    # Ensure tool directories exist
    os.makedirs("datasets/drive_india/uvh26", exist_ok=True)
    os.makedirs("datasets/plates/roboflow", exist_ok=True)
    os.makedirs("datasets/fire_sense/kaggle", exist_ok=True)

    # 1. Download UVH-26
    # download_hf_dataset("iisc-aim/UVH-26", "datasets/drive_india/uvh26")
    
    # 2. Download a sample of UCF-Crime (if direct link is known)
    # Direct link for a subset often used in benchmarks
    print("🚀 Ready to download. Please ensure 'huggingface_hub' is installed.")
