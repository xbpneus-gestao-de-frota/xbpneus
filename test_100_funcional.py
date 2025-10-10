#!/usr/bin/env python3
"""
Teste Final Completo - Sistema 100% Funcional
Sistema XBPneus - Transportador
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Cores
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text.center(80)}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ️  {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def test_login():
    """Teste de login"""
    print_header("TESTE 1: Login do Transportador")
    
    response = requests.post(
        f"{BASE_URL}/api/transportador/login/",
        json={
            "email": "transportador.novo@xbpneus.com",
            "password": "senha123"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        # Token pode estar em 'access' ou 'tokens.access'
        token = data.get('access') or data.get('tokens', {}).get('access')
        print_success(f"Login realizado com sucesso!")
        if token:
            print_info(f"   Token: {token[:50]}...")
        return token, True
    else:
        print_error(f"Falha no login: {response.status_code}")
        return None, False

def test_dashboard(token):
    """Teste de dashboard"""
    print_header("TESTE 2: Dashboard do Transportador")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/transportador/dashboard/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Dashboard acessível!")
        print_info(f"   Total de veículos: {data.get('frota', {}).get('total_veiculos', 0)}")
        print_info(f"   Veículos ativos: {data.get('frota', {}).get('veiculos_ativos', 0)}")
        print_info(f"   OS abertas: {data.get('manutencao', {}).get('os_abertas', 0)}")
        return True
    else:
        print_error(f"Erro ao acessar dashboard: {response.status_code}")
        return False

def test_me(token):
    """Teste de perfil /me/"""
    print_header("TESTE 3: Endpoint /me/")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/transportador/me/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Endpoint /me/ funcionando!")
        print_info(f"   Email: {data.get('email')}")
        print_info(f"   Nome: {data.get('nome')}")
        print_info(f"   Tipo: {data.get('tipo')}")
        return True
    else:
        print_error(f"Erro ao acessar /me/: {response.status_code}")
        return False

def test_profile(token):
    """Teste de perfil /profile/"""
    print_header("TESTE 4: Endpoint /profile/")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/transportador/profile/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Endpoint /profile/ funcionando!")
        print_info(f"   Email: {data.get('email')}")
        print_info(f"   CNPJ: {data.get('cnpj')}")
        print_info(f"   Telefone: {data.get('telefone')}")
        return True
    else:
        print_error(f"Erro ao acessar /profile/: {response.status_code}")
        return False

def test_veiculos(token):
    """Teste de listagem de veículos"""
    print_header("TESTE 5: Listagem de Veículos")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/transportador/frota/veiculos/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Listagem de veículos funcionando!")
        print_info(f"   Total: {data.get('count', 0)}")
        print_info(f"   Registros na página: {len(data.get('results', []))}")
        return True
    else:
        print_error(f"Erro ao listar veículos: {response.status_code}")
        return False

def test_ordens_servico(token):
    """Teste de ordens de serviço"""
    print_header("TESTE 6: Ordens de Serviço")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/transportador/manutencao/ordens-servico/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Endpoint de ordens de serviço funcionando!")
        print_info(f"   Total: {data.get('count', 0)}")
        return True
    else:
        print_error(f"Erro ao acessar ordens de serviço: {response.status_code}")
        return False

def test_estoque(token):
    """Teste de movimentações de estoque"""
    print_header("TESTE 7: Movimentações de Estoque")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/transportador/estoque/movimentacoes/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Endpoint de estoque funcionando!")
        print_info(f"   Total: {data.get('count', 0)}")
        return True
    else:
        print_error(f"Erro ao acessar estoque: {response.status_code}")
        return False

def test_pneus(token):
    """Teste de pneus"""
    print_header("TESTE 8: Listagem de Pneus")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/transportador/pneus/pneus/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Endpoint de pneus funcionando!")
        print_info(f"   Total: {data.get('count', 0)}")
        return True
    elif response.status_code == 404:
        print_error("Endpoint de pneus não encontrado (404)")
        return False
    else:
        print_error(f"Erro ao acessar pneus: {response.status_code}")
        return False

def test_security(token):
    """Teste de segurança"""
    print_header("TESTE 9: Segurança - Token Inválido")
    
    headers = {"Authorization": "Bearer token_invalido_123"}
    response = requests.get(f"{BASE_URL}/api/transportador/dashboard/", headers=headers)
    
    if response.status_code == 401:
        print_success("Token inválido rejeitado corretamente!")
        return True
    else:
        print_error(f"Falha na segurança: {response.status_code}")
        return False

def test_create_veiculo(token):
    """Teste de criação de veículo"""
    print_header("TESTE 10: Criar Veículo")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Gerar placa única
    import time
    placa = f"TST{int(time.time()) % 10000:04d}"
    
    response = requests.post(
        f"{BASE_URL}/api/transportador/frota/veiculos/",
        headers=headers,
        json={
            "placa": placa,
            "modelo": "Teste Automatizado",
            "tipo": "CAMINHAO",
            "status": "ATIVO"
        }
    )
    
    if response.status_code == 201:
        data = response.json()
        print_success("Veículo criado com sucesso!")
        print_info(f"   Placa: {data.get('placa')}")
        print_info(f"   Modelo: {data.get('modelo')}")
        return True
    else:
        print_error(f"Erro ao criar veículo: {response.status_code}")
        print_info(f"   Resposta: {response.text[:200]}")
        return False

def main():
    """Função principal"""
    print_header("TESTE COMPLETO - SISTEMA 100% FUNCIONAL")
    print_info("Sistema XBPneus - Módulo Transportador")
    print_info("Data: 10 de Outubro de 2025\n")
    
    resultados = []
    
    # Teste 1: Login
    token, success = test_login()
    resultados.append(("Login", success))
    
    if not token:
        print_error("\n❌ Não foi possível obter token. Abortando testes.")
        return
    
    # Teste 2: Dashboard
    resultados.append(("Dashboard", test_dashboard(token)))
    
    # Teste 3: /me/
    resultados.append(("/me/", test_me(token)))
    
    # Teste 4: /profile/
    resultados.append(("/profile/", test_profile(token)))
    
    # Teste 5: Veículos
    resultados.append(("Veículos", test_veiculos(token)))
    
    # Teste 6: Ordens de Serviço
    resultados.append(("Ordens de Serviço", test_ordens_servico(token)))
    
    # Teste 7: Estoque
    resultados.append(("Estoque", test_estoque(token)))
    
    # Teste 8: Pneus
    resultados.append(("Pneus", test_pneus(token)))
    
    # Teste 9: Segurança
    resultados.append(("Segurança", test_security(token)))
    
    # Teste 10: Criar Veículo
    resultados.append(("Criar Veículo", test_create_veiculo(token)))
    
    # Relatório Final
    print_header("RELATÓRIO FINAL - SISTEMA 100% FUNCIONAL")
    
    total = len(resultados)
    sucesso = sum(1 for _, s in resultados if s)
    falhas = total - sucesso
    percentual = (sucesso / total * 100) if total > 0 else 0
    
    print(f"\n{BLUE}Resumo Geral:{RESET}")
    print(f"  Total de testes: {total}")
    print(f"  Testes bem-sucedidos: {sucesso}/{total} ({percentual:.0f}%)")
    print(f"  Testes falhados: {falhas}/{total}")
    
    print(f"\n{BLUE}Detalhes por Teste:{RESET}")
    for nome, sucesso_teste in resultados:
        status = f"{GREEN}✅ PASSOU{RESET}" if sucesso_teste else f"{RED}❌ FALHOU{RESET}"
        print(f"  {nome}: {status}")
    
    print(f"\n{BLUE}{'='*80}{RESET}")
    if falhas == 0:
        print(f"{GREEN}STATUS FINAL: ✅ TODOS OS TESTES PASSARAM! SISTEMA 100% FUNCIONAL{RESET}")
    else:
        print(f"{YELLOW}STATUS FINAL: ⚠️  {falhas} TESTE(S) FALHARAM{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

if __name__ == '__main__':
    main()

