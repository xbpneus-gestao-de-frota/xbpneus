#!/usr/bin/env python3
"""
Script de seed funcional - Baseado na estrutura real do banco
Uso: python seed_working.py
"""
import os, sys, django
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.empresas.models import Empresa
from backend.users.models import User
from backend.transportador.frota.models import Vehicle
from backend.transportador.pneus.models import Tire

def seed():
    print("=" * 80)
    print("SEED FUNCIONAL - XBPNEUS v10.0.6")
    print("=" * 80 + "\n")
    
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
    
    # Veículos - SEM campo empresa
    print("🚚 Veículos...")
    veiculos_data = [
        {'placa': 'ABC1234', 'marca': 'Scania', 'modelo': 'R450'},
        {'placa': 'DEF5678', 'marca': 'Volvo', 'modelo': 'FH540'},
        {'placa': 'GHI9012', 'marca': 'Mercedes', 'modelo': 'Actros'},
    ]
    
    for data in veiculos_data:
        v, created = Vehicle.objects.get_or_create(
            placa=data['placa'],
            defaults={
                'modelo': data['modelo'],
                'marca': data['marca'],
                'tipo': 'Caminhão',
                'status': 'Ativo',
                'km': 50000,
                'km_ultima_manutencao': 48000,
                'numero_eixos': 3,
                'total_posicoes_pneus': 10,
            }
        )
        print(f"   {'✅ Criado' if created else 'ℹ️  Já existe'}: {v.placa} - {v.marca} {v.modelo}")
    print()
    
    # Pneus - Verificar campos obrigatórios reais
    print("🛞 Pneus...")
    count = 0
    for i in range(1, 11):
        codigo = f'PN{i:04d}'
        if not Tire.objects.filter(codigo=codigo).exists():
            try:
                Tire.objects.create(
                    codigo=codigo,
                    medida='295/80R22.5',
                    tipo='Novo',
                    dot='202401',
                    status='Estoque',
                    posicao_atual='Estoque',
                    km_total=0,
                    km_atual=0,
                    numero_recapagens=0,
                    pode_recapar=True,
                    valor_compra=Decimal('1200.00'),
                    valor_atual=Decimal('1200.00'),
                )
                count += 1
            except Exception as e:
                print(f"   ⚠️  Erro ao criar pneu {codigo}: {e}")
                # Tentar descobrir campos obrigatórios
                from backend.transportador.pneus.models import Tire as TireModel
                required = [f.name for f in TireModel._meta.get_fields() if hasattr(f, 'null') and not f.null and f.name not in ['id', 'criado_em', 'atualizado_em']]
                print(f"   ℹ️  Campos obrigatórios: {', '.join(required)}")
                break
    
    if count > 0:
        print(f"   ✅ {count} pneus criados\n")
    else:
        print(f"   ℹ️  Pneus já existem ou erro ao criar\n")
    
    print("=" * 80)
    print("✅ SEED CONCLUÍDO!")
    print("=" * 80)
    print("\n📊 Dados no Banco:")
    print(f"   • {Empresa.objects.count()} Empresa(s)")
    print(f"   • {User.objects.count()} Usuário(s)")
    print(f"   • {Vehicle.objects.count()} Veículo(s)")
    print(f"   • {Tire.objects.count()} Pneu(s)")
    print("\n🔑 Credenciais:")
    print("   • admin / admin123")
    print("\n✅ Banco populado!\n")

if __name__ == '__main__':
    try:
        seed()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
