#!/usr/bin/env python3
"""
Script de seed minimalista - Apenas campos obrigatórios
Uso: python seed_minimal.py
"""
import os, sys, django
from datetime import date
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.empresas.models import Empresa
from backend.transportador.frota.models import Vehicle
from backend.transportador.pneus.models import Tire
from backend.transportador.estoque.models import Produto
from backend.transportador.clientes.models import Cliente
from backend.transportador.fornecedores.models import Fornecedor

def seed():
    print("=" * 80)
    print("SEED MINIMALISTA - XBPNEUS v10.0.5")
    print("=" * 80 + "\n")
    
    # Empresa
    print("📦 Empresa...")
    empresa = Empresa.objects.first()
    if not empresa:
        empresa = Empresa.objects.create(
            cnpj='12345678000190',
            nome='Transportadora XB Pneus',
            tipo='Transportadora'
        )
    print(f"   ✅ {empresa.nome}\n")
    
    # Veículos
    print("🚚 Veículos...")
    placas = ['ABC1234', 'DEF5678', 'GHI9012']
    for placa in placas:
        if not Vehicle.objects.filter(placa=placa).exists():
            Vehicle.objects.create(
                placa=placa,
                modelo='Scania R450',
                tipo='Caminhão',
                status='Ativo',
                km=50000,
                km_ultima_manutencao=48000,
                numero_eixos=3,
                total_posicoes_pneus=10,
            )
            print(f"   ✅ {placa}")
    print()
    
    # Pneus
    print("🛞 Pneus...")
    for i in range(1, 11):
        codigo = f'PN{i:04d}'
        if not Tire.objects.filter(codigo=codigo).exists():
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
    print(f"   ✅ 10 pneus\n")
    
    # Produtos
    print("📦 Produtos...")
    for i in range(1, 6):
        codigo = f'PROD{i:03d}'
        if not Produto.objects.filter(codigo=codigo).exists():
            Produto.objects.create(
                empresa=empresa,
                codigo=codigo,
                codigo_barras=f'789{i:010d}',
                descricao=f'Produto Teste {i}',
                unidade='UN',
                estoque_minimo=10,
                estoque_maximo=100,
                ponto_reposicao=20,
                custo_medio=Decimal('50.00'),
                preco_venda=Decimal('80.00'),
                ncm='12345678',
                localizacao='A1',
                observacoes='Teste',
                ativo=True,
            )
    print(f"   ✅ 5 produtos\n")
    
    # Clientes
    print("👔 Clientes...")
    for i in range(1, 4):
        cpf_cnpj = f'{i:014d}'
        if not Cliente.objects.filter(cpf_cnpj=cpf_cnpj).exists():
            Cliente.objects.create(
                empresa=empresa,
                tipo='PJ',
                cpf_cnpj=cpf_cnpj,
                nome_razao_social=f'Cliente Teste {i} Ltda',
                limite_credito=Decimal('10000.00'),
                prazo_pagamento=30,
                status='Ativo',
            )
    print(f"   ✅ 3 clientes\n")
    
    # Fornecedores
    print("🏭 Fornecedores...")
    for i in range(1, 4):
        cpf_cnpj = f'{i+10:014d}'
        if not Fornecedor.objects.filter(cpf_cnpj=cpf_cnpj).exists():
            Fornecedor.objects.create(
                empresa=empresa,
                tipo='PJ',
                categoria='Pneus',
                cpf_cnpj=cpf_cnpj,
                nome_razao_social=f'Fornecedor Teste {i} Ltda',
                prazo_pagamento=30,
                avaliacao=5,
                status='Ativo',
            )
    print(f"   ✅ 3 fornecedores\n")
    
    print("=" * 80)
    print("✅ SEED CONCLUÍDO!")
    print("=" * 80)
    print("\n📊 Dados Criados:")
    print(f"   • 1 Empresa")
    print(f"   • 3 Veículos")
    print(f"   • 10 Pneus")
    print(f"   • 5 Produtos")
    print(f"   • 3 Clientes")
    print(f"   • 3 Fornecedores")
    print("\n✅ Banco populado!\n")

if __name__ == '__main__':
    try:
        seed()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
