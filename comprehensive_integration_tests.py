#!/usr/bin/env python3
"""
Script Abrangente de Testes de Integração Frontend-Backend
Testa fluxos completos de usuário e interações entre frontend e backend
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
API_BASE = f"{BASE_URL}/api"

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TestRunner:
    def __init__(self):
        self.test_results = []
        self.auth_token = None
        self.user_id = None
        
    def print_header(self, text):
        """Imprime um cabeçalho formatado"""
        print(f"\n{BLUE}{'='*70}")
        print(f"{text:^70}")
        print(f"{'='*70}{RESET}\n")
    
    def print_test(self, name, status, details=""):
        """Registra e imprime resultado de teste"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if status == "PASS":
            symbol = f"{GREEN}✓{RESET}"
            color = GREEN
        elif status == "FAIL":
            symbol = f"{RED}✗{RESET}"
            color = RED
        else:
            symbol = f"{YELLOW}⚠{RESET}"
            color = YELLOW
        
        print(f"{symbol} {name}")
        if details:
            print(f"  {color}→ {details}{RESET}")
        
        self.test_results.append({
            "timestamp": timestamp,
            "name": name,
            "status": status,
            "details": details
        })
    
    def test_backend_connectivity(self):
        """Testa conectividade com o backend"""
        self.print_header("Teste 1: Conectividade com Backend")
        
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            self.print_test("Conexão com Backend", "PASS", f"Status: {response.status_code}")
            return True
        except Exception as e:
            self.print_test("Conexão com Backend", "FAIL", str(e))
            return False
    
    def test_frontend_connectivity(self):
        """Testa conectividade com o frontend"""
        self.print_header("Teste 2: Conectividade com Frontend")
        
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            self.print_test("Conexão com Frontend", "PASS", f"Status: {response.status_code}")
            return True
        except Exception as e:
            self.print_test("Conexão com Frontend", "FAIL", str(e))
            return False
    
    def test_api_documentation(self):
        """Testa endpoints de documentação da API"""
        self.print_header("Teste 3: Documentação da API")
        
        # Teste de Schema
        try:
            response = requests.get(f"{API_BASE}/schema/", timeout=5)
            if response.status_code == 200:
                self.print_test("Schema OpenAPI", "PASS", "Documentação acessível")
            else:
                self.print_test("Schema OpenAPI", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_test("Schema OpenAPI", "FAIL", str(e))
        
        # Teste de Docs
        try:
            response = requests.get(f"{API_BASE}/docs/", timeout=5)
            if response.status_code == 200:
                self.print_test("Documentação DRF", "PASS", "Documentação acessível")
            else:
                self.print_test("Documentação DRF", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_test("Documentação DRF", "FAIL", str(e))
    
    def test_authentication_flow(self):
        """Testa fluxo de autenticação"""
        self.print_header("Teste 4: Fluxo de Autenticação")
        
        # Teste de login
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/token/",
                json=login_data,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'access' in data:
                    self.auth_token = data['access']
                    self.print_test("Login", "PASS", "Token obtido com sucesso")
                    
                    # Teste de obtenção de dados do usuário
                    headers = {"Authorization": f"Bearer {self.auth_token}"}
                    response = requests.get(
                        f"{API_BASE}/auth/me/",
                        headers=headers,
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        user_data = response.json()
                        self.user_id = user_data.get('id')
                        self.print_test("Obtenção de Dados do Usuário", "PASS", f"Usuário: {user_data.get('username')}")
                    else:
                        self.print_test("Obtenção de Dados do Usuário", "FAIL", f"Status: {response.status_code}")
                else:
                    self.print_test("Login", "FAIL", "Token não encontrado na resposta")
            else:
                self.print_test("Login", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_test("Login", "FAIL", str(e))
    
    def test_transportador_module(self):
        """Testa módulo transportador"""
        self.print_header("Teste 5: Módulo Transportador")
        
        if not self.auth_token:
            self.print_test("Módulo Transportador", "FAIL", "Autenticação necessária")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        endpoints = [
            ("motorista", "Motoristas"),
            ("frota", "Frota"),
            ("pneus", "Pneus"),
            ("manutencao", "Manutenção"),
            ("estoque", "Estoque"),
            ("custos", "Custos"),
            ("combustivel", "Combustível"),
            ("multas", "Multas"),
            ("viagens", "Viagens"),
            ("clientes", "Clientes"),
            ("fornecedores", "Fornecedores"),
            ("dashboards", "Dashboards"),
            ("relatorios", "Relatórios"),
        ]
        
        success_count = 0
        for endpoint, name in endpoints:
            try:
                response = requests.get(
                    f"{API_BASE}/transportador/{endpoint}/",
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code == 200:
                    self.print_test(f"Transportador - {name}", "PASS", "Endpoint acessível")
                    success_count += 1
                else:
                    self.print_test(f"Transportador - {name}", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.print_test(f"Transportador - {name}", "FAIL", str(e))
        
        print(f"\n{BLUE}Resumo: {success_count}/{len(endpoints)} endpoints funcionais{RESET}")
    
    def test_missing_endpoints(self):
        """Testa endpoints que podem estar faltando"""
        self.print_header("Teste 6: Endpoints Ausentes/Com Problemas")
        
        endpoints = [
            ("approve", "Aprovação de Usuários"),
            ("motorista", "Módulo Motorista (raiz)"),
            ("borracharia", "Módulo Borracharia (raiz)"),
            ("revenda", "Módulo Revenda (raiz)"),
            ("recapagem", "Módulo Recapagem (raiz)"),
            ("reports", "Relatórios (raiz)"),
            ("jobs", "Jobs (raiz)"),
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(
                    f"{API_BASE}/{endpoint}/",
                    timeout=5
                )
                
                if response.status_code == 200:
                    self.print_test(f"Endpoint: {name}", "PASS", "Implementado")
                elif response.status_code == 404:
                    self.print_test(f"Endpoint: {name}", "FAIL", "Não encontrado (404)")
                elif response.status_code == 405:
                    self.print_test(f"Endpoint: {name}", "FAIL", "Método não permitido (405)")
                elif response.status_code == 401:
                    self.print_test(f"Endpoint: {name}", "FAIL", "Autenticação necessária (401)")
                else:
                    self.print_test(f"Endpoint: {name}", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.print_test(f"Endpoint: {name}", "FAIL", str(e))
    
    def test_frontend_pages(self):
        """Testa carregamento de páginas do frontend"""
        self.print_header("Teste 7: Páginas do Frontend")
        
        pages = [
            ("/", "Página Inicial"),
            ("/login", "Login"),
            ("/cadastro", "Cadastro"),
            ("/pos-cadastro", "Pós-Cadastro"),
        ]
        
        for path, name in pages:
            try:
                response = requests.get(
                    f"{FRONTEND_URL}{path}",
                    timeout=5
                )
                
                if response.status_code == 200:
                    self.print_test(f"Página: {name}", "PASS", "Carregada com sucesso")
                else:
                    self.print_test(f"Página: {name}", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.print_test(f"Página: {name}", "FAIL", str(e))
    
    def test_error_handling(self):
        """Testa tratamento de erros"""
        self.print_header("Teste 8: Tratamento de Erros")
        
        # Teste de endpoint inexistente
        try:
            response = requests.get(
                f"{API_BASE}/endpoint-inexistente/",
                timeout=5
            )
            
            if response.status_code == 404:
                self.print_test("Erro 404 - Endpoint Inexistente", "PASS", "Retorna 404 corretamente")
            else:
                self.print_test("Erro 404 - Endpoint Inexistente", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_test("Erro 404 - Endpoint Inexistente", "FAIL", str(e))
        
        # Teste de autenticação inválida
        try:
            headers = {"Authorization": "Bearer token_invalido"}
            response = requests.get(
                f"{API_BASE}/auth/me/",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 401:
                self.print_test("Erro 401 - Token Inválido", "PASS", "Retorna 401 corretamente")
            else:
                self.print_test("Erro 401 - Token Inválido", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_test("Erro 401 - Token Inválido", "FAIL", str(e))
    
    def generate_report(self):
        """Gera relatório de testes"""
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
        
        # Salvar relatório em arquivo
        report_file = "/home/ubuntu/xbpneus/test_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\nRelatório salvo em: {report_file}")
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print(f"\n{BLUE}{'='*70}")
        print("BATERIA ABRANGENTE DE TESTES DE INTEGRAÇÃO")
        print("Sistema XBPneus")
        print(f"{'='*70}{RESET}\n")
        
        self.test_backend_connectivity()
        self.test_frontend_connectivity()
        self.test_api_documentation()
        self.test_authentication_flow()
        self.test_transportador_module()
        self.test_missing_endpoints()
        self.test_frontend_pages()
        self.test_error_handling()
        self.generate_report()
        
        print(f"\n{BLUE}{'='*70}")
        print("FIM DOS TESTES")
        print(f"{'='*70}{RESET}\n")

def main():
    runner = TestRunner()
    runner.run_all_tests()

if __name__ == "__main__":
    main()

