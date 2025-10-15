import re

def extract_frontend_urls_simple(filepath):
    urls = set()
    with open(filepath, 'r') as f:
        content = f.read()

    # Regex para capturar strings que começam com /api/ dentro de aspas simples, duplas ou crases
    # Isso deve cobrir a maioria dos casos de endpoints definidos no config.js
    matches = re.findall(r"['\"`](/api/[^'\"`]+)['\"`]", content)
    for match in matches:
        urls.add(match)

    return sorted(list(urls))

if __name__ == '__main__':
    frontend_config_path = '/home/ubuntu/xbpneus/frontend/src/api/config.js'
    extracted_urls = extract_frontend_urls_simple(frontend_config_path)
    with open('frontend_endpoints.txt', 'w') as f:
        for url in extracted_urls:
            f.write(url + '\n')
EOF"
