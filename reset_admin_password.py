#!/usr/bin/env python3
"""
Script para resetar a senha do superusuário admin
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.transportador.models import UsuarioTransportador

# Buscar ou criar admin
admin_email = "admin@xbpneus.com"
admin_password = "admin123"

try:
    admin = UsuarioTransportador.objects.get(email=admin_email)
    admin.set_password(admin_password)
    admin.save()
    print(f"✅ Senha do admin resetada com sucesso!")
    print(f"   Email: {admin_email}")
    print(f"   Senha: {admin_password}")
except UsuarioTransportador.DoesNotExist:
    print(f"❌ Admin não encontrado. Criando novo admin...")
    admin = UsuarioTransportador.objects.create_superuser(
        email=admin_email,
        password=admin_password,
        nome_razao_social="Administrador XBPneus",
        cnpj="00000000000000",
        telefone="(00) 00000-0000"
    )
    print(f"✅ Admin criado com sucesso!")
    print(f"   Email: {admin_email}")
    print(f"   Senha: {admin_password}")

