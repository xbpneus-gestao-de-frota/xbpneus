
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def check_frontend_pages():
    print("\n--- Verificação de Funcionalidades de Frontend (Botões e Telas) ---")

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa o navegador em modo headless (sem interface gráfica)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Caminho para o chromedriver (instalado via apt-get)
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    base_url = "http://localhost:3000"
    # Rotas de exemplo, você pode adicionar mais com base no App.jsx
    # Como muitas rotas são protegidas, focaremos nas rotas de login e algumas públicas se houver.
    # Para testar rotas protegidas, seria necessário implementar um login.
    routes = [
        "/", # Página de Login
        "/cadastro", # Página de Cadastro
        "/pos-cadastro", # Página de Pós-Cadastro
        # Adicione mais rotas públicas ou que não exigem autenticação aqui
    ]

    for route in routes:
        url = f"{base_url}{route}"
        try:
            driver.get(url)
            time.sleep(2)  # Dar um tempo para a página carregar
            if "Error" not in driver.title and "Page not found" not in driver.page_source:
                print(f"[OK] {url} - Página carregada com sucesso. Título: {driver.title}")
            else:
                print(f"[ERRO] {url} - Página não carregou corretamente ou erro detectado. Título: {driver.title}")

            # Exemplo de verificação de elemento (pode ser adaptado para botões específicos)
            if route == "/":
                try:
                    login_button = driver.find_element(By.TAG_NAME, "button") # Procura por um botão genérico
                    print(f"[INFO] Botão encontrado na página de login: {login_button.text}")
                except: 
                    print("[INFO] Nenhum botão encontrado na página de login.")

        except Exception as e:
            print(f"[ERRO] {url} - Erro ao acessar a página: {e}")

    driver.quit()

if __name__ == "__main__":
    check_frontend_pages()

