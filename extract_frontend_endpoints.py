import re

def extract_frontend_urls(filepath):
    urls = set()
    with open(filepath, 'r') as f:
        content = f.read()

    # Regex para capturar URLs dentro de template literals com API_BASE_URL
    # Ex: `${API_BASE_URL}/api/users/register_full/`
    # Captura o que está entre `${API_BASE_URL}` e o `
    matches = re.findall(r"`\$\{API_BASE_URL\}(/api/[^`]+)/?`", content)
    for match in matches:
        urls.add(match)

    return sorted(list(urls))

if __name__ == '__main__':
    frontend_config_path = '/home/ubuntu/xbpneus/frontend/src/api/config.js'
    extracted_urls = extract_frontend_urls(frontend_config_path)
    with open('/home/ubuntu/xbpneus/frontend_endpoints.txt', 'w') as f:
        for url in extracted_urls:
            f.write(url + '\n')
EOF"
