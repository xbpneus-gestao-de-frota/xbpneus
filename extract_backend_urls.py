import os
import re

def extract_urls_from_file(filepath):
    urls = []
    with open(filepath, 'r') as f:
        content = f.read()

    # Regex para capturar paths simples e de router
    for match in re.finditer(r"path\([\'\"]([a-zA-Z0-9_\-/]+)[\'\"]", content):
        urls.append(match.group(1))
    
    for match in re.finditer(r"router\.register\([\'\"]([a-zA-Z0-9_\-/]+)[\'\"]", content):
        urls.append(match.group(1))

    return urls

def main():
    backend_dir = 'backend'
    all_backend_urls = set()

    for root, _, files in os.walk(backend_dir):
        for file in files:
            if file == 'urls.py':
                filepath = os.path.join(root, file)
                extracted_urls = extract_urls_from_file(filepath)
                for url_pattern in extracted_urls:
                    all_backend_urls.add(url_pattern)

    config_urls_path = 'config/urls.py'
    if os.path.exists(config_urls_path):
        with open(config_urls_path, 'r') as f:
            config_content = f.read()
            
            for match in re.finditer(r"path\([\'\"]([a-zA-Z0-9_\-/]+)[\'\"]", config_content):
                all_backend_urls.add(match.group(1))
            
            for match in re.finditer(r"try_include\([\'\"]([a-zA-Z0-9_\-/]+)[\'\"]", config_content):
                prefix = match.group(1)
                all_backend_urls.add(prefix)

    for url in sorted(list(all_backend_urls)):
        print(url)

if __name__ == '__main__':
    main()
EOF"

source /home/ubuntu/.user_env && cd . && python extract_backend_urls.py > backend_endpoints.txt
