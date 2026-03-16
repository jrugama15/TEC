import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

base_url = "http://websitemigrado.desarrollo.tecnacional.edu.ni/"
output_dir = "."

def download_file(url, folder):
    try:
        parsed = urlparse(url)
        if not parsed.netloc or parsed.netloc == urlparse(base_url).netloc:
            # It's a relative or same-domain URL
            path = parsed.path.lstrip('/')
            if not path:
                return url
                
            local_path = os.path.join(folder, path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            if not os.path.exists(local_path):
                print(f"Downloading {url} to {local_path}...")
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
            
            return path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return url

def main():
    print("Fetching main page...")
    response = requests.get(base_url)
    if response.status_code != 200:
        print("Failed to fetch main page.")
        return
        
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Download CSS, JS, images
    tags = {
        'link': 'href',
        'script': 'src',
        'img': 'src',
        'source': 'src',
    }
    
    for tag, attr in tags.items():
        for el in soup.find_all(tag):
            url = el.get(attr)
            if url:
                full_url = urljoin(base_url, url)
                local_path = download_file(full_url, output_dir)
                if local_path and not url.startswith('http') and not url.startswith('//'):
                    el[attr] = local_path
                    
    # Save modified HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print("Download complete.")

if __name__ == "__main__":
    main()
