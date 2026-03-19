import requests
import json

def peek_zenodo(record_id):
    print(f"🔍 Peeking at Zenodo Record: {record_id}")
    url = f"https://zenodo.org/api/records/{record_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Record: {data['metadata']['title']}")
        for f in data.get('files', []):
            print(f"- File: {f['key']}, Link: {f['links']['self']}")
    except Exception as e:
        print(f"❌ Failed to peek Zenodo {record_id}: {e}")

def peek_github_releases(repo):
    print(f"🔍 Peeking at GitHub Releases: {repo}")
    url = f"https://api.github.com/repos/{repo}/releases"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for release in data:
            print(f"✅ Release: {release['tag_name']}")
            for asset in release.get('assets', []):
                print(f"- Asset: {asset['name']}, Link: {asset['browser_download_url']}")
    except Exception as e:
        print(f"❌ Failed to peek GitHub {repo}: {e}")

if __name__ == "__main__":
    peek_zenodo("7488960") # FGVD
    peek_zenodo("836749")  # FIRESENSE
    peek_github_releases("DeepQuestAI/Fire-Smoke-Dataset")
