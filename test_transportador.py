#!/usr/bin/env python3
"""
Script de Teste Específico para Transportador - Sistema XBPneus
"""
import os
import sys
import django
import requests
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.transportador.models import UsuarioTransportador
from django.contrib.auth.hashers import check_password

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

# Dados de teste
TRANSPORTADOR_TESTE = {
    "email": "transportador.novo@xbpneus.com",
    "password": "senha123",
    "password_confirm": "senha123",
    "nome_razao_social": "Transportadora Novo Teste Ltda",
    "cnpj": "77777777000177",
    "telefone": "(11) 97777-7777"
}

def limpar_transportador_teste():
    """Remove transportador de teste se existir"""
    print_header("LIMPEZA: Removendo Transportador de Teste Anterior")
    
    try:
        user = UsuarioTransportador.objects.filter(email=TRANSPORTADOR_TESTE['email']).first()
        if user:
            user.delete()
            print_success(f"Transportador removido: {TRANSPORTADOR_TESTE['email']}")
        else:
            print_info("Nenhum transportador anterior encontrado")
    except Exception as e:
        print_error(f"Erro na limpeza: {str(e)}")

def teste_1_cadastro_valido():
    """Teste 1: Cadastro com dados válidos"""
    print_header("TESTE 1: Cadastro de Transportador com Dados Válidos")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transportador/register/",
            json=TRANSPORTADOR_TESTE,
            headers={"Content-Type": "application/json"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            print_success("Cadastro realizado com sucesso!")
            print_info(f"   ID: {data.get('id', 'N/A')}")
            print_info(f"   Email: {data.get('email', 'N/A')}")
            print_info(f"   CNPJ: {data.get('cnpj', 'N/A')}")
            print_info(f"   Aprovado: {data.get('aprovado', False)}")
            print_info(f"   Ativo: {data.get('is_active', False)}")
            return True
        else:
            print_error(f"Erro no cadastro: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def teste_2_cadastro_email_duplicado():
    """Teste 2: Cadastro com email duplicado"""
    print_header("TESTE 2: Cadastro com Email Duplicado")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transportador/register/",
            json=TRANSPORTADOR_TESTE,
            headers={"Content-Type": "application/json"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            if 'email' in data:
                print_success("Validação de email duplicado funcionando!")
                print_info(f"   Mensagem: {data['email']}")
                return True
            else:
                print_error("Erro não retornou campo 'email'")
                return False
        else:
            print_error(f"Status inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def teste_3_cadastro_senha_curta():
    """Teste 3: Cadastro com senha muito curta"""
    print_header("TESTE 3: Cadastro com Senha Muito Curta")
    
    dados = TRANSPORTADOR_TESTE.copy()
    dados['email'] = 'outro.transportador@xbpneus.com'
    dados['cnpj'] = '88888888000188'
    dados['password'] = '123'
    dados['password_confirm'] = '123'
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transportador/register/",
            json=dados,
            headers={"Content-Type": "application/json"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            if 'password' in data:
                print_success("Validação de senha mínima funcionando!")
                print_info(f"   Mensagem: {data['password']}")
                return True
            else:
                print_error("Erro não retornou campo 'password'")
                return False
        else:
            print_error(f"Status inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def teste_4_cadastro_senhas_diferentes():
    """Teste 4: Cadastro com senhas não coincidentes"""
    print_header("TESTE 4: Cadastro com Senhas Não Coincidentes")
    
    dados = TRANSPORTADOR_TESTE.copy()
    dados['email'] = 'outro2.transportador@xbpneus.com'
    dados['cnpj'] = '99999999000199'
    dados['password'] = 'senha123'
    dados['password_confirm'] = 'senha456'
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transportador/register/",
            json=dados,
            headers={"Content-Type": "application/json"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            if 'password' in data or 'non_field_errors' in data:
                print_success("Validação de senhas coincidentes funcionando!")
                print_info(f"   Mensagem: {data.get('password', data.get('non_field_errors', 'N/A'))}")
                return True
            else:
                print_error("Erro não retornou validação de senha")
                return False
        else:
            print_error(f"Status inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def teste_5_aprovacao_admin():
    """Teste 5: Aprovação pelo administrador"""
    print_header("TESTE 5: Aprovação pelo Administrador")
    
    try:
        user = UsuarioTransportador.objects.get(email=TRANSPORTADOR_TESTE['email'])
        admin = UsuarioTransportador.objects.filter(is_superuser=True).first()
        
        if not admin:
            print_error("Administrador não encontrado!")
            return False
        
        print_info(f"Transportador ID: {user.id}")
        print_info(f"Status antes: Aprovado={user.aprovado}, Ativo={user.is_active}")
        
        # Aprovar
        user.aprovado = True
        user.is_active = True
        user.aprovado_em = datetime.now()
        user.aprovado_por = admin.email
        user.save()
        
        # Verificar
        user.refresh_from_db()
        
        if user.aprovado and user.is_active:
            print_success("Aprovação realizada com sucesso!")
            print_info(f"   Status depois: Aprovado={user.aprovado}, Ativo={user.is_active}")
            print_info(f"   Aprovado por: {user.aprovado_por}")
            return True
        else:
            print_error("Aprovação não foi aplicada corretamente")
            return False
            
    except UsuarioTransportador.DoesNotExist:
        print_error("Transportador não encontrado no banco de dados")
        return False
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def teste_6_login_valido():
    """Teste 6: Login com credenciais válidas"""
    print_header("TESTE 6: Login com Credenciais Válidas")
    
    dados_login = {
        "email": TRANSPORTADOR_TESTE['email'],
        "password": TRANSPORTADOR_TESTE['password']
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transportador/login/",
            json=dados_login,
            headers={"Content-Type": "application/json"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # Aceitar tanto 'access' direto quanto dentro de 'tokens'
            tem_token = ('access' in data or 'token' in data or 
                        ('tokens' in data and 'access' in data['tokens']))
            if tem_token:
                print_success("Login realizado com sucesso!")
                print_info(f"   Token recebido: Sim")
                print_info(f"   Usuário: {data.get('user', {}).get('email', 'N/A')}")
                print_info(f"   Redirect: {data.get('redirect', 'N/A')}")
                return True
            else:
                print_error("Resposta não contém token")
                print_info(f"   Resposta: {json.dumps(data, indent=2)}")
                return False
        else:
            print_error(f"Erro no login: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def teste_7_login_senha_incorreta():
    """Teste 7: Login com senha incorreta"""
    print_header("TESTE 7: Login com Senha Incorreta")
    
    dados_login = {
        "email": TRANSPORTADOR_TESTE['email'],
        "password": "senhaerrada123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transportador/login/",
            json=dados_login,
            headers={"Content-Type": "application/json"}
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 401 or response.status_code == 400:
            print_success("Validação de senha incorreta funcionando!")
            print_info(f"   Mensagem: {response.text}")
            return True
        else:
            print_error(f"Status inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def teste_8_verificacao_banco():
    """Teste 8: Verificação no banco de dados"""
    print_header("TESTE 8: Verificação no Banco de Dados")
    
    try:
        user = UsuarioTransportador.objects.get(email=TRANSPORTADOR_TESTE['email'])
        
        print_success("Transportador encontrado no banco!")
        print_info(f"   ID: {user.id}")
        print_info(f"   Email: {user.email}")
        print_info(f"   Nome/Razão Social: {user.nome_razao_social}")
        print_info(f"   CNPJ: {user.cnpj}")
        print_info(f"   Telefone: {user.telefone}")
        print_info(f"   Aprovado: {user.aprovado}")
        print_info(f"   Ativo: {user.is_active}")
        print_info(f"   Superusuário: {user.is_superuser}")
        print_info(f"   Aprovado por: {user.aprovado_por}")
        print_info(f"   Criado em: {user.criado_em}")
        
        # Verificar senha
        senha_ok = check_password(TRANSPORTADOR_TESTE['password'], user.password)
        print_info(f"   Senha hash válida: {senha_ok}")
        
        # Verificar campo empresa
        print_info(f"   Empresa: {user.empresa if hasattr(user, 'empresa') else 'Campo não existe'}")
        
        return True
        
    except UsuarioTransportador.DoesNotExist:
        print_error("Transportador não encontrado no banco de dados")
        return False
    except Exception as e:
        print_error(f"Exceção: {str(e)}")
        return False

def gerar_relatorio(resultados):
    """Gera relatório final"""
    print_header("RELATÓRIO FINAL - TESTES DO TRANSPORTADOR")
    
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
    print_header("TESTES COMPLETOS DO TRANSPORTADOR - SISTEMA XBPNEUS")
    print_info(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_info(f"URL Base: {BASE_URL}")
    
    resultados = {}
    
    # Limpeza
    limpar_transportador_teste()
    
    # Executar testes
    resultados["Teste 1: Cadastro Válido"] = teste_1_cadastro_valido()
    resultados["Teste 2: Email Duplicado"] = teste_2_cadastro_email_duplicado()
    resultados["Teste 3: Senha Curta"] = teste_3_cadastro_senha_curta()
    resultados["Teste 4: Senhas Diferentes"] = teste_4_cadastro_senhas_diferentes()
    resultados["Teste 5: Aprovação Admin"] = teste_5_aprovacao_admin()
    resultados["Teste 6: Login Válido"] = teste_6_login_valido()
    resultados["Teste 7: Senha Incorreta"] = teste_7_login_senha_incorreta()
    resultados["Teste 8: Verificação Banco"] = teste_8_verificacao_banco()
    
    # Relatório
    gerar_relatorio(resultados)

if __name__ == '__main__':
    main()

