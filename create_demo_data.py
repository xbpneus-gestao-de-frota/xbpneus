#!/usr/bin/env python3
"""
Script para criar dados de demonstração no sistema XBPneus
"""
import os
import django
import sys

# Configurar Django
sys.path.append('/home/ubuntu/xbpneus')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.transportador.frota.models import Vehicle
from backend.transportador.pneus.models import Tire
from backend.transportador.manutencao.models import OrdemServico
from backend.transportador.empresas.models import Empresa
from django.contrib.auth import get_user_model

User = get_user_model()

def create_demo_data():
    print("🚀 Criando dados de demonstração...")
    
    # Buscar usuário de teste
    try:
        user = User.objects.get(email='transportador.teste2@xbpneus.com')
        empresa = user.transportador.empresa
        print(f"✅ Usuário encontrado: {user.email}")
        print(f"✅ Empresa: {empresa.nome}")
    except:
        print("❌ Usuário não encontrado!")
        return
    
    # Criar veículos
    print("\n📦 Criando veículos...")
    veiculos_data = [
        {'placa': 'ABC1234', 'marca': 'Mercedes-Benz', 'modelo': 'Actros 2546', 'tipo': 'CAMINHAO', 'ano_fabricacao': 2020, 'km_atual': 150000},
        {'placa': 'DEF5678', 'marca': 'Scania', 'modelo': 'R 450', 'tipo': 'CAVALO_MECANICO', 'ano_fabricacao': 2021, 'km_atual': 80000},
        {'placa': 'GHI9012', 'marca': 'Volvo', 'modelo': 'FH 540', 'tipo': 'CAMINHAO', 'ano_fabricacao': 2019, 'km_atual': 200000},
    ]
    
    for vdata in veiculos_data:
        v, created = Vehicle.objects.get_or_create(
            placa=vdata['placa'],
            defaults={**vdata, 'empresa': empresa}
        )
        if created:
            print(f"  ✅ Veículo criado: {v.placa} - {v.marca} {v.modelo}")
    
    # Criar pneus
    print("\n🛞 Criando pneus...")
    pneus_data = [
        {'numero_serie': 'PN001', 'marca': 'Michelin', 'modelo': 'X Multi D', 'medida': '295/80R22.5', 'dot': '2320', 'sulco_atual': 18.0, 'status': 'ESTOQUE'},
        {'numero_serie': 'PN002', 'marca': 'Pirelli', 'modelo': 'FH01', 'medida': '295/80R22.5', 'dot': '1520', 'sulco_atual': 16.5, 'status': 'ESTOQUE'},
        {'numero_serie': 'PN003', 'marca': 'Goodyear', 'modelo': 'G159', 'medida': '295/80R22.5', 'dot': '4220', 'sulco_atual': 19.0, 'status': 'ESTOQUE'},
        {'numero_serie': 'PN004', 'marca': 'Bridgestone', 'modelo': 'R268', 'medida': '295/80R22.5', 'dot': '3020', 'sulco_atual': 17.0, 'status': 'ESTOQUE'},
        {'numero_serie': 'PN005', 'marca': 'Continental', 'modelo': 'HDR2', 'medida': '295/80R22.5', 'dot': '2820', 'sulco_atual': 18.5, 'status': 'ESTOQUE'},
    ]
    
    for pdata in pneus_data:
        p, created = Tire.objects.get_or_create(
            numero_serie=pdata['numero_serie'],
            defaults={**pdata, 'empresa': empresa}
        )
        if created:
            print(f"  ✅ Pneu criado: {p.numero_serie} - {p.marca} {p.modelo}")
    
    # Criar ordens de serviço
    print("\n🔧 Criando ordens de serviço...")
    veiculo = Vehicle.objects.filter(empresa=empresa).first()
    if veiculo:
        os_data = [
            {'tipo': 'PREVENTIVA', 'descricao': 'Revisão dos 150.000 km', 'prioridade': 'MEDIA', 'status': 'ABERTA'},
            {'tipo': 'CORRETIVA', 'descricao': 'Troca de óleo e filtros', 'prioridade': 'ALTA', 'status': 'EM_ANDAMENTO'},
        ]
        
        for osdata in os_data:
            os, created = OrdemServico.objects.get_or_create(
                veiculo=veiculo,
                descricao=osdata['descricao'],
                defaults={**osdata, 'empresa': empresa}
            )
            if created:
                print(f"  ✅ OS criada: {os.descricao}")
    
    print("\n🎉 Dados de demonstração criados com sucesso!")
    print(f"   📊 {Vehicle.objects.filter(empresa=empresa).count()} veículos")
    print(f"   🛞 {Tire.objects.filter(empresa=empresa).count()} pneus")
    print(f"   🔧 {OrdemServico.objects.filter(empresa=empresa).count()} ordens de serviço")

if __name__ == '__main__':
    create_demo_data()
