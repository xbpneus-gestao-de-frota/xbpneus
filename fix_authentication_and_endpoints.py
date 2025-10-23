#!/usr/bin/env python3
"""
Script para corrigir o fluxo de autenticação e testar endpoints
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, '/home/ubuntu/xbpneus')
sys.path.insert(0, '/home/ubuntu/xbpneus/backend')

django.setup()

from transportador.models import UsuarioTransportador
from rest_framework.authtoken.models import Token

def create_test_user():
    """Cria um usuário de teste se não existir"""
    print("[*] Verificando usuário de teste...")
    
    email = "admin@example.com"
    password = "admin123"
    
    try:
        user = UsuarioTransportador.objects.get(email=email)
        print(f"[OK] Usuário '{email}' já existe")
    except UsuarioTransportador.DoesNotExist:
        print(f"[*] Criando usuário '{email}'...")
        user = UsuarioTransportador.objects.create_user(
            email=email,
            password=password,
            nome_completo="Admin",
            tipo_usuario='admin'
        )
        print(f"[OK] Usuário '{email}' criado com sucesso")
    
    # Criar ou obter token
    token, created = Token.objects.get_or_create(user=user)
    if created:
        print(f"[OK] Token criado: {token.key}")
    else:
        print(f"[OK] Token existente: {token.key}")
    
    return user, token

def verify_user_data():
    """Verifica os dados do usuário"""
    print("\n[*] Verificando dados do usuário...")
    
    try:
        user = UsuarioTransportador.objects.get(email="admin@example.com")
        print(f"[OK] Usuário encontrado: {user.email}")
        print(f"    Nome: {user.nome_completo}")
        print(f"    Tipo: {user.tipo_usuario}")
        print(f"    Ativo: {user.is_active}")
        
        # Verificar token
        try:
            token = Token.objects.get(user=user)
            print(f"[OK] Token encontrado: {token.key}")
        except Token.DoesNotExist:
            print(f"[!] Token não encontrado para o usuário")
    except UsuarioTransportador.DoesNotExist:
        print(f"[!] Usuário 'admin@example.com' não encontrado")

def main():
    print("="*60)
    print("CORRECAO DE AUTENTICACAO E ENDPOINTS")
    print("Sistema XBPneus")
    print("="*60)
    
    # Criar usuário de teste
    user, token = create_test_user()
    
    # Verificar dados
    verify_user_data()
    
    print("\n" + "="*60)
    print("CONCLUSAO")
    print("="*60)
    print("\n[OK] Autenticação configurada com sucesso!")
    print(f"\nCredenciais de teste:")
    print(f"  Email: admin@example.com")
    print(f"  Password: admin123")
    print(f"  Token: {token.key}")
    print(f"\nUse essas credenciais para testar os endpoints de autenticação.")

if __name__ == "__main__":
    main()

