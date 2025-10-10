#!/usr/bin/env python3
"""
Script para criar usuários de teste no sistema XBPneus
Tipos de usuário: transportador, borracharia, revenda, motorista, recapadora
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.render_production')
sys.path.insert(0, '/opt/render/project/src')

django.setup()

from django.contrib.auth import get_user_model
from usuarios.models import Usuario

User = get_user_model()

# Dados dos usuários de teste
usuarios_teste = [
    {
        'email': 'transportador.teste@xbpneus.com',
        'password': 'Teste@2025',
        'nome': 'Transportador Teste',
        'tipo_usuario': 'transportador',
        'cpf_cnpj': '12345678901',
        'telefone': '11999999001',
        'is_active': True,
        'is_approved': True,
    },
    {
        'email': 'borracharia.teste@xbpneus.com',
        'password': 'Teste@2025',
        'nome': 'Borracharia Teste',
        'tipo_usuario': 'borracharia',
        'cpf_cnpj': '12345678902',
        'telefone': '11999999002',
        'is_active': True,
        'is_approved': True,
    },
    {
        'email': 'revenda.teste@xbpneus.com',
        'password': 'Teste@2025',
        'nome': 'Revenda Teste',
        'tipo_usuario': 'revenda',
        'cpf_cnpj': '12345678903',
        'telefone': '11999999003',
        'is_active': True,
        'is_approved': True,
    },
    {
        'email': 'motorista.teste@xbpneus.com',
        'password': 'Teste@2025',
        'nome': 'Motorista Teste',
        'tipo_usuario': 'motorista',
        'cpf_cnpj': '12345678904',
        'telefone': '11999999004',
        'is_active': True,
        'is_approved': True,
    },
    {
        'email': 'recapadora.teste@xbpneus.com',
        'password': 'Teste@2025',
        'nome': 'Recapadora Teste',
        'tipo_usuario': 'recapadora',
        'cpf_cnpj': '12345678905',
        'telefone': '11999999005',
        'is_active': True,
        'is_approved': True,
    },
]

# Criar superusuário admin
print("=" * 60)
print("CRIANDO SUPERUSUÁRIO ADMIN")
print("=" * 60)

admin_email = 'admin@xbpneus.com'
admin_password = 'Admin@2025'

try:
    if User.objects.filter(email=admin_email).exists():
        print(f"✅ Superusuário {admin_email} já existe")
        admin = User.objects.get(email=admin_email)
    else:
        admin = User.objects.create_superuser(
            email=admin_email,
            password=admin_password,
            nome='Administrador Sistema'
        )
        print(f"✅ Superusuário criado: {admin_email}")
        print(f"   Senha: {admin_password}")
except Exception as e:
    print(f"❌ Erro ao criar superusuário: {e}")

print()

# Criar usuários de teste
print("=" * 60)
print("CRIANDO USUÁRIOS DE TESTE")
print("=" * 60)

usuarios_criados = []

for user_data in usuarios_teste:
    email = user_data['email']
    password = user_data.pop('password')
    
    try:
        if User.objects.filter(email=email).exists():
            print(f"⚠️  Usuário {email} já existe")
            user = User.objects.get(email=email)
            # Atualizar senha
            user.set_password(password)
            user.save()
            print(f"   Senha atualizada para: {password}")
        else:
            user = User.objects.create_user(
                email=email,
                password=password,
                **user_data
            )
            print(f"✅ Usuário criado: {email}")
            print(f"   Tipo: {user_data['tipo_usuario']}")
            print(f"   Senha: {password}")
        
        usuarios_criados.append({
            'email': email,
            'password': password,
            'tipo': user_data['tipo_usuario'],
            'nome': user_data['nome']
        })
    except Exception as e:
        print(f"❌ Erro ao criar usuário {email}: {e}")
    
    print()

# Resumo final
print("=" * 60)
print("RESUMO - CREDENCIAIS DE ACESSO")
print("=" * 60)
print()
print("🔐 SUPERUSUÁRIO ADMIN")
print(f"   Email: {admin_email}")
print(f"   Senha: {admin_password}")
print(f"   URL: https://xbpneus-backend.onrender.com/admin")
print()

print("👥 USUÁRIOS DE TESTE")
for user in usuarios_criados:
    print(f"   [{user['tipo'].upper()}] {user['nome']}")
    print(f"   Email: {user['email']}")
    print(f"   Senha: {user['password']}")
    print()

print("=" * 60)
print("✅ SCRIPT CONCLUÍDO COM SUCESSO!")
print("=" * 60)

