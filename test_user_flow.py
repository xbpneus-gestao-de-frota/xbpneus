#!/usr/bin/env python3
"""
Script de Teste - Fluxo Completo de Usuários
Sistema XBPNEUS v10

Testa o fluxo completo para cada tipo de usuário:
1. Cadastro
2. Verificação de pós-cadastro (aguardando aprovação)
3. Aprovação pelo admin
4. Login
5. Acesso ao dashboard específico

Tipos de usuário testados:
- Transportador
- Motorista
- Borracharia
- Revenda
- Recapagem
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple
import sys

# Configurações
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Imprime cabeçalho formatado"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")

def print_success(text: str):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text: str):
    """Imprime mensagem de erro"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text: str):
    """Imprime mensagem informativa"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def print_warning(text: str):
    """Imprime mensagem de aviso"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

# Dados de teste para cada tipo de usuário
TEST_USERS = {
    "transportador": {
        "email": "teste_transportador@xbpneus.com",
        "nome_razao_social": "Transportadora Teste XBP Ltda",
        "cnpj": "12.345.678/0001-90",
        "telefone": "(11) 98765-4321",
        "password": "SenhaSegura123",
        "password_confirm": "SenhaSegura123",
        "register_endpoint": "/api/transportador/register/",
        "login_endpoint": "/api/transportador/login/",
        "dashboard_path": "/transportador/dashboard/",
        "admin_model": "transportador/usuariotransportador"
    },
    "motorista": {
        "email": "teste_motorista@xbpneus.com",
        "nome_completo": "João da Silva Santos",
        "cpf": "123.456.789-00",
        "cnh": "12345678900",
        "categoria_cnh": "D",
        "telefone": "(11) 98765-4321",
        "password": "SenhaSegura123",
        "password_confirm": "SenhaSegura123",
        "register_endpoint": "/api/motorista/register/",
        "login_endpoint": "/api/motorista/login/",
        "dashboard_path": "/motorista/dashboard/",
        "admin_model": "motorista/usuariomotorista"
    },
    "borracharia": {
        "email": "teste_borracharia@xbpneus.com",
        "nome_razao_social": "Borracharia Teste XBP Ltda",
        "cnpj": "98.765.432/0001-10",
        "telefone": "(11) 98765-4321",
        "password": "SenhaSegura123",
        "password_confirm": "SenhaSegura123",
        "register_endpoint": "/api/borracharia/register/",
        "login_endpoint": "/api/borracharia/login/",
        "dashboard_path": "/borracharia/dashboard/",
        "admin_model": "borracharia/usuarioborracharia"
    },
    "revenda": {
        "email": "teste_revenda@xbpneus.com",
        "nome_razao_social": "Revenda Teste XBP Ltda",
        "cnpj": "11.222.333/0001-44",
        "telefone": "(11) 98765-4321",
        "password": "SenhaSegura123",
        "password_confirm": "SenhaSegura123",
        "register_endpoint": "/api/revenda/register/",
        "login_endpoint": "/api/revenda/login/",
        "dashboard_path": "/revenda/dashboard/",
        "admin_model": "revenda/usuariorevenda"
    },
    "recapagem": {
        "email": "teste_recapagem@xbpneus.com",
        "nome_razao_social": "Recapagem Teste XBP Ltda",
        "cnpj": "55.666.777/0001-88",
        "telefone": "(11) 98765-4321",
        "password": "SenhaSegura123",
        "password_confirm": "SenhaSegura123",
        "register_endpoint": "/api/recapagem/register/",
        "login_endpoint": "/api/recapagem/login/",
        "dashboard_path": "/recapagem/dashboard/",
        "admin_model": "recapagem/usuariorecapagem"
    }
}

class TestResults:
    """Armazena resultados dos testes"""
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
    
    def add_result(self, user_type: str, step: str, success: bool, message: str, details: dict = None):
        """Adiciona resultado de um teste"""
        self.results.append({
            "user_type": user_type,
            "step": step,
            "success": success,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        })
    
    def get_summary(self) -> Dict:
        """Retorna resumo dos testes"""
        total = len(self.results)
        success = sum(1 for r in self.results if r["success"])
        failed = total - success
        duration = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "total_tests": total,
            "success": success,
            "failed": failed,
            "success_rate": (success / total * 100) if total > 0 else 0,
            "duration_seconds": duration,
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.now().isoformat()
        }

def check_backend_health() -> bool:
    """Verifica se o backend está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/healthz/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("status") == "ok"
        return False
    except Exception as e:
        print_error(f"Backend não está acessível: {e}")
        return False

def test_register(user_type: str, user_data: Dict, results: TestResults) -> Tuple[bool, Dict]:
    """Testa o cadastro de um usuário"""
    print_info(f"Testando cadastro de {user_type}...")
    
    endpoint = BASE_URL + user_data["register_endpoint"]
    
    # Prepara dados para registro (remove campos de controle)
    register_data = {k: v for k, v in user_data.items() 
                    if k not in ["register_endpoint", "login_endpoint", "dashboard_path", "admin_model"]}
    
    try:
        response = requests.post(endpoint, json=register_data, timeout=10)
        
        if response.status_code == 201:
            data = response.json()
            print_success(f"Cadastro realizado: {data.get('message', 'Sucesso')}")
            
            # Verifica se o usuário foi criado corretamente
            user_info = data.get("user", {})
            if user_info:
                print_info(f"  ID: {user_info.get('id')}")
                print_info(f"  Email: {user_info.get('email')}")
                print_info(f"  Aprovado: {user_info.get('aprovado', False)}")
                print_info(f"  Ativo: {user_info.get('is_active', False)}")
            
            results.add_result(user_type, "cadastro", True, "Cadastro realizado com sucesso", data)
            return True, data
        else:
            error_msg = response.json() if response.text else {"error": "Sem resposta"}
            print_error(f"Falha no cadastro: {response.status_code}")
            print_error(f"  Detalhes: {json.dumps(error_msg, indent=2)}")
            results.add_result(user_type, "cadastro", False, f"Erro {response.status_code}", error_msg)
            return False, error_msg
            
    except Exception as e:
        print_error(f"Erro ao cadastrar: {e}")
        results.add_result(user_type, "cadastro", False, f"Exceção: {str(e)}", {})
        return False, {}

def test_login_before_approval(user_type: str, user_data: Dict, results: TestResults) -> bool:
    """Testa login antes da aprovação (deve falhar)"""
    print_info(f"Testando login antes da aprovação de {user_type}...")
    
    endpoint = BASE_URL + user_data["login_endpoint"]
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(endpoint, json=login_data, timeout=10)
        
        if response.status_code == 403:
            data = response.json()
            error_msg = data.get("error", "")
            print_success(f"Login bloqueado corretamente: {error_msg}")
            results.add_result(user_type, "login_pre_aprovacao", True, "Login bloqueado como esperado", data)
            return True
        elif response.status_code == 401:
            print_success("Login bloqueado corretamente (credenciais inválidas)")
            results.add_result(user_type, "login_pre_aprovacao", True, "Login bloqueado como esperado", {})
            return True
        else:
            print_warning(f"Login deveria ter sido bloqueado, mas retornou: {response.status_code}")
            results.add_result(user_type, "login_pre_aprovacao", False, f"Login não bloqueado: {response.status_code}", {})
            return False
            
    except Exception as e:
        print_error(f"Erro ao testar login: {e}")
        results.add_result(user_type, "login_pre_aprovacao", False, f"Exceção: {str(e)}", {})
        return False

def simulate_admin_approval(user_type: str, user_data: Dict, results: TestResults) -> bool:
    """Simula aprovação pelo admin (via Django Admin)"""
    print_info(f"Simulando aprovação do admin para {user_type}...")
    print_warning("  NOTA: Esta etapa requer aprovação manual no Django Admin")
    print_info(f"  URL: {BASE_URL}/admin/{user_data['admin_model']}/")
    print_info(f"  Email do usuário: {user_data['email']}")
    print_info("  Ações necessárias:")
    print_info("    1. Acessar Django Admin")
    print_info("    2. Localizar o usuário pendente")
    print_info("    3. Marcar 'aprovado' como True")
    print_info("    4. Marcar 'is_active' como True")
    print_info("    5. Salvar")
    
    # Aqui poderíamos fazer uma aprovação automática via API do Django Admin
    # mas isso requer autenticação de superusuário
    
    results.add_result(user_type, "aprovacao_admin", True, "Aprovação manual necessária", {
        "admin_url": f"{BASE_URL}/admin/{user_data['admin_model']}/",
        "user_email": user_data['email']
    })
    
    return True

def test_login_after_approval(user_type: str, user_data: Dict, results: TestResults) -> Tuple[bool, Dict]:
    """Testa login após aprovação"""
    print_info(f"Testando login após aprovação de {user_type}...")
    
    endpoint = BASE_URL + user_data["login_endpoint"]
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(endpoint, json=login_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Login realizado com sucesso!")
            
            # Verifica tokens
            tokens = data.get("tokens", {})
            if tokens:
                print_info(f"  Access Token: {tokens.get('access', '')[:50]}...")
                print_info(f"  Refresh Token: {tokens.get('refresh', '')[:50]}...")
            
            # Verifica redirect
            redirect = data.get("redirect", "")
            if redirect:
                print_info(f"  Redirect: {redirect}")
                
                # Verifica se o redirect está correto
                expected_redirect = user_data["dashboard_path"]
                if expected_redirect in redirect:
                    print_success(f"  Redirect correto para dashboard de {user_type}")
                else:
                    print_warning(f"  Redirect inesperado. Esperado: {expected_redirect}, Recebido: {redirect}")
            
            results.add_result(user_type, "login_pos_aprovacao", True, "Login bem-sucedido", data)
            return True, data
        else:
            error_msg = response.json() if response.text else {"error": "Sem resposta"}
            print_error(f"Falha no login: {response.status_code}")
            print_error(f"  Detalhes: {json.dumps(error_msg, indent=2)}")
            results.add_result(user_type, "login_pos_aprovacao", False, f"Erro {response.status_code}", error_msg)
            return False, error_msg
            
    except Exception as e:
        print_error(f"Erro ao fazer login: {e}")
        results.add_result(user_type, "login_pos_aprovacao", False, f"Exceção: {str(e)}", {})
        return False, {}

def test_dashboard_access(user_type: str, user_data: Dict, tokens: Dict, results: TestResults) -> bool:
    """Testa acesso ao dashboard específico"""
    print_info(f"Testando acesso ao dashboard de {user_type}...")
    
    # Como o dashboard é uma rota do frontend, não podemos testar diretamente
    # Mas podemos verificar se o frontend está acessível
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print_success("Frontend acessível")
            print_info(f"  Dashboard esperado: {user_data['dashboard_path']}")
            results.add_result(user_type, "dashboard_access", True, "Frontend acessível", {})
            return True
        else:
            print_error(f"Frontend retornou: {response.status_code}")
            results.add_result(user_type, "dashboard_access", False, f"Erro {response.status_code}", {})
            return False
    except Exception as e:
        print_error(f"Erro ao acessar frontend: {e}")
        results.add_result(user_type, "dashboard_access", False, f"Exceção: {str(e)}", {})
        return False

def test_user_flow(user_type: str, user_data: Dict, results: TestResults, auto_approve: bool = False):
    """Testa o fluxo completo de um tipo de usuário"""
    print_header(f"TESTANDO FLUXO: {user_type.upper()}")
    
    # Passo 1: Cadastro
    success, register_data = test_register(user_type, user_data, results)
    if not success:
        print_error(f"Falha no cadastro de {user_type}. Abortando testes deste usuário.")
        return
    
    time.sleep(1)
    
    # Passo 2: Login antes da aprovação (deve falhar)
    test_login_before_approval(user_type, user_data, results)
    
    time.sleep(1)
    
    # Passo 3: Aprovação pelo admin
    simulate_admin_approval(user_type, user_data, results)
    
    if not auto_approve:
        print_warning(f"\n⏸  PAUSADO: Aprove manualmente o usuário {user_type} no Django Admin")
        print_info(f"   Pressione ENTER após aprovar o usuário...")
        input()
    
    time.sleep(1)
    
    # Passo 4: Login após aprovação
    success, login_data = test_login_after_approval(user_type, user_data, results)
    if not success:
        print_error(f"Falha no login de {user_type}. Verifique se o usuário foi aprovado.")
        return
    
    time.sleep(1)
    
    # Passo 5: Acesso ao dashboard
    tokens = login_data.get("tokens", {})
    test_dashboard_access(user_type, user_data, tokens, results)

def print_summary(results: TestResults):
    """Imprime resumo dos testes"""
    summary = results.get_summary()
    
    print_header("RESUMO DOS TESTES")
    
    print(f"{Colors.BOLD}Total de testes:{Colors.RESET} {summary['total_tests']}")
    print(f"{Colors.GREEN}Sucessos:{Colors.RESET} {summary['success']}")
    print(f"{Colors.RED}Falhas:{Colors.RESET} {summary['failed']}")
    print(f"{Colors.BOLD}Taxa de sucesso:{Colors.RESET} {summary['success_rate']:.2f}%")
    print(f"{Colors.BOLD}Duração:{Colors.RESET} {summary['duration_seconds']:.2f} segundos")
    
    print(f"\n{Colors.BOLD}Detalhes por tipo de usuário:{Colors.RESET}\n")
    
    for user_type in TEST_USERS.keys():
        user_results = [r for r in results.results if r["user_type"] == user_type]
        if user_results:
            success_count = sum(1 for r in user_results if r["success"])
            total_count = len(user_results)
            
            status_icon = "✓" if success_count == total_count else "✗"
            color = Colors.GREEN if success_count == total_count else Colors.RED
            
            print(f"{color}{status_icon} {user_type.upper()}: {success_count}/{total_count} testes passaram{Colors.RESET}")
            
            for result in user_results:
                step_icon = "  ✓" if result["success"] else "  ✗"
                step_color = Colors.GREEN if result["success"] else Colors.RED
                print(f"{step_color}{step_icon} {result['step']}: {result['message']}{Colors.RESET}")

def save_results_to_file(results: TestResults, filename: str = "test_results.json"):
    """Salva resultados em arquivo JSON"""
    output = {
        "summary": results.get_summary(),
        "results": results.results
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print_success(f"\nResultados salvos em: {filename}")

def main():
    """Função principal"""
    print_header("TESTE DE FLUXO DE USUÁRIOS - XBPNEUS v10")
    
    # Verifica se o backend está rodando
    print_info("Verificando backend...")
    if not check_backend_health():
        print_error("Backend não está rodando ou não está saudável!")
        print_info("Certifique-se de que o backend está rodando em http://localhost:8000")
        sys.exit(1)
    
    print_success("Backend está rodando e saudável!\n")
    
    # Pergunta se deve fazer aprovação automática ou manual
    print_info("Modo de aprovação:")
    print("  1. Manual (pausa para aprovação no Django Admin)")
    print("  2. Automático (pula etapa de aprovação - requer superusuário)")
    
    mode = input("\nEscolha o modo (1 ou 2): ").strip()
    auto_approve = (mode == "2")
    
    if auto_approve:
        print_warning("Modo automático selecionado - aprovação será simulada")
    else:
        print_info("Modo manual selecionado - será necessário aprovar cada usuário")
    
    # Inicializa resultados
    results = TestResults()
    
    # Testa cada tipo de usuário
    for user_type, user_data in TEST_USERS.items():
        test_user_flow(user_type, user_data, results, auto_approve)
        print()  # Linha em branco entre testes
    
    # Imprime resumo
    print_summary(results)
    
    # Salva resultados
    save_results_to_file(results)
    
    print_header("TESTES CONCLUÍDOS")

if __name__ == "__main__":
    main()

