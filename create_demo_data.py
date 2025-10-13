#!/usr/bin/env python3
"""
Script para criar dados de demonstração no sistema XBPneus
Uso: python create_demo_data.py [email_do_usuario]
"""
import os
import django
import sys

# Configurar Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.transportador.frota.models import Vehicle
from backend.transportador.pneus.models import Tire
from backend.transportador.manutencao.models import OrdemServico
from backend.transportador.empresas.models import Empresa
from django.contrib.auth import get_user_model

User = get_user_model()

def create_demo_data(user_email=None):
    print("🚀 Criando dados de demonstração...")
    
    # Buscar usuário
    try:
        if user_email:
            user = User.objects.get(email=user_email)
        else:
            # Buscar primeiro usuário transportador aprovado
            user = User.objects.filter(
                tipo='transportador',
                is_active=True
            ).first()
            
        if not user:
            print("❌ Nenhum usuário transportador encontrado!")
            print("💡 Crie um usuário primeiro ou especifique um email:")
            print("   python create_demo_data.py usuario@email.com")
            return
            
        empresa = user.transportador.empresa
        print(f"✅ Usuário: {user.email}")
        print(f"✅ Empresa: {empresa.nome}")
    except Exception as e:
        print(f"❌ Erro ao buscar usuário: {e}")
        return
    
    # Criar veículos
    print("\n📦 Criando veículos...")
    veiculos_data = [
        {
            'placa': 'ABC1D34', 
            'marca': 'Mercedes-Benz', 
            'modelo': 'Actros 2546', 
            'tipo': 'CAMINHAO', 
            'ano_fabricacao': 2020, 
            'km_atual': 150000,
            'km_proxima_manutencao': 160000,
            'ativo': True
        },
        {
            'placa': 'DEF5G78', 
            'marca': 'Scania', 
            'modelo': 'R 450', 
            'tipo': 'CAVALO_MECANICO', 
            'ano_fabricacao': 2021, 
            'km_atual': 80000,
            'km_proxima_manutencao': 90000,
            'ativo': True
        },
        {
            'placa': 'GHI9J12', 
            'marca': 'Volvo', 
            'modelo': 'FH 540', 
            'tipo': 'CAMINHAO', 
            'ano_fabricacao': 2019, 
            'km_atual': 200000,
            'km_proxima_manutencao': 205000,
            'ativo': True
        },
    ]
    
    veiculos_criados = 0
    for vdata in veiculos_data:
        v, created = Vehicle.objects.get_or_create(
            placa=vdata['placa'],
            defaults={**vdata, 'empresa': empresa}
        )
        if created:
            veiculos_criados += 1
            print(f"  ✅ Veículo criado: {v.placa} - {v.marca} {v.modelo}")
        else:
            print(f"  ℹ️  Veículo já existe: {v.placa}")
    
    # Criar pneus
    print("\n🛞 Criando pneus...")
    pneus_data = [
        {'numero_fogo': 'PN001', 'marca': 'Michelin', 'modelo': 'X Multi D', 'medida': '295/80R22.5', 'dot': '2320', 'sulco_atual': 18.0, 'status': 'ESTOQUE'},
        {'numero_fogo': 'PN002', 'marca': 'Pirelli', 'modelo': 'FH01', 'medida': '295/80R22.5', 'dot': '1520', 'sulco_atual': 4.5, 'status': 'MONTADO'},
        {'numero_fogo': 'PN003', 'marca': 'Goodyear', 'modelo': 'G159', 'medida': '295/80R22.5', 'dot': '4220', 'sulco_atual': 19.0, 'status': 'ESTOQUE'},
        {'numero_fogo': 'PN004', 'marca': 'Bridgestone', 'modelo': 'R268', 'medida': '295/80R22.5', 'dot': '3020', 'sulco_atual': 2.5, 'status': 'MONTADO'},
        {'numero_fogo': 'PN005', 'marca': 'Continental', 'modelo': 'HDR2', 'medida': '295/80R22.5', 'dot': '2820', 'sulco_atual': 18.5, 'status': 'ESTOQUE'},
    ]
    
    pneus_criados = 0
    for pdata in pneus_data:
        p, created = Tire.objects.get_or_create(
            numero_fogo=pdata['numero_fogo'],
            defaults={**pdata, 'empresa': empresa}
        )
        if created:
            pneus_criados += 1
            print(f"  ✅ Pneu criado: {p.numero_fogo} - {p.marca} {p.modelo} (Sulco: {p.sulco_atual}mm)")
        else:
            print(f"  ℹ️  Pneu já existe: {p.numero_fogo}")
    
    # Criar ordens de serviço
    print("\n🔧 Criando ordens de serviço...")
    veiculo = Vehicle.objects.filter(empresa=empresa).first()
    os_criadas = 0
    if veiculo:
        os_data = [
            {
                'tipo': 'PREVENTIVA', 
                'descricao': 'Revisão dos 150.000 km - Troca de óleo, filtros e verificação geral', 
                'prioridade': 'MEDIA', 
                'status': 'ABERTA',
                'km_veiculo': veiculo.km_atual
            },
            {
                'tipo': 'CORRETIVA', 
                'descricao': 'Troca de pneus críticos (sulco < 3mm)', 
                'prioridade': 'ALTA', 
                'status': 'EM_ANDAMENTO',
                'km_veiculo': veiculo.km_atual
            },
        ]
        
        for osdata in os_data:
            # Verificar se já existe OS similar
            existing = OrdemServico.objects.filter(
                veiculo=veiculo,
                descricao__icontains=osdata['descricao'].split('-')[0].strip()
            ).exists()
            
            if not existing:
                os = OrdemServico.objects.create(
                    veiculo=veiculo,
                    empresa=empresa,
                    **osdata
                )
                os_criadas += 1
                print(f"  ✅ OS criada: {os.descricao[:50]}...")
            else:
                print(f"  ℹ️  OS similar já existe")
    
    print("\n" + "="*60)
    print("🎉 Dados de demonstração processados!")
    print("="*60)
    print(f"   📊 Veículos: {veiculos_criados} criados, {Vehicle.objects.filter(empresa=empresa).count()} total")
    print(f"   🛞 Pneus: {pneus_criados} criados, {Tire.objects.filter(empresa=empresa).count()} total")
    print(f"   🔧 Ordens de Serviço: {os_criadas} criadas, {OrdemServico.objects.filter(empresa=empresa).count()} total")
    print("="*60)
    print("\n💡 Agora acesse o dashboard para ver os dados!")
    print(f"   🌐 https://xbpneus-frontend.onrender.com/login")
    print(f"   📧 Email: {user.email}")

if __name__ == '__main__':
    user_email = sys.argv[1] if len(sys.argv) > 1 else None
    create_demo_data(user_email)

