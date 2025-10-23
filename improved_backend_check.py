#!/usr/bin/env python3
"""
Script Aprimorado de Verificação de Funcionalidades de Backend
Testa endpoints com métodos HTTP corretos e autenticação
"""

import requests
import json
import sys
from requests.auth import HTTPBasicAuth

# Configuração
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Token de autenticação (será obtido após login)
auth_token = None

def print_header(text):
    """Imprime um cabeçalho formatado"""
    print(f"\n{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    """Imprime mensagem de sucesso"""
    print(f"{GREEN}[OK]{RESET} {text}")

def print_error(text):
    """Imprime mensagem de erro"""
    print(f"{RED}[ERRO]{RESET} {text}")

def print_warning(text):
    """Imprime mensagem de aviso"""
    print(f"{YELLOW}[AVISO]{RESET} {text}")

def print_info(text):
    """Imprime mensagem de informação"""
    print(f"{BLUE}[INFO]{RESET} {text}")

def test_endpoint(method, url, expected_status=None, data=None, headers=None, description=""):
    """
    Testa um endpoint específico
    
    Args:
        method: GET, POST, PUT, DELETE, etc.
        url: URL completa do endpoint
        expected_status: Status esperado (opcional)
        data: Dados para POST/PUT (opcional)
        headers: Headers customizados (opcional)
        description: Descrição do teste
    """
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=5)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=5)
        else:
            print_warning(f"Método HTTP não suportado: {method}")
            return False
        
        status = response.status_code
        
        # Determinar se foi sucesso
        if expected_status:
            success = status == expected_status
        else:
            success = 200 <= status < 300
        
        if success:
            print_success(f"{method:6} {url:50} - Status: {status}")
            if description:
                print(f"        {description}")
            return True
        else:
            print_error(f"{method:6} {url:50} - Status: {status}")
            if description:
                print(f"        {description}")
            # Tentar exibir mensagem de erro da resposta
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    if 'detail' in error_data:
                        print(f"        Detalhe: {error_data['detail']}")
                    elif 'error' in error_data:
                        print(f"        Erro: {error_data['error']}")
            except:
                pass
            return False
    except requests.exceptions.Timeout:
        print_error(f"{method:6} {url:50} - Timeout")
        return False
    except requests.exceptions.ConnectionError:
        print_error(f"{method:6} {url:50} - Erro de conexão")
        return False
    except Exception as e:
        print_error(f"{method:6} {url:50} - Exceção: {str(e)}")
        return False

def test_authentication():
    """Testa endpoints de autenticação"""
    global auth_token
    
    print_header("Testes de Autenticação")
    
    # Teste de registro (se disponível)
    register_data = {
        "username": "testuser_automated",
        "email": "testuser@example.com",
        "password": "TestPassword123!",
        "password_confirm": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User",
        "user_type": "transportador"
    }
    
    test_endpoint(
        "POST",
        f"{API_BASE}/users/register_full/",
        data=register_data,
        description="Registro de novo usuário"
    )
    
    # Teste de obtenção de token
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
                auth_token = data['access']
                print_success(f"POST {API_BASE}/token/ - Status: 200")
                print(f"        Token obtido com sucesso")
            else:
                print_error(f"POST {API_BASE}/token/ - Token não encontrado na resposta")
        else:
            print_error(f"POST {API_BASE}/token/ - Status: {response.status_code}")
    except Exception as e:
        print_error(f"POST {API_BASE}/token/ - Exceção: {str(e)}")
    
    # Teste de refresh de token (se token foi obtido)
    if auth_token:
        refresh_data = {"access": auth_token}
        test_endpoint(
            "POST",
            f"{API_BASE}/token/refresh/",
            data=refresh_data,
            description="Renovação de token"
        )
        
        # Teste de verificação de token
        verify_data = {"token": auth_token}
        test_endpoint(
            "POST",
            f"{API_BASE}/token/verify/",
            data=verify_data,
            description="Verificação de token"
        )
    
    # Teste de obtenção de dados do usuário autenticado
    if auth_token:
        headers = {"Authorization": f"Bearer {auth_token}"}
        test_endpoint(
            "GET",
            f"{API_BASE}/auth/me/",
            headers=headers,
            description="Obtenção de dados do usuário autenticado"
        )

def test_transportador_endpoints():
    """Testa endpoints do módulo transportador"""
    print_header("Testes de Endpoints do Módulo Transportador")
    
    endpoints = [
        ("GET", f"{API_BASE}/transportador/motorista/", "Listagem de motoristas"),
        ("GET", f"{API_BASE}/transportador/frota/", "Listagem de frotas"),
        ("GET", f"{API_BASE}/transportador/pneus/", "Listagem de pneus"),
        ("GET", f"{API_BASE}/transportador/manutencao/", "Listagem de manutenções"),
        ("GET", f"{API_BASE}/transportador/estoque/", "Listagem de estoque"),
        ("GET", f"{API_BASE}/transportador/loja/", "Listagem de loja"),
        ("GET", f"{API_BASE}/transportador/custos/", "Listagem de custos"),
        ("GET", f"{API_BASE}/transportador/combustivel/", "Listagem de combustível"),
        ("GET", f"{API_BASE}/transportador/multas/", "Listagem de multas"),
        ("GET", f"{API_BASE}/transportador/documentos/", "Listagem de documentos"),
        ("GET", f"{API_BASE}/transportador/viagens/", "Listagem de viagens"),
        ("GET", f"{API_BASE}/transportador/clientes/", "Listagem de clientes"),
        ("GET", f"{API_BASE}/transportador/fornecedores/", "Listagem de fornecedores"),
        ("GET", f"{API_BASE}/transportador/seguros/", "Listagem de seguros"),
        ("GET", f"{API_BASE}/transportador/contratos/", "Listagem de contratos"),
        ("GET", f"{API_BASE}/transportador/faturamento/", "Listagem de faturamento"),
        ("GET", f"{API_BASE}/transportador/pagamentos/", "Listagem de pagamentos"),
        ("GET", f"{API_BASE}/transportador/telemetria/", "Listagem de telemetria"),
        ("GET", f"{API_BASE}/transportador/rastreamento/", "Listagem de rastreamento"),
        ("GET", f"{API_BASE}/transportador/rotas/", "Listagem de rotas"),
        ("GET", f"{API_BASE}/transportador/entregas/", "Listagem de entregas"),
        ("GET", f"{API_BASE}/transportador/dashboards/", "Listagem de dashboards"),
        ("GET", f"{API_BASE}/transportador/notificacoes/", "Listagem de notificações"),
        ("GET", f"{API_BASE}/transportador/almoxarifado/", "Listagem de almoxarifado"),
        ("GET", f"{API_BASE}/transportador/relatorios/", "Listagem de relatórios"),
        ("GET", f"{API_BASE}/transportador/cargas/", "Listagem de cargas"),
        ("GET", f"{API_BASE}/transportador/pecas/", "Listagem de peças"),
        ("GET", f"{API_BASE}/transportador/ferramentas/", "Listagem de ferramentas"),
        ("GET", f"{API_BASE}/transportador/epis/", "Listagem de EPIs"),
        ("GET", f"{API_BASE}/transportador/treinamentos/", "Listagem de treinamentos"),
        ("GET", f"{API_BASE}/transportador/compliance/", "Listagem de compliance"),
        ("GET", f"{API_BASE}/transportador/alertas/", "Listagem de alertas"),
        ("GET", f"{API_BASE}/transportador/integracoes/", "Listagem de integrações"),
        ("GET", f"{API_BASE}/transportador/configuracoes/", "Listagem de configurações"),
        ("GET", f"{API_BASE}/transportador/empresas/", "Listagem de empresas"),
        ("GET", f"{API_BASE}/transportador/financeiro/", "Listagem de financeiro"),
        ("GET", f"{API_BASE}/transportador/relatorios_transportador/", "Listagem de relatórios transportador"),
        ("GET", f"{API_BASE}/transportador/tr/", "Listagem de TR"),
        ("GET", f"{API_BASE}/transportador/implemento/", "Listagem de implementos"),
        ("GET", f"{API_BASE}/transportador/analise_pneus/", "Listagem de análise de pneus"),
        ("GET", f"{API_BASE}/transportador/garantias/", "Listagem de garantias"),
        ("GET", f"{API_BASE}/transportador/auditoria/", "Listagem de auditoria"),
        ("GET", f"{API_BASE}/transportador/notas_fiscais/", "Listagem de notas fiscais"),
        ("GET", f"{API_BASE}/transportador/ia/", "Listagem de IA"),
    ]
    
    success_count = 0
    for method, url, description in endpoints:
        if test_endpoint(method, url, description=description):
            success_count += 1
    
    print(f"\n{BLUE}Resumo: {success_count}/{len(endpoints)} endpoints funcionais{RESET}")

def test_missing_endpoints():
    """Testa endpoints que faltam ou retornam 404"""
    print_header("Testes de Endpoints Ausentes/Com Problemas")
    
    endpoints = [
        ("GET", f"{API_BASE}/approve/", "Aprovação de usuários"),
        ("GET", f"{API_BASE}/motorista/", "Módulo motorista (raiz)"),
        ("GET", f"{API_BASE}/borracharia/", "Módulo borracharia (raiz)"),
        ("GET", f"{API_BASE}/revenda/", "Módulo revenda (raiz)"),
        ("GET", f"{API_BASE}/recapagem/", "Módulo recapagem (raiz)"),
        ("GET", f"{API_BASE}/reports/", "Relatórios (raiz)"),
        ("GET", f"{API_BASE}/jobs/", "Jobs (raiz)"),
        ("GET", f"{API_BASE}/schema/swagger/", "Documentação Swagger"),
    ]
    
    for method, url, description in endpoints:
        test_endpoint(method, url, description=description)

def test_documentation_endpoints():
    """Testa endpoints de documentação"""
    print_header("Testes de Endpoints de Documentação")
    
    endpoints = [
        ("GET", f"{API_BASE}/schema/", "Schema OpenAPI"),
        ("GET", f"{API_BASE}/docs/", "Documentação DRF"),
    ]
    
    for method, url, description in endpoints:
        test_endpoint(method, url, description=description)

def main():
    """Função principal"""
    print(f"\n{BLUE}{'='*60}")
    print("VERIFICAÇÃO APRIMORADA DE FUNCIONALIDADES DE BACKEND")
    print("Sistema XBPneus")
    print(f"{'='*60}{RESET}\n")
    
    # Verificar conexão com o servidor
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print_success(f"Conexão com servidor em {BASE_URL} estabelecida")
    except:
        print_error(f"Não foi possível conectar ao servidor em {BASE_URL}")
        sys.exit(1)
    
    # Executar testes
    test_documentation_endpoints()
    test_authentication()
    test_transportador_endpoints()
    test_missing_endpoints()
    
    print(f"\n{BLUE}{'='*60}")
    print("FIM DA VERIFICAÇÃO")
    print(f"{'='*60}{RESET}\n")

if __name__ == "__main__":
    main()

