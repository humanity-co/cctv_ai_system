import requests
import os

def download_file(url, target_path):
    print(f"📥 Downloading {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, stream=True, allow_redirects=True)
        response.raise_for_status()
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded to {target_path}")
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

if __name__ == "__main__":
    os.makedirs("datasets/fire_sense", exist_ok=True)
    os.makedirs("datasets/crime", exist_ok=True)
    os.makedirs("datasets/drive_india/fgvd_data", exist_ok=True)

    # 1. Verified Fire-Smoke GitHub (v1 release)
    download_file("https://github.com/DeepQuestAI/Fire-Smoke-Dataset/releases/download/v1/FIRE-SMOKE-DATASET.zip", "datasets/fire_sense/fire_smoke_github.zip")

    # 2. Verified FIRESENSE Zenodo
    download_file("https://zenodo.org/api/records/836749/files/fire_videos.1406.zip/content", "datasets/fire_sense/fire_videos.zip")
    download_file("https://zenodo.org/api/records/836749/files/smoke_videos.1407.zip/content", "datasets/fire_sense/smoke_videos.zip")

    # 3. Verified FGVD Zenodo (5.5GB)
    download_file("https://zenodo.org/api/records/7488960/files/IDD_FGVD.tar.gz/content", "datasets/drive_india/fgvd_data/IDD_FGVD.tar.gz")

    print("🚀 Background downloads complete.")
