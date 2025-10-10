#!/usr/bin/env python3
"""
Script de seed usando SQL direto para evitar problemas de ORM
"""
import os, sys, django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from backend.empresas.models import Empresa
from backend.users.models import User

def seed():
    print("=" * 80)
    print("SEED SQL DIRETO - XBPNEUS v10.0.6")
    print("=" * 80 + "\n")
    
    cursor = connection.cursor()
    
    # Empresa
    print("📦 Empresa...")
    empresa, created = Empresa.objects.get_or_create(
        cnpj='12345678000190',
        defaults={'nome': 'Transportadora XB Pneus Ltda', 'tipo': 'Transportadora'}
    )
    print(f"   {'✅ Criada' if created else 'ℹ️  Já existe'}: {empresa.nome}\n")
    
    # Admin
    print("👤 Admin...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@xbpneus.com', 'admin123', empresa=empresa)
        print("   ✅ Admin criado\n")
    else:
        print("   ℹ️  Admin já existe\n")
    
    # Veículos - SQL direto
    print("🚚 Veículos...")
    veiculos = [
        ('ABC1234', 'Scania', 'R450', 'Caminhão', 'Ativo', 50000, 48000, 3, 10),
        ('DEF5678', 'Volvo', 'FH540', 'Caminhão', 'Ativo', 45000, 43000, 3, 10),
        ('GHI9012', 'Mercedes', 'Actros', 'Caminhão', 'Ativo', 60000, 58000, 3, 10),
    ]
    
    now = datetime.now().isoformat()
    for placa, marca, modelo, tipo, status, km, km_ult, eixos, posicoes in veiculos:
        cursor.execute("""
            INSERT OR IGNORE INTO frota_vehicle 
            (placa, marca, modelo, tipo, status, km, km_ultima_manutencao, numero_eixos, total_posicoes_pneus, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (placa, marca, modelo, tipo, status, km, km_ult, eixos, posicoes, now, now))
        if cursor.rowcount > 0:
            print(f"   ✅ Criado: {placa} - {marca} {modelo}")
        else:
            print(f"   ℹ️  Já existe: {placa}")
    print()
    
    # Pneus - SQL direto
    print("🛞 Pneus...")
    count = 0
    for i in range(1, 11):
        codigo = f'PN{i:04d}'
        cursor.execute("""
            INSERT OR IGNORE INTO pneus_tire
            (codigo, medida, tipo, dot, status, posicao_atual, km_total, km_atual, numero_recapagens, pode_recapar, valor_compra, valor_atual, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, '295/80R22.5', 'Novo', '202401', 'Estoque', 'Estoque', 0, 0, 0, 1, 1200.00, 1200.00, now, now))
        if cursor.rowcount > 0:
            count += 1
    print(f"   ✅ {count} pneus criados\n")
    
    connection.commit()
    
    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM empresas_empresa")
    empresas_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users_user")
    users_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM frota_vehicle")
    vehicles_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM pneus_tire")
    tires_count = cursor.fetchone()[0]
    
    print("=" * 80)
    print("✅ SEED CONCLUÍDO!")
    print("=" * 80)
    print("\n📊 Dados no Banco:")
    print(f"   • {empresas_count} Empresa(s)")
    print(f"   • {users_count} Usuário(s)")
    print(f"   • {vehicles_count} Veículo(s)")
    print(f"   • {tires_count} Pneu(s)")
    print("\n🔑 Credenciais:")
    print("   • admin / admin123")
    print("\n✅ Banco populado com sucesso!\n")

if __name__ == '__main__':
    try:
        seed()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
