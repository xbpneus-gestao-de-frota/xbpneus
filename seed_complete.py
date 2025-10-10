#!/usr/bin/env python3
"""
Script de seed completo - Popular banco com dados de teste
Uso: python seed_complete.py
"""
import os, sys, django
from datetime import datetime, timedelta, date
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.empresas.models import Empresa
from backend.users.models import User
from backend.transportador.frota.models import Vehicle, Position
from backend.transportador.motorista_interno.models import MotoristaInterno
from backend.transportador.pneus.models import Tire
from backend.transportador.estoque.models import Produto, CategoriaProduto
from backend.transportador.clientes.models import Cliente
from backend.transportador.fornecedores.models import Fornecedor
from backend.transportador.combustivel.models import PostoCombustivel, Abastecimento
from backend.transportador.custos.models import CategoriaCusto, Custo
from backend.transportador.multas.models import Multa
from backend.transportador.viagens.models import Viagem

def limpar_dados():
    """Limpar dados de teste anteriores"""
    print("🗑️  Limpando dados anteriores...")
    Viagem.objects.all().delete()
    Multa.objects.all().delete()
    Custo.objects.all().delete()
    Abastecimento.objects.all().delete()
    Produto.objects.all().delete()
    CategoriaProduto.objects.all().delete()
    Tire.objects.all().delete()
    Position.objects.all().delete()
    Vehicle.objects.all().delete()
    MotoristaInterno.objects.all().delete()
    PostoCombustivel.objects.all().delete()
    CategoriaCusto.objects.all().delete()
    Cliente.objects.filter(cnpj__startswith='111').delete()
    Fornecedor.objects.filter(cnpj__startswith='222').delete()
    print("   ✅ Dados limpos\n")

def seed():
    print("=" * 80)
    print("SEED COMPLETO - XBPNEUS v10.0.4")
    print("=" * 80 + "\n")
    
    # Limpar dados anteriores
    limpar_dados()
    
    # Empresa
    print("📦 Empresa...")
    empresa = Empresa.objects.first()
    if not empresa:
        empresa = Empresa.objects.create(
            cnpj='12345678000190',
            nome='Transportadora XB Pneus Ltda',
            razao_social='XB Pneus Transportes Ltda'
        )
    print(f"   ✅ {empresa.nome}\n")
    
    # Motoristas
    print("🚛 Motoristas...")
    motoristas = []
    nomes = ['João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa', 'Carlos Souza']
    for i, nome in enumerate(nomes, 1):
        m = MotoristaInterno.objects.create(
            cpf=f'{i:011d}',
            nome_completo=nome,
            cnh=f'SP{i:09d}',
            categoria_cnh='E',
            validade_cnh=date(2026, 12, 31),
            data_nascimento=date(1980 + i, 1, 1),
            data_admissao=date(2020, 1, 1),
            tipo_contrato='CLT',
            status='Ativo',
        )
        motoristas.append(m)
        print(f"   ✅ {m.nome_completo}")
    print()
    
    # Veículos
    print("🚚 Veículos...")
    veiculos_data = [
        {'placa': 'ABC1234', 'marca': 'Scania', 'modelo': 'R450', 'tipo': 'Caminhão', 'eixos': 3, 'posicoes': 10},
        {'placa': 'DEF5678', 'marca': 'Volvo', 'modelo': 'FH540', 'tipo': 'Caminhão', 'eixos': 3, 'posicoes': 10},
        {'placa': 'GHI9012', 'marca': 'Mercedes', 'modelo': 'Actros', 'tipo': 'Caminhão', 'eixos': 3, 'posicoes': 10},
        {'placa': 'JKL3456', 'marca': 'Iveco', 'modelo': 'Stralis', 'tipo': 'Caminhão', 'eixos': 3, 'posicoes': 10},
        {'placa': 'MNO7890', 'marca': 'Randon', 'modelo': 'Bitrem', 'tipo': 'Carreta', 'eixos': 2, 'posicoes': 8},
    ]
    
    veiculos = []
    for data in veiculos_data:
        v = Vehicle.objects.create(
            placa=data['placa'],
            marca=data['marca'],
            modelo=data['modelo'],
            tipo=data['tipo'],
            status='Ativo',
            km=50000,
            km_ultima_manutencao=48000,
            numero_eixos=data['eixos'],
            total_posicoes_pneus=data['posicoes'],
            ano_fabricacao=2020,
        )
        veiculos.append(v)
        print(f"   ✅ {v.placa} - {v.marca} {v.modelo}")
    print()
    
    # Posições de Pneus
    print("📍 Posições de Pneus...")
    total_pos = 0
    for veiculo in veiculos:
        for i in range(1, veiculo.total_posicoes_pneus + 1):
            Position.objects.create(
                veiculo=veiculo,
                eixo=((i-1) // 2) + 1,
                lado='Esquerdo' if i % 2 == 1 else 'Direito',
                tipo='Tração' if i <= 4 else 'Livre',
                posicao=i,
            )
            total_pos += 1
    print(f"   ✅ {total_pos} posições criadas\n")
    
    # Pneus
    print("🛞 Pneus...")
    marcas = ['Michelin', 'Pirelli', 'Goodyear', 'Bridgestone', 'Continental']
    modelos = ['XZA2', 'FG85', 'G159', 'R268', 'HSR2']
    for i in range(1, 51):  # 50 pneus
        Tire.objects.create(
            numero_fogo=f'PN{i:04d}',
            marca=marcas[i % len(marcas)],
            modelo=modelos[i % len(modelos)],
            medida='295/80R22.5',
            tipo='Novo' if i <= 30 else 'Recapado',
            status='Estoque',
            dot=f'2024{i:02d}',
        )
    print(f"   ✅ 50 pneus criados\n")
    
    # Categorias de Produtos
    print("📁 Categorias de Produtos...")
    cats = []
    for nome in ['Pneus', 'Peças', 'Ferramentas', 'EPIs', 'Lubrificantes']:
        c = CategoriaProduto.objects.create(
            nome=nome,
            descricao=f'Categoria {nome}',
        )
        cats.append(c)
    print(f"   ✅ {len(cats)} categorias\n")
    
    # Produtos
    print("📦 Produtos...")
    produtos_data = [
        ('PN001', 'Pneu 295/80R22.5 Michelin XZA2', Decimal('1200.00'), cats[0]),
        ('PN002', 'Pneu 295/80R22.5 Pirelli FG85', Decimal('1150.00'), cats[0]),
        ('PC001', 'Filtro de Óleo', Decimal('45.00'), cats[1]),
        ('PC002', 'Filtro de Ar', Decimal('85.00'), cats[1]),
        ('PC003', 'Pastilha de Freio', Decimal('250.00'), cats[1]),
        ('FR001', 'Chave de Roda', Decimal('120.00'), cats[2]),
        ('FR002', 'Macaco Hidráulico', Decimal('450.00'), cats[2]),
        ('EP001', 'Capacete de Segurança', Decimal('35.00'), cats[3]),
        ('EP002', 'Luvas de Proteção', Decimal('15.00'), cats[3]),
        ('LB001', 'Óleo Motor 15W40', Decimal('180.00'), cats[4]),
    ]
    
    for codigo, nome, preco, cat in produtos_data:
        Produto.objects.create(
            codigo=codigo,
            nome=nome,
            preco_unitario=preco,
            categoria=cat,
            unidade='UN',
        )
    print(f"   ✅ {len(produtos_data)} produtos\n")
    
    # Clientes
    print("👔 Clientes...")
    clientes_data = [
        ('Empresa ABC Ltda', '11122233300014'),
        ('Indústria XYZ S/A', '11144455500017'),
        ('Comércio 123 Eireli', '11177788800015'),
        ('Distribuidora Alfa', '11199900000011'),
        ('Logística Beta', '11122244400018'),
    ]
    
    for nome, cnpj in clientes_data:
        Cliente.objects.create(
            nome=nome,
            cnpj=cnpj,
        )
    print(f"   ✅ {len(clientes_data)} clientes\n")
    
    # Fornecedores
    print("🏭 Fornecedores...")
    fornecedores_data = [
        ('Distribuidora de Pneus Sul', '22233344400015'),
        ('Auto Peças Rápidas', '22255666700018'),
        ('Ferramentas Industriais Ltda', '22288999000011'),
        ('Lubrificantes Premium', '22211122200014'),
        ('EPIs Segurança Total', '22244455500017'),
    ]
    
    for nome, cnpj in fornecedores_data:
        Fornecedor.objects.create(
            nome=nome,
            cnpj=cnpj,
        )
    print(f"   ✅ {len(fornecedores_data)} fornecedores\n")
    
    # Postos de Combustível
    print("⛽ Postos de Combustível...")
    postos_data = [
        ('Posto Shell BR-101 KM 250', '33312312300013'),
        ('Posto Ipiranga Rodovia SP-348', '33345645600016'),
        ('Posto Petrobras BR-116', '33388999000011'),
    ]
    
    postos = []
    for nome, cnpj in postos_data:
        p = PostoCombustivel.objects.create(
            nome=nome,
            cnpj=cnpj,
        )
        postos.append(p)
    print(f"   ✅ {len(postos)} postos\n")
    
    # Abastecimentos
    print("⛽ Abastecimentos...")
    for i, veiculo in enumerate(veiculos, 1):
        for j in range(1, 4):  # 3 abastecimentos por veículo
            Abastecimento.objects.create(
                veiculo=veiculo,
                posto=postos[(i + j) % len(postos)],
                data=date.today() - timedelta(days=j*7),
                litros=Decimal('200.00') + Decimal(j * 10),
                valor_total=Decimal('1200.00') + Decimal(j * 60),
                km_atual=50000 - (j * 500),
                tipo_combustivel='Diesel S10',
            )
    print(f"   ✅ {len(veiculos) * 3} abastecimentos\n")
    
    # Categorias de Custo
    print("💰 Categorias de Custo...")
    cat_custos_data = ['Combustível', 'Manutenção', 'Pneus', 'Pedágio', 'Seguro', 'IPVA']
    cat_custos = []
    for nome in cat_custos_data:
        c = CategoriaCusto.objects.create(
            nome=nome,
            descricao=f'Custos com {nome}',
        )
        cat_custos.append(c)
    print(f"   ✅ {len(cat_custos)} categorias\n")
    
    # Custos
    print("💰 Custos...")
    for i, veiculo in enumerate(veiculos, 1):
        for j, cat in enumerate(cat_custos[:3], 1):  # 3 custos por veículo
            Custo.objects.create(
                veiculo=veiculo,
                categoria=cat,
                data=date.today() - timedelta(days=j*5),
                descricao=f'Custo de {cat.nome} - {veiculo.placa}',
                valor=Decimal('500.00') + Decimal(j * 100),
            )
    print(f"   ✅ {len(veiculos) * 3} custos\n")
    
    # Multas
    print("🚨 Multas...")
    tipos_infracao = [
        'Excesso de velocidade',
        'Ultrapassagem indevida',
        'Estacionamento irregular',
        'Falta de equipamento obrigatório',
    ]
    
    for i, veiculo in enumerate(veiculos[:3], 1):  # 3 veículos com multas
        for j in range(1, 3):  # 2 multas por veículo
            Multa.objects.create(
                numero_auto=f'AUTO{i:03d}{j:03d}',
                veiculo=veiculo,
                data_infracao=date.today() - timedelta(days=j*15),
                tipo_infracao=tipos_infracao[(i + j) % len(tipos_infracao)],
                valor=Decimal('195.23') + Decimal(j * 100),
                pontos=5 + j,
                status='Pendente',
                local_infracao=f'BR-101 KM {100 + i*10}',
            )
    print(f"   ✅ 6 multas\n")
    
    # Viagens
    print("🗺️  Viagens...")
    rotas = [
        ('São Paulo - SP', 'Rio de Janeiro - RJ', 450),
        ('São Paulo - SP', 'Curitiba - PR', 400),
        ('São Paulo - SP', 'Belo Horizonte - MG', 580),
        ('Rio de Janeiro - RJ', 'Belo Horizonte - MG', 430),
        ('Curitiba - PR', 'Florianópolis - SC', 300),
    ]
    
    for i, veiculo in enumerate(veiculos, 1):
        origem, destino, km = rotas[i % len(rotas)]
        for j in range(1, 4):  # 3 viagens por veículo
            data_saida = date.today() - timedelta(days=j*10)
            data_chegada = data_saida + timedelta(days=1)
            
            Viagem.objects.create(
                veiculo=veiculo,
                motorista=motoristas[(i + j) % len(motoristas)],
                origem=origem,
                destino=destino,
                data_saida=data_saida,
                data_chegada=data_chegada,
                km_inicial=50000 - (j * km),
                km_final=50000 - (j * km) + km,
                status='Concluída',
            )
    print(f"   ✅ {len(veiculos) * 3} viagens\n")
    
    print("=" * 80)
    print("✅ SEED CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print("\n📊 Resumo dos Dados Criados:")
    print(f"   • 1 Empresa")
    print(f"   • {len(motoristas)} Motoristas")
    print(f"   • {len(veiculos)} Veículos")
    print(f"   • {total_pos} Posições de Pneus")
    print(f"   • 50 Pneus")
    print(f"   • {len(cats)} Categorias de Produtos")
    print(f"   • {len(produtos_data)} Produtos")
    print(f"   • {len(clientes_data)} Clientes")
    print(f"   • {len(fornecedores_data)} Fornecedores")
    print(f"   • {len(postos)} Postos de Combustível")
    print(f"   • {len(veiculos) * 3} Abastecimentos")
    print(f"   • {len(cat_custos)} Categorias de Custo")
    print(f"   • {len(veiculos) * 3} Custos")
    print(f"   • 6 Multas")
    print(f"   • {len(veiculos) * 3} Viagens")
    print("\n🔑 Credenciais:")
    print("   • admin / admin123")
    print("\n✅ Banco de dados populado e pronto para testes!\n")

if __name__ == '__main__':
    try:
        seed()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
