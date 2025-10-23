#!/usr/bin/env python3
"""
Script para testar o fluxo de autenticação e navegação no frontend do XBPneus.
Reproduz o problema de redirecionamento para a tela de login ao clicar em botões.
"""

import time
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configuração do Selenium
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")

# Inicializar o driver
driver = webdriver.Chrome(options=chrome_options)

# URLs base
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000/api"

# Dados de teste
TEST_USER = {
    "email": "transportador@test.com",
    "password": "senha123",
    "user_type": "transportador"
}

def log_test(message, status="INFO"):
    """Registra mensagens de teste com timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def test_login():
    """Testa o fluxo de login."""
    log_test("Iniciando teste de login...")
    
    try:
        driver.get(f"{BASE_URL}/login")
        log_test("Página de login carregada", "PASS")
        
        # Aguardar o carregamento da página
        time.sleep(2)
        
        # Verificar se o formulário de login está presente
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            log_test("Campo de email encontrado", "PASS")
        except:
            log_test("Campo de email NÃO encontrado", "FAIL")
            return False
        
        # Preencher o formulário de login
        email_input.send_keys(TEST_USER["email"])
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(TEST_USER["password"])
        
        # Clicar no botão de login
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()
        
        log_test("Botão de login clicado", "INFO")
        
        # Aguardar redirecionamento
        time.sleep(3)
        
        # Verificar se foi redirecionado para o dashboard ou volta para login
        current_url = driver.current_url
        log_test(f"URL atual após login: {current_url}", "INFO")
        
        if "/login" in current_url:
            log_test("Redirecionado para login (falha na autenticação)", "FAIL")
            return False
        elif "/dashboard" in current_url or "/motorista/dashboard" in current_url:
            log_test("Redirecionado para dashboard (sucesso)", "PASS")
            return True
        else:
            log_test(f"Redirecionado para URL inesperada: {current_url}", "WARN")
            return False
            
    except Exception as e:
        log_test(f"Erro durante login: {str(e)}", "FAIL")
        return False

def test_button_click_navigation():
    """Testa a navegação ao clicar em botões."""
    log_test("Iniciando teste de navegação por clique em botões...", "INFO")
    
    try:
        # Primeiro, fazer login
        if not test_login():
            log_test("Não foi possível fazer login. Abortando teste de navegação.", "FAIL")
            return False
        
        # Aguardar o dashboard carregar
        time.sleep(2)
        
        # Procurar por botões de navegação
        buttons = driver.find_elements(By.TAG_NAME, "button")
        log_test(f"Total de botões encontrados na página: {len(buttons)}", "INFO")
        
        # Testar alguns botões específicos
        test_buttons = [
            "Frota",
            "Pneus",
            "Estoque",
            "Manutenção",
            "Relatórios",
            "Configurações"
        ]
        
        for button_text in test_buttons:
            try:
                # Procurar pelo botão
                button = None
                for btn in driver.find_elements(By.TAG_NAME, "button"):
                    if button_text.lower() in btn.text.lower():
                        button = btn
                        break
                
                if not button:
                    # Tentar procurar em links
                    for link in driver.find_elements(By.TAG_NAME, "a"):
                        if button_text.lower() in link.text.lower():
                            button = link
                            break
                
                if button:
                    log_test(f"Clicando no botão: {button_text}", "INFO")
                    button.click()
                    time.sleep(2)
                    
                    current_url = driver.current_url
                    log_test(f"URL após clicar em {button_text}: {current_url}", "INFO")
                    
                    # Verificar se foi redirecionado para login
                    if "/login" in current_url:
                        log_test(f"PROBLEMA DETECTADO: Redirecionado para login ao clicar em {button_text}", "FAIL")
                    else:
                        log_test(f"Navegação bem-sucedida para {button_text}", "PASS")
                    
                    # Voltar ao dashboard
                    driver.get(f"{BASE_URL}/dashboard")
                    time.sleep(1)
                else:
                    log_test(f"Botão '{button_text}' não encontrado", "WARN")
                    
            except Exception as e:
                log_test(f"Erro ao testar botão {button_text}: {str(e)}", "FAIL")
        
        return True
        
    except Exception as e:
        log_test(f"Erro durante teste de navegação: {str(e)}", "FAIL")
        return False

def test_token_expiration():
    """Testa o comportamento quando o token expira."""
    log_test("Iniciando teste de expiração de token...", "INFO")
    
    try:
        # Fazer login
        if not test_login():
            log_test("Não foi possível fazer login. Abortando teste de expiração.", "FAIL")
            return False
        
        # Remover o token do localStorage para simular expiração
        driver.execute_script("localStorage.removeItem('access_token');")
        log_test("Token removido do localStorage", "INFO")
        
        # Tentar navegar para uma rota protegida
        driver.get(f"{BASE_URL}/dashboard")
        time.sleep(2)
        
        current_url = driver.current_url
        log_test(f"URL após remoção do token: {current_url}", "INFO")
        
        if "/login" in current_url:
            log_test("Redirecionado para login após expiração do token (comportamento esperado)", "PASS")
            return True
        else:
            log_test("NÃO foi redirecionado para login após expiração do token", "FAIL")
            return False
            
    except Exception as e:
        log_test(f"Erro durante teste de expiração: {str(e)}", "FAIL")
        return False

def test_api_response():
    """Testa as respostas da API de autenticação."""
    log_test("Iniciando teste de respostas da API...", "INFO")
    
    try:
        # Testar endpoint de token
        import requests
        
        login_data = {
            "username": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        
        response = requests.post(f"{API_URL}/token/", json=login_data)
        log_test(f"Status da resposta de token: {response.status_code}", "INFO")
        
        if response.status_code == 200:
            data = response.json()
            if "access" in data:
                log_test("Token obtido com sucesso", "PASS")
                return True
            else:
                log_test("Resposta não contém token de acesso", "FAIL")
                return False
        else:
            log_test(f"Erro na autenticação: {response.text}", "FAIL")
            return False
            
    except Exception as e:
        log_test(f"Erro ao testar API: {str(e)}", "FAIL")
        return False

def main():
    """Executa todos os testes."""
    log_test("=== INICIANDO TESTES DE AUTENTICAÇÃO E NAVEGAÇÃO ===", "INFO")
    
    try:
        # Executar testes
        results = {
            "API Response": test_api_response(),
            "Login": test_login(),
            "Button Navigation": test_button_click_navigation(),
            "Token Expiration": test_token_expiration(),
        }
        
        # Resumo dos resultados
        log_test("=== RESUMO DOS TESTES ===", "INFO")
        for test_name, result in results.items():
            status = "PASS" if result else "FAIL"
            log_test(f"{test_name}: {status}", status)
        
        # Verificar se todos os testes passaram
        all_passed = all(results.values())
        if all_passed:
            log_test("Todos os testes passaram!", "PASS")
        else:
            log_test("Alguns testes falharam. Verifique os logs acima.", "FAIL")
        
    finally:
        # Fechar o driver
        driver.quit()
        log_test("Driver fechado", "INFO")

if __name__ == "__main__":
    main()

