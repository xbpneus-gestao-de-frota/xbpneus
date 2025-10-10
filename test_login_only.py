#!/usr/bin/env python3
"""
Script de Teste - Login Após Aprovação
Sistema XBPNEUS v10

Testa apenas o login dos usuários já aprovados
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Cores
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

TEST_LOGINS = {
    "motorista": {
        "email": "teste_motorista@xbpneus.com",
        "password": "SenhaSegura123",
        "endpoint": "/api/motorista/login/"
    },
    "borracharia": {
        "email": "teste_borracharia@xbpneus.com",
        "password": "SenhaSegura123",
        "endpoint": "/api/borracharia/login/"
    },
    "revenda": {
        "email": "teste_revenda@xbpneus.com",
        "password": "SenhaSegura123",
        "endpoint": "/api/revenda/login/"
    },
    "recapagem": {
        "email": "teste_recapagem@xbpneus.com",
        "password": "SenhaSegura123",
        "endpoint": "/api/recapagem/login/"
    }
}

def test_login(user_type, data):
    """Testa login de um usuário"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}Testando login: {user_type.upper()}{Colors.RESET}")
    
    endpoint = BASE_URL + data["endpoint"]
    login_data = {
        "email": data["email"],
        "password": data["password"]
    }
    
    try:
        response = requests.post(endpoint, json=login_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"{Colors.GREEN}✓ Login realizado com sucesso!{Colors.RESET}")
            print(f"  Email: {data['email']}")
            
            # Tokens
            tokens = result.get("tokens", {})
            if tokens:
                print(f"  Access Token: {tokens.get('access', '')[:50]}...")
                print(f"  Refresh Token: {tokens.get('refresh', '')[:50]}...")
            
            # Redirect
            redirect = result.get("redirect", "")
            if redirect:
                print(f"  Redirect: {redirect}")
            
            # User data
            user = result.get("user", {})
            if user:
                print(f"  Nome: {user.get('nome_razao_social') or user.get('nome_completo', 'N/A')}")
                print(f"  Aprovado: {user.get('aprovado', False)}")
                print(f"  Ativo: {user.get('is_active', False)}")
            
            return True
        else:
            error = response.json() if response.text else {}
            print(f"{Colors.RED}✗ Falha no login: {response.status_code}{Colors.RESET}")
            print(f"  Erro: {json.dumps(error, indent=2)}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}✗ Erro: {e}{Colors.RESET}")
        return False

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'TESTE DE LOGIN - USUÁRIOS APROVADOS'.center(80)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")
    
    results = {}
    for user_type, data in TEST_LOGINS.items():
        results[user_type] = test_login(user_type, data)
    
    # Resumo
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'RESUMO'.center(80)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")
    
    success = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Total: {total}")
    print(f"{Colors.GREEN}Sucessos: {success}{Colors.RESET}")
    print(f"{Colors.RED}Falhas: {total - success}{Colors.RESET}")
    print(f"Taxa de sucesso: {(success/total*100):.1f}%\n")
    
    for user_type, success in results.items():
        icon = "✓" if success else "✗"
        color = Colors.GREEN if success else Colors.RED
        print(f"{color}{icon} {user_type.upper()}{Colors.RESET}")

if __name__ == "__main__":
    main()

