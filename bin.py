import requests


def download_subtitle(download_url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(download_url, headers=headers)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Subtitle downloaded successfully: {filename}")
    else:
        print(f"Failed to download subtitle. Status code: {response.status_code}")
        
        