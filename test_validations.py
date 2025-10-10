#!/usr/bin/env python3.11
"""
Script de Teste de Validações - Sistema XBPneus
Testa todas as validações de negócio implementadas
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
EMAIL = "transportador.novo@xbpneus.com"
PASSWORD = "senha123"

def login():
    """Faz login e retorna o token"""
    response = requests.post(
        f"{BASE_URL}/api/transportador/login/",
        json={"email": EMAIL, "password": PASSWORD}
    )
    if response.status_code == 200:
        return response.json()["tokens"]["access"]
    raise Exception(f"Erro no login: {response.text}")

def test_vehicle_validations(token):
    """Testa validações de veículos"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n" + "="*80)
    print("TESTES DE VALIDAÇÃO DE VEÍCULOS")
    print("="*80)
    
    tests = [
        {
            "name": "Placa inválida (formato errado)",
            "data": {
                "placa": "INVALID",
                "modelo": "Teste",
                "marca": "Teste",
                "ano_fabricacao": 2023,
                "ano_modelo": 2023,
                "km": 0,
                "numero_eixos": 3,
                "total_posicoes_pneus": 10,
                "status": "ATIVO"
            },
            "should_fail": True
        },
        {
            "name": "Ano de fabricação futuro",
            "data": {
                "placa": "TST9999",
                "modelo": "Teste",
                "marca": "Teste",
                "ano_fabricacao": 2030,
                "ano_modelo": 2030,
                "km": 0,
                "numero_eixos": 3,
                "total_posicoes_pneus": 10,
                "status": "ATIVO"
            },
            "should_fail": True
        },
        {
            "name": "KM negativo",
            "data": {
                "placa": "TST8888",
                "modelo": "Teste",
                "marca": "Teste",
                "ano_fabricacao": 2023,
                "ano_modelo": 2023,
                "km": -1000,
                "numero_eixos": 3,
                "total_posicoes_pneus": 10,
                "status": "ATIVO"
            },
            "should_fail": True
        },
        {
            "name": "Número de eixos inválido (< 2)",
            "data": {
                "placa": "TST7777",
                "modelo": "Teste",
                "marca": "Teste",
                "ano_fabricacao": 2023,
                "ano_modelo": 2023,
                "km": 0,
                "numero_eixos": 1,
                "total_posicoes_pneus": 10,
                "status": "ATIVO"
            },
            "should_fail": True
        },
        {
            "name": "Veículo válido (placa padrão antigo)",
            "data": {
                "placa": "VAL1234",
                "modelo": "Scania R450",
                "marca": "Scania",
                "ano_fabricacao": 2023,
                "ano_modelo": 2024,
                "km": 50000,
                "numero_eixos": 3,
                "total_posicoes_pneus": 10,
                "status": "ATIVO"
            },
            "should_fail": False
        },
        {
            "name": "Veículo válido (placa Mercosul)",
            "data": {
                "placa": "ABC1D23",
                "modelo": "Volvo FH540",
                "marca": "Volvo",
                "ano_fabricacao": 2024,
                "ano_modelo": 2024,
                "km": 10000,
                "numero_eixos": 3,
                "total_posicoes_pneus": 10,
                "status": "ATIVO"
            },
            "should_fail": False
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        print(f"\n📝 Teste: {test['name']}")
        print(f"   Deve falhar: {'Sim' if test['should_fail'] else 'Não'}")
        
        response = requests.post(
            f"{BASE_URL}/api/transportador/frota/veiculos/",
            json=test["data"],
            headers=headers
        )
        
        if test["should_fail"]:
            if response.status_code == 400:
                print(f"   ✅ PASSOU - Validação funcionou corretamente")
                print(f"   Erro retornado: {response.json()}")
                passed += 1
            else:
                print(f"   ❌ FALHOU - Deveria ter rejeitado (Status: {response.status_code})")
                failed += 1
        else:
            if response.status_code == 201:
                print(f"   ✅ PASSOU - Veículo criado com sucesso")
                passed += 1
            else:
                print(f"   ❌ FALHOU - Deveria ter aceito (Status: {response.status_code})")
                print(f"   Erro: {response.json()}")
                failed += 1
    
    print(f"\n{'='*80}")
    print(f"Resultado: {passed} passou, {failed} falhou de {len(tests)} testes")
    print(f"{'='*80}")
    
    return passed, failed

def test_tire_validations(token):
    """Testa validações de pneus"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n" + "="*80)
    print("TESTES DE VALIDAÇÃO DE PNEUS")
    print("="*80)
    
    tests = [
        {
            "name": "Medida inválida (formato errado)",
            "data": {
                "codigo": "TEST001",
                "medida": "INVALID",
                "dot": "2523",
                "status": "ESTOQUE"
            },
            "should_fail": True
        },
        {
            "name": "Código muito curto",
            "data": {
                "codigo": "AB",
                "medida": "295/80R22.5",
                "dot": "2523",
                "status": "ESTOQUE"
            },
            "should_fail": True
        },
        {
            "name": "Número de recapagens muito alto",
            "data": {
                "codigo": "TEST002",
                "medida": "295/80R22.5",
                "dot": "2523",
                "numero_recapagens": 10,
                "status": "ESTOQUE"
            },
            "should_fail": True
        },
        {
            "name": "Pneu válido",
            "data": {
                "codigo": "VALID001",
                "medida": "295/80R22.5",
                "dot": "2523",
                "marca": "Michelin",
                "modelo": "XZA",
                "tipo": "NOVO",
                "numero_recapagens": 0,
                "status": "ESTOQUE"
            },
            "should_fail": False
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        print(f"\n📝 Teste: {test['name']}")
        print(f"   Deve falhar: {'Sim' if test['should_fail'] else 'Não'}")
        
        response = requests.post(
            f"{BASE_URL}/api/transportador/pneus/pneus/",
            json=test["data"],
            headers=headers
        )
        
        if test["should_fail"]:
            if response.status_code == 400:
                print(f"   ✅ PASSOU - Validação funcionou corretamente")
                print(f"   Erro retornado: {response.json()}")
                passed += 1
            else:
                print(f"   ❌ FALHOU - Deveria ter rejeitado (Status: {response.status_code})")
                failed += 1
        else:
            if response.status_code == 201:
                print(f"   ✅ PASSOU - Pneu criado com sucesso")
                passed += 1
            else:
                print(f"   ❌ FALHOU - Deveria ter aceito (Status: {response.status_code})")
                print(f"   Erro: {response.json()}")
                failed += 1
    
    print(f"\n{'='*80}")
    print(f"Resultado: {passed} passou, {failed} falhou de {len(tests)} testes")
    print(f"{'='*80}")
    
    return passed, failed

def main():
    print("\n" + "="*80)
    print("SISTEMA XBPNEUS - TESTE DE VALIDAÇÕES DE NEGÓCIO")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Servidor: {BASE_URL}")
    
    try:
        # Login
        print("\n🔐 Fazendo login...")
        token = login()
        print("✅ Login realizado com sucesso!")
        
        # Testes de veículos
        vehicle_passed, vehicle_failed = test_vehicle_validations(token)
        
        # Testes de pneus
        tire_passed, tire_failed = test_tire_validations(token)
        
        # Resultado final
        total_passed = vehicle_passed + tire_passed
        total_failed = vehicle_failed + tire_failed
        total_tests = total_passed + total_failed
        
        print("\n" + "="*80)
        print("RESULTADO FINAL")
        print("="*80)
        print(f"Total de testes: {total_tests}")
        print(f"✅ Passou: {total_passed}")
        print(f"❌ Falhou: {total_failed}")
        print(f"Taxa de sucesso: {(total_passed/total_tests*100):.1f}%")
        print("="*80)
        
        if total_failed == 0:
            print("\n🎉 TODAS AS VALIDAÇÕES ESTÃO FUNCIONANDO PERFEITAMENTE!")
        else:
            print(f"\n⚠️  {total_failed} teste(s) falharam. Revise as validações.")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return 1
    
    return 0 if total_failed == 0 else 1

if __name__ == "__main__":
    exit(main())

