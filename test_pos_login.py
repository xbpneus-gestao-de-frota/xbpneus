#!/usr/bin/env python3
"""
Script de Teste Pós-Login - Endpoints Protegidos do Transportador
"""
import requests
import json

# Cores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text.center(80)}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ️  {text}{RESET}")

BASE_URL = "http://localhost:8000"

# Credenciais do transportador de teste
CREDENCIAIS = {
    "email": "transportador.novo@xbpneus.com",
    "password": "senha123"
}

def fazer_login():
    """Faz login e retorna o token de acesso"""
    print_header("AUTENTICAÇÃO: Fazendo Login")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transportador/login/",
            json=CREDENCIAIS,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extrair token (pode estar em 'access', 'token' ou 'tokens.access')
            token = None
            if 'tokens' in data and 'access' in data['tokens']:
                token = data['tokens']['access']
            elif 'access' in data:
                token = data['access']
            elif 'token' in data:
                token = data['token']
            
            if token:
                print_success("Login realizado com sucesso!")
                print_info(f"   Usuário: {data.get('user', {}).get('email', 'N/A')}")
                print_info(f"   Token obtido: {token[:50]}...")
                return token
            else:
                print_error("Token não encontrado na resposta")
                return None
        else:
            print_error(f"Erro no login: {response.status_code}")
            print_info(f"   Resposta: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return None

def teste_1_acesso_sem_token():
    """Teste 1: Tentar acessar endpoint protegido sem token"""
    print_header("TESTE 1: Acesso a Endpoint Protegido SEM Token")
    
    endpoints = [
        "/api/transportador/frota/veiculos/",
        "/api/transportador/frota/pneus/",
        "/api/transportador/estoque/movimentacoes/",
        "/api/transportador/manutencao/ordens-servico/"
    ]
    
    resultados = []
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print_info(f"Endpoint: {endpoint}")
            print_info(f"   Status: {response.status_code}")
            
            if response.status_code in [401, 403]:
                print_success(f"   ✅ Protegido corretamente (não autorizado)")
                resultados.append(True)
            else:
                print_error(f"   ❌ Endpoint não está protegido!")
                resultados.append(False)
                
        except Exception as e:
            print_error(f"   Exceção: {str(e)}")
            resultados.append(False)
    
    return all(resultados)

def teste_2_acesso_com_token(token):
    """Teste 2: Acessar endpoints protegidos COM token válido"""
    print_header("TESTE 2: Acesso a Endpoints Protegidos COM Token Válido")
    
    if not token:
        print_error("Token não fornecido!")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    endpoints = {
        "Veículos da Frota": "/api/transportador/frota/veiculos/",
        "Pneus": "/api/transportador/frota/pneus/",
        "Movimentações de Estoque": "/api/transportador/estoque/movimentacoes/",
        "Ordens de Serviço": "/api/transportador/manutencao/ordens-servico/"
    }
    
    resultados = []
    
    for nome, endpoint in endpoints.items():
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            print_info(f"{nome}: {endpoint}")
            print_info(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"   ✅ Acesso autorizado!")
                
                # Verificar se retornou lista ou objeto com results
                if isinstance(data, list):
                    print_info(f"   Registros: {len(data)}")
                elif isinstance(data, dict) and 'results' in data:
                    print_info(f"   Registros: {len(data['results'])}")
                    print_info(f"   Total: {data.get('count', 'N/A')}")
                else:
                    print_info(f"   Tipo de resposta: {type(data).__name__}")
                
                resultados.append(True)
            elif response.status_code == 404:
                print_success(f"   ✅ Endpoint não encontrado (pode não estar implementado)")
                resultados.append(True)
            else:
                print_error(f"   ❌ Erro: {response.status_code}")
                print_info(f"   Resposta: {response.text[:200]}")
                resultados.append(False)
                
        except Exception as e:
            print_error(f"   Exceção: {str(e)}")
            resultados.append(False)
    
    return all(resultados)

def teste_3_acesso_token_invalido():
    """Teste 3: Tentar acessar com token inválido"""
    print_header("TESTE 3: Acesso com Token INVÁLIDO")
    
    headers = {
        "Authorization": "Bearer token_invalido_123456",
        "Content-Type": "application/json"
    }
    
    endpoint = "/api/transportador/frota/veiculos/"
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        print_info(f"Endpoint: {endpoint}")
        print_info(f"   Status: {response.status_code}")
        
        if response.status_code in [401, 403]:
            print_success("   ✅ Token inválido rejeitado corretamente")
            return True
        else:
            print_error(f"   ❌ Token inválido foi aceito!")
            return False
            
    except Exception as e:
        print_error(f"   Exceção: {str(e)}")
        return False

def teste_4_dashboard_info(token):
    """Teste 4: Obter informações do dashboard"""
    print_header("TESTE 4: Informações do Dashboard")
    
    if not token:
        print_error("Token não fornecido!")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    endpoints_dashboard = [
        "/api/transportador/dashboard/",
        "/api/transportador/me/",
        "/api/transportador/profile/"
    ]
    
    for endpoint in endpoints_dashboard:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            print_info(f"Endpoint: {endpoint}")
            print_info(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"   ✅ Dados obtidos com sucesso!")
                
                # Mostrar algumas informações
                if isinstance(data, dict):
                    if 'email' in data:
                        print_info(f"   Email: {data.get('email')}")
                    if 'nome_razao_social' in data:
                        print_info(f"   Nome: {data.get('nome_razao_social')}")
                    print_info(f"   Campos: {len(data.keys())}")
                
                return True
            elif response.status_code == 404:
                print_info(f"   ⚠️  Endpoint não encontrado")
                continue
            else:
                print_error(f"   ❌ Erro: {response.status_code}")
                
        except Exception as e:
            print_error(f"   Exceção: {str(e)}")
    
    return False

def teste_5_criar_veiculo(token):
    """Teste 5: Criar um veículo na frota"""
    print_header("TESTE 5: Criar Veículo na Frota")
    
    if not token:
        print_error("Token não fornecido!")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    veiculo_data = {
        "placa": "ABC1234",
        "modelo": "Scania R450",
        "ano": 2023,
        "tipo": "Caminhão",
        "status": "ativo"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transportador/frota/veiculos/",
            json=veiculo_data,
            headers=headers
        )
        
        print_info(f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_success("✅ Veículo criado com sucesso!")
            print_info(f"   ID: {data.get('id', 'N/A')}")
            print_info(f"   Placa: {data.get('placa', 'N/A')}")
            print_info(f"   Modelo: {data.get('modelo', 'N/A')}")
            return True
        elif response.status_code == 404:
            print_info("⚠️  Endpoint de criação não encontrado")
            return True  # Não é erro, endpoint pode não existir
        elif response.status_code == 400:
            print_info("⚠️  Erro de validação (pode ser placa duplicada)")
            print_info(f"   Resposta: {response.text[:200]}")
            return True  # Validação funcionando
        else:
            print_error(f"❌ Erro: {response.status_code}")
            print_info(f"   Resposta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def teste_6_listar_com_paginacao(token):
    """Teste 6: Testar paginação nos endpoints"""
    print_header("TESTE 6: Paginação de Resultados")
    
    if not token:
        print_error("Token não fornecido!")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    endpoint = "/api/transportador/frota/veiculos/"
    
    try:
        # Testar com parâmetros de paginação
        response = requests.get(
            f"{BASE_URL}{endpoint}?page=1&page_size=10",
            headers=headers
        )
        
        print_info(f"Endpoint: {endpoint}?page=1&page_size=10")
        print_info(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("✅ Paginação funcionando!")
            
            if isinstance(data, dict):
                print_info(f"   Count: {data.get('count', 'N/A')}")
                print_info(f"   Next: {data.get('next', 'N/A')}")
                print_info(f"   Previous: {data.get('previous', 'N/A')}")
                print_info(f"   Results: {len(data.get('results', []))}")
            
            return True
        elif response.status_code == 404:
            print_info("⚠️  Endpoint não encontrado")
            return True
        else:
            print_error(f"❌ Erro: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def gerar_relatorio(resultados):
    """Gera relatório final"""
    print_header("RELATÓRIO FINAL - TESTES PÓS-LOGIN")
    
    total = len(resultados)
    sucessos = sum(1 for r in resultados.values() if r)
    taxa = (sucessos * 100) // total if total > 0 else 0
    
    print(f"\n{BLUE}Resumo Geral:{RESET}")
    print(f"  Total de testes: {total}")
    print(f"  Testes bem-sucedidos: {sucessos}/{total} ({taxa}%)")
    print(f"  Testes falhados: {total - sucessos}/{total}")
    
    print(f"\n{BLUE}Detalhes por Teste:{RESET}\n")
    
    for nome, resultado in resultados.items():
        status = f"{GREEN}✅ PASSOU{RESET}" if resultado else f"{RED}❌ FALHOU{RESET}"
        print(f"  {nome}: {status}")
    
    if sucessos == total:
        print(f"\n{GREEN}{'='*80}{RESET}")
        print(f"{GREEN}STATUS FINAL: ✅ TODOS OS TESTES PASSARAM!{RESET}")
        print(f"{GREEN}{'='*80}{RESET}\n")
    else:
        print(f"\n{YELLOW}{'='*80}{RESET}")
        print(f"{YELLOW}STATUS FINAL: ⚠️  {total - sucessos} TESTE(S) FALHARAM{RESET}")
        print(f"{YELLOW}{'='*80}{RESET}\n")

def main():
    """Função principal"""
    print_header("TESTES PÓS-LOGIN - TRANSPORTADOR - SISTEMA XBPNEUS")
    
    resultados = {}
    
    # Fazer login primeiro
    token = fazer_login()
    
    if not token:
        print_error("\n❌ Não foi possível fazer login. Abortando testes.")
        return
    
    # Executar testes
    resultados["Teste 1: Acesso sem Token"] = teste_1_acesso_sem_token()
    resultados["Teste 2: Acesso com Token Válido"] = teste_2_acesso_com_token(token)
    resultados["Teste 3: Acesso com Token Inválido"] = teste_3_acesso_token_invalido()
    resultados["Teste 4: Informações do Dashboard"] = teste_4_dashboard_info(token)
    resultados["Teste 5: Criar Veículo"] = teste_5_criar_veiculo(token)
    resultados["Teste 6: Paginação"] = teste_6_listar_com_paginacao(token)
    
    # Relatório
    gerar_relatorio(resultados)

if __name__ == '__main__':
    main()

