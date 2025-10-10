#!/usr/bin/env python3
"""
Script de Teste Completo do Fluxo de Usuários - Sistema XBPneus
Testa cadastro, aprovação e login para os 5 tipos de usuários
"""
import os
import sys
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.transportador.models import UsuarioTransportador
from backend.motorista.models import UsuarioMotorista
from backend.borracharia.models import UsuarioBorracharia
from backend.revenda.models import UsuarioRevenda
from backend.recapagem.models import UsuarioRecapagem
from django.contrib.auth.hashers import check_password

# Cores para output
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

# Dados de teste para os 5 tipos de usuários
USUARIOS_TESTE = {
    'transportador': {
        'model': UsuarioTransportador,
        'data': {
            'email': 'transportador.teste@xbpneus.com',
            'password': 'senha123',
            'nome_razao_social': 'Transportadora Teste Ltda',
            'cnpj': '55555555000155',
            'telefone': '(11) 91111-1111'
        },
        'dashboard': '/dashboard'
    },
    'motorista': {
        'model': UsuarioMotorista,
        'data': {
            'email': 'motorista.teste@xbpneus.com',
            'password': 'senha123',
            'nome_completo': 'João Motorista Silva',
            'cpf': '11111111111',
            'telefone': '(11) 92222-2222',
            'cnh': '12345678901'
        },
        'dashboard': '/motorista/dashboard'
    },
    'borracharia': {
        'model': UsuarioBorracharia,
        'data': {
            'email': 'borracharia.teste@xbpneus.com',
            'password': 'senha123',
            'nome_razao_social': 'Borracharia Teste Ltda',
            'cnpj': '22222222000122',
            'telefone': '(11) 93333-3333'
        },
        'dashboard': '/borracharia/dashboard'
    },
    'revenda': {
        'model': UsuarioRevenda,
        'data': {
            'email': 'revenda.teste@xbpneus.com',
            'password': 'senha123',
            'nome_razao_social': 'Revenda Teste Ltda',
            'cnpj': '33333333000133',
            'telefone': '(11) 94444-4444'
        },
        'dashboard': '/revenda/dashboard'
    },
    'recapadora': {
        'model': UsuarioRecapagem,
        'data': {
            'email': 'recapadora.teste@xbpneus.com',
            'password': 'senha123',
            'nome_razao_social': 'Recapadora Teste Ltda',
            'cnpj': '44444444000144',
            'telefone': '(11) 95555-5555'
        },
        'dashboard': '/recapadora/dashboard'
    }
}

def limpar_usuarios_teste():
    """Remove usuários de teste anteriores"""
    print_header("FASE 0: Limpeza de Usuários de Teste Anteriores")
    
    for tipo, config in USUARIOS_TESTE.items():
        model = config['model']
        email = config['data']['email']
        
        try:
            usuario = model.objects.filter(email=email).first()
            if usuario:
                usuario.delete()
                print_info(f"Usuário {tipo} anterior removido: {email}")
            else:
                print_info(f"Nenhum usuário {tipo} anterior encontrado")
        except Exception as e:
            print_error(f"Erro ao limpar {tipo}: {str(e)}")

def fase1_cadastro():
    """Fase 1: Cadastro dos 5 tipos de usuários"""
    print_header("FASE 1: Cadastro dos 5 Tipos de Usuários")
    
    resultados = {}
    
    for tipo, config in USUARIOS_TESTE.items():
        print(f"\n{YELLOW}Cadastrando {tipo.upper()}...{RESET}")
        
        model = config['model']
        data = config['data'].copy()
        password = data.pop('password')
        
        try:
            # Criar usuário
            if hasattr(model.objects, 'create_user'):
                usuario = model.objects.create_user(password=password, **data)
            else:
                usuario = model.objects.create(**data)
                usuario.set_password(password)
                usuario.save()
            
            print_success(f"{tipo.capitalize()} cadastrado: {data['email']}")
            print_info(f"   ID: {usuario.id}")
            print_info(f"   Aprovado: {getattr(usuario, 'aprovado', 'N/A')}")
            print_info(f"   Ativo: {usuario.is_active}")
            
            resultados[tipo] = {
                'cadastro': 'SUCESSO',
                'id': usuario.id,
                'email': data['email']
            }
            
        except Exception as e:
            print_error(f"Erro ao cadastrar {tipo}: {str(e)}")
            resultados[tipo] = {
                'cadastro': 'ERRO',
                'erro': str(e)
            }
    
    return resultados

def fase2_aprovacao(resultados):
    """Fase 2: Aprovação dos usuários pelo administrador"""
    print_header("FASE 2: Aprovação dos Usuários pelo Administrador")
    
    admin = UsuarioTransportador.objects.filter(is_superuser=True).first()
    if not admin:
        print_error("Nenhum administrador encontrado!")
        return resultados
    
    print_info(f"Administrador: {admin.email}")
    
    for tipo, config in USUARIOS_TESTE.items():
        if resultados[tipo]['cadastro'] != 'SUCESSO':
            print_info(f"Pulando {tipo} (cadastro falhou)")
            continue
            
        print(f"\n{YELLOW}Aprovando {tipo.upper()}...{RESET}")
        
        model = config['model']
        email = config['data']['email']
        
        try:
            usuario = model.objects.get(email=email)
            
            # Aprovar usuário
            if hasattr(usuario, 'aprovado'):
                usuario.aprovado = True
                usuario.aprovado_em = datetime.now()
                usuario.aprovado_por = admin.email
            
            usuario.is_active = True
            usuario.save()
            
            print_success(f"{tipo.capitalize()} aprovado com sucesso!")
            print_info(f"   Aprovado: {getattr(usuario, 'aprovado', 'N/A')}")
            print_info(f"   Ativo: {usuario.is_active}")
            
            resultados[tipo]['aprovacao'] = 'SUCESSO'
            
        except Exception as e:
            print_error(f"Erro ao aprovar {tipo}: {str(e)}")
            resultados[tipo]['aprovacao'] = 'ERRO'
            resultados[tipo]['erro_aprovacao'] = str(e)
    
    return resultados

def fase3_login(resultados):
    """Fase 3: Teste de login para cada tipo de usuário"""
    print_header("FASE 3: Teste de Login dos Usuários")
    
    for tipo, config in USUARIOS_TESTE.items():
        if resultados[tipo].get('aprovacao') != 'SUCESSO':
            print_info(f"Pulando login de {tipo} (aprovação falhou)")
            continue
            
        print(f"\n{YELLOW}Testando login de {tipo.upper()}...{RESET}")
        
        model = config['model']
        email = config['data']['email']
        password = config['data']['password']
        
        try:
            # Buscar usuário
            usuario = model.objects.get(email=email)
            
            # Verificar senha
            senha_correta = check_password(password, usuario.password)
            
            if senha_correta:
                print_success(f"Login de {tipo} bem-sucedido!")
                print_info(f"   Email: {email}")
                print_info(f"   Dashboard: {config['dashboard']}")
                print_info(f"   Aprovado: {getattr(usuario, 'aprovado', 'N/A')}")
                print_info(f"   Ativo: {usuario.is_active}")
                
                resultados[tipo]['login'] = 'SUCESSO'
                resultados[tipo]['dashboard'] = config['dashboard']
            else:
                print_error(f"Senha incorreta para {tipo}")
                resultados[tipo]['login'] = 'ERRO'
                resultados[tipo]['erro_login'] = 'Senha incorreta'
                
        except model.DoesNotExist:
            print_error(f"Usuário {tipo} não encontrado")
            resultados[tipo]['login'] = 'ERRO'
            resultados[tipo]['erro_login'] = 'Usuário não encontrado'
        except Exception as e:
            print_error(f"Erro no login de {tipo}: {str(e)}")
            resultados[tipo]['login'] = 'ERRO'
            resultados[tipo]['erro_login'] = str(e)
    
    return resultados

def gerar_relatorio(resultados):
    """Gera relatório final dos testes"""
    print_header("RELATÓRIO FINAL DOS TESTES")
    
    total = len(resultados)
    cadastros_ok = sum(1 for r in resultados.values() if r.get('cadastro') == 'SUCESSO')
    aprovacoes_ok = sum(1 for r in resultados.values() if r.get('aprovacao') == 'SUCESSO')
    logins_ok = sum(1 for r in resultados.values() if r.get('login') == 'SUCESSO')
    
    print(f"\n{BLUE}Resumo Geral:{RESET}")
    print(f"  Total de tipos de usuários: {total}")
    print(f"  Cadastros bem-sucedidos: {cadastros_ok}/{total} ({cadastros_ok*100//total}%)")
    print(f"  Aprovações bem-sucedidas: {aprovacoes_ok}/{total} ({aprovacoes_ok*100//total}%)")
    print(f"  Logins bem-sucedidos: {logins_ok}/{total} ({logins_ok*100//total}%)")
    
    print(f"\n{BLUE}Detalhes por Tipo de Usuário:{RESET}\n")
    
    for tipo, resultado in resultados.items():
        print(f"{YELLOW}{tipo.upper()}{RESET}")
        print(f"  Email: {resultado.get('email', 'N/A')}")
        print(f"  Cadastro: {resultado.get('cadastro', 'N/A')}")
        print(f"  Aprovação: {resultado.get('aprovacao', 'N/A')}")
        print(f"  Login: {resultado.get('login', 'N/A')}")
        print(f"  Dashboard: {resultado.get('dashboard', 'N/A')}")
        
        if resultado.get('cadastro') == 'ERRO':
            print(f"  {RED}Erro no cadastro: {resultado.get('erro', 'N/A')}{RESET}")
        if resultado.get('aprovacao') == 'ERRO':
            print(f"  {RED}Erro na aprovação: {resultado.get('erro_aprovacao', 'N/A')}{RESET}")
        if resultado.get('login') == 'ERRO':
            print(f"  {RED}Erro no login: {resultado.get('erro_login', 'N/A')}{RESET}")
        print()
    
    # Salvar relatório em JSON
    with open('/home/ubuntu/relatorio_testes_usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False, default=str)
    
    print_success("Relatório salvo em: /home/ubuntu/relatorio_testes_usuarios.json")
    
    # Status final
    if logins_ok == total:
        print(f"\n{GREEN}{'='*80}{RESET}")
        print(f"{GREEN}STATUS FINAL: ✅ TODOS OS TESTES PASSARAM COM SUCESSO!{RESET}")
        print(f"{GREEN}{'='*80}{RESET}\n")
    else:
        print(f"\n{YELLOW}{'='*80}{RESET}")
        print(f"{YELLOW}STATUS FINAL: ⚠️  ALGUNS TESTES FALHARAM{RESET}")
        print(f"{YELLOW}{'='*80}{RESET}\n")

def main():
    """Função principal"""
    print_header("TESTE COMPLETO DO FLUXO DE USUÁRIOS - SISTEMA XBPNEUS")
    print_info(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print_info(f"Tipos de usuários: {len(USUARIOS_TESTE)}")
    
    # Fase 0: Limpeza
    limpar_usuarios_teste()
    
    # Fase 1: Cadastro
    resultados = fase1_cadastro()
    
    # Fase 2: Aprovação
    resultados = fase2_aprovacao(resultados)
    
    # Fase 3: Login
    resultados = fase3_login(resultados)
    
    # Relatório Final
    gerar_relatorio(resultados)

if __name__ == '__main__':
    main()

