#!/usr/bin/env python3
"""
Script de Testes de Responsividade do Frontend
Testa o carregamento e layout das páginas em diferentes tamanhos de tela
"""

import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Configuração
FRONTEND_URL = "http://localhost:3000"

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class ResponsiveDesignTester:
    def __init__(self):
        self.test_results = []
        self.driver = None
        
        # Tamanhos de tela para testar (width, height, device_name)
        self.screen_sizes = [
            (1920, 1080, "Desktop (1920x1080)"),
            (1366, 768, "Laptop (1366x768)"),
            (768, 1024, "Tablet (768x1024)"),
            (375, 667, "Mobile (375x667)"),
            (414, 896, "Mobile Large (414x896)"),
        ]
        
        # Páginas para testar
        self.pages = [
            ("/", "Página Inicial"),
            ("/login", "Login"),
            ("/cadastro", "Cadastro"),
            ("/pos-cadastro", "Pós-Cadastro"),
        ]
    
    def print_header(self, text):
        """Imprime um cabeçalho formatado"""
        print(f"\n{BLUE}{'='*70}")
        print(f"{text:^70}")
        print(f"{'='*70}{RESET}\n")
    
    def print_test(self, name, status, details=""):
        """Registra e imprime resultado de teste"""
        if status == "PASS":
            symbol = f"{GREEN}✓{RESET}"
        elif status == "FAIL":
            symbol = f"{RED}✗{RESET}"
        else:
            symbol = f"{YELLOW}⚠{RESET}"
        
        print(f"{symbol} {name}")
        if details:
            print(f"  → {details}")
        
        self.test_results.append({
            "name": name,
            "status": status,
            "details": details
        })
    
    def setup_driver(self):
        """Configura o driver do Selenium"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--headless=new") # Novo modo headless
            chrome_options.add_argument("--disable-features=RendererCodeIntegrity") # Pode resolver problemas de inicialização
            chrome_options.add_argument("--window-size=1920,1080") # Definir um tamanho inicial de janela
            chrome_options.add_argument("--start-maximized") # Maximizar janela ao iniciar
            
            service = Service(executable_path="/usr/bin/chromedriver")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.print_test("Inicialização do Selenium", "PASS", "Driver configurado")
            return True
        except Exception as e:
            self.print_test("Inicialização do Selenium", "FAIL", str(e))
            return False
    
    def test_page_load(self, url, page_name, width, height, device_name):
        """Testa carregamento de página em um tamanho específico"""
        try:
            # Definir tamanho da janela
            self.driver.set_window_size(width, height)
            time.sleep(0.5)
            
            # Navegar para a página
            full_url = f"{FRONTEND_URL}{url}"
            self.driver.get(full_url)
            
            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Verificar se há erros no console
            logs = self.driver.get_log('browser')
            errors = [log for log in logs if log['level'] == 'SEVERE']
            
            if errors:
                error_messages = [log['message'] for log in errors]
                self.print_test(
                    f"{page_name} - {device_name}",
                    "WARNING",
                    f"Erros no console: {len(errors)}"
                )
            else:
                self.print_test(
                    f"{page_name} - {device_name}",
                    "PASS",
                    f"Carregado em {device_name}"
                )
            
            return True
        except Exception as e:
            self.print_test(
                f"{page_name} - {device_name}",
                "FAIL",
                str(e)
            )
            return False
    
    def test_element_visibility(self, page_url, page_name, width, height, device_name):
        """Testa visibilidade de elementos em diferentes tamanhos"""
        try:
            self.driver.set_window_size(width, height)
            time.sleep(0.5)
            
            full_url = f"{FRONTEND_URL}{page_url}"
            self.driver.get(full_url)
            
            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Verificar se há elementos com display:none ou visibility:hidden
            hidden_elements = self.driver.execute_script("""
                var elements = document.querySelectorAll('*');
                var hidden = [];
                elements.forEach(function(el) {
                    var style = window.getComputedStyle(el);
                    if (style.display === 'none' || style.visibility === 'hidden') {
                        hidden.push(el.tagName);
                    }
                });
                return hidden.length;
            """)
            
            # Verificar scroll horizontal
            has_horizontal_scroll = self.driver.execute_script("""
                return document.documentElement.scrollWidth > window.innerWidth;
            """)
            
            if has_horizontal_scroll:
                self.print_test(
                    f"Scroll Horizontal - {page_name} ({device_name})",
                    "WARNING",
                    "Página tem scroll horizontal"
                )
            else:
                self.print_test(
                    f"Scroll Horizontal - {page_name} ({device_name})",
                    "PASS",
                    "Sem scroll horizontal"
                )
            
            return True
        except Exception as e:
            self.print_test(
                f"Visibilidade de Elementos - {page_name} ({device_name})",
                "FAIL",
                str(e)
            )
            return False
    
    def test_button_clickability(self, page_url, page_name, width, height, device_name):
        """Testa se botões são clicáveis em diferentes tamanhos"""
        try:
            self.driver.set_window_size(width, height)
            time.sleep(0.5)
            
            full_url = f"{FRONTEND_URL}{page_url}"
            self.driver.get(full_url)
            
            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Encontrar todos os botões
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            
            if buttons:
                # Verificar se os botões são clicáveis
                clickable_count = 0
                for button in buttons[:3]:  # Testar apenas os 3 primeiros
                    try:
                        # Verificar se o botão é visível
                        if button.is_displayed():
                            clickable_count += 1
                    except:
                        pass
                
                self.print_test(
                    f"Botões Clicáveis - {page_name} ({device_name})",
                    "PASS",
                    f"{clickable_count} botões visíveis"
                )
            else:
                self.print_test(
                    f"Botões Clicáveis - {page_name} ({device_name})",
                    "WARNING",
                    "Nenhum botão encontrado"
                )
            
            return True
        except Exception as e:
            self.print_test(
                f"Botões Clicáveis - {page_name} ({device_name})",
                "FAIL",
                str(e)
            )
            return False
    
    def run_all_tests(self):
        """Executa todos os testes de responsividade"""
        self.print_header("TESTES DE RESPONSIVIDADE DO FRONTEND")
        
        if not self.setup_driver():
            return
        
        try:
            # Teste de carregamento de páginas
            self.print_header("Teste 1: Carregamento de Páginas")
            
            for page_url, page_name in self.pages:
                for width, height, device_name in self.screen_sizes:
                    self.test_page_load(page_url, page_name, width, height, device_name)
                    time.sleep(0.5)
            
            # Teste de visibilidade de elementos
            self.print_header("Teste 2: Visibilidade de Elementos")
            
            for page_url, page_name in self.pages:
                for width, height, device_name in self.screen_sizes:
                    self.test_element_visibility(page_url, page_name, width, height, device_name)
                    time.sleep(0.5)
            
            # Teste de clicabilidade de botões
            self.print_header("Teste 3: Clicabilidade de Botões")
            
            for page_url, page_name in self.pages:
                for width, height, device_name in self.screen_sizes:
                    self.test_button_clickability(page_url, page_name, width, height, device_name)
                    time.sleep(0.5)
            
            # Gerar relatório
            self.print_header("Relatório de Testes")
            
            total_tests = len(self.test_results)
            passed_tests = sum(1 for t in self.test_results if t['status'] == 'PASS')
            failed_tests = sum(1 for t in self.test_results if t['status'] == 'FAIL')
            warning_tests = sum(1 for t in self.test_results if t['status'] == 'WARNING')
            
            success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            
            print(f"Total de Testes: {total_tests}")
            print(f"{GREEN}Passou: {passed_tests}{RESET}")
            print(f"{RED}Falhou: {failed_tests}{RESET}")
            print(f"{YELLOW}Avisos: {warning_tests}{RESET}")
            print(f"\nTaxa de Sucesso: {success_rate:.1f}%")
            
        finally:
            if self.driver:
                self.driver.quit()
            
            print(f"\n{BLUE}{'='*70}")
            print("FIM DOS TESTES DE RESPONSIVIDADE")
            print(f"{'='*70}{RESET}\n")

def main():
    tester = ResponsiveDesignTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()

