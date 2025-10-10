#!/usr/bin/env python3
"""
Script Auxiliar - Aprovação Automática de Usuários
Sistema XBPNEUS v10

Este script aprova automaticamente usuários pendentes no Django Admin.
Deve ser executado com o Django shell ou manage.py.
"""

import os
import sys
import django

# Configura Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def approve_user_by_email(email: str, user_type: str) -> bool:
    """
    Aprova um usuário específico por email
    
    Args:
        email: Email do usuário
        user_type: Tipo do usuário (transportador, motorista, borracharia, revenda, recapagem)
    
    Returns:
        bool: True se aprovado com sucesso, False caso contrário
    """
    try:
        if user_type == "transportador":
            from backend.transportador.models import UsuarioTransportador
            user = UsuarioTransportador.objects.get(email=email)
        elif user_type == "motorista":
            from backend.motorista.models import UsuarioMotorista
            user = UsuarioMotorista.objects.get(email=email)
        elif user_type == "borracharia":
            from backend.borracharia.models import UsuarioBorracharia
            user = UsuarioBorracharia.objects.get(email=email)
        elif user_type == "revenda":
            from backend.revenda.models import UsuarioRevenda
            user = UsuarioRevenda.objects.get(email=email)
        elif user_type == "recapagem":
            from backend.recapagem.models import UsuarioRecapagem
            user = UsuarioRecapagem.objects.get(email=email)
        else:
            print(f"❌ Tipo de usuário inválido: {user_type}")
            return False
        
        # Aprova o usuário
        user.aprovado = True
        user.is_active = True
        user.save()
        
        print(f"✅ Usuário {email} ({user_type}) aprovado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao aprovar usuário {email}: {e}")
        return False

def approve_all_pending_users():
    """Aprova todos os usuários pendentes de todos os tipos"""
    
    approved_count = 0
    failed_count = 0
    
    # Lista de modelos de usuário
    user_models = [
        ("transportador", "backend.transportador.models", "UsuarioTransportador"),
        ("motorista", "backend.motorista.models", "UsuarioMotorista"),
        ("borracharia", "backend.borracharia.models", "UsuarioBorracharia"),
        ("revenda", "backend.revenda.models", "UsuarioRevenda"),
        ("recapagem", "backend.recapagem.models", "UsuarioRecapagem"),
    ]
    
    print("🔍 Procurando usuários pendentes...\n")
    
    for user_type, module_path, model_name in user_models:
        try:
            # Importa o modelo dinamicamente
            module = __import__(module_path, fromlist=[model_name])
            UserModel = getattr(module, model_name)
            
            # Busca usuários pendentes
            pending_users = UserModel.objects.filter(aprovado=False)
            
            if pending_users.exists():
                print(f"\n📋 {user_type.upper()}: {pending_users.count()} usuário(s) pendente(s)")
                
                for user in pending_users:
                    try:
                        user.aprovado = True
                        user.is_active = True
                        user.save()
                        
                        email = getattr(user, 'email', 'N/A')
                        name = getattr(user, 'nome_razao_social', None) or getattr(user, 'nome_completo', 'N/A')
                        
                        print(f"  ✅ Aprovado: {email} - {name}")
                        approved_count += 1
                        
                    except Exception as e:
                        print(f"  ❌ Erro ao aprovar: {e}")
                        failed_count += 1
            else:
                print(f"✓ {user_type.upper()}: Nenhum usuário pendente")
                
        except Exception as e:
            print(f"❌ Erro ao processar {user_type}: {e}")
            failed_count += 1
    
    # Resumo
    print(f"\n{'='*60}")
    print(f"📊 RESUMO")
    print(f"{'='*60}")
    print(f"✅ Aprovados: {approved_count}")
    print(f"❌ Falhas: {failed_count}")
    print(f"{'='*60}\n")
    
    return approved_count, failed_count

def list_all_users():
    """Lista todos os usuários de todos os tipos"""
    
    user_models = [
        ("transportador", "backend.transportador.models", "UsuarioTransportador"),
        ("motorista", "backend.motorista.models", "UsuarioMotorista"),
        ("borracharia", "backend.borracharia.models", "UsuarioBorracharia"),
        ("revenda", "backend.revenda.models", "UsuarioRevenda"),
        ("recapagem", "backend.recapagem.models", "UsuarioRecapagem"),
    ]
    
    print("\n📋 LISTA DE TODOS OS USUÁRIOS\n")
    
    for user_type, module_path, model_name in user_models:
        try:
            module = __import__(module_path, fromlist=[model_name])
            UserModel = getattr(module, model_name)
            
            users = UserModel.objects.all()
            
            if users.exists():
                print(f"\n{user_type.upper()} ({users.count()} usuário(s)):")
                print("-" * 80)
                
                for user in users:
                    email = getattr(user, 'email', 'N/A')
                    name = getattr(user, 'nome_razao_social', None) or getattr(user, 'nome_completo', 'N/A')
                    aprovado = "✅" if user.aprovado else "⏳"
                    ativo = "✅" if user.is_active else "❌"
                    
                    print(f"  {aprovado} {email}")
                    print(f"     Nome: {name}")
                    print(f"     Aprovado: {user.aprovado} | Ativo: {user.is_active}")
                    print()
            else:
                print(f"\n{user_type.upper()}: Nenhum usuário cadastrado")
                
        except Exception as e:
            print(f"\n❌ Erro ao listar {user_type}: {e}")

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Aprovação de usuários XBPNEUS")
    parser.add_argument("--email", help="Email do usuário para aprovar")
    parser.add_argument("--type", help="Tipo do usuário (transportador, motorista, borracharia, revenda, recapagem)")
    parser.add_argument("--all", action="store_true", help="Aprovar todos os usuários pendentes")
    parser.add_argument("--list", action="store_true", help="Listar todos os usuários")
    
    args = parser.parse_args()
    
    if args.list:
        list_all_users()
    elif args.all:
        approve_all_pending_users()
    elif args.email and args.type:
        approve_user_by_email(args.email, args.type)
    else:
        print("Uso:")
        print("  python approve_users.py --list                              # Lista todos os usuários")
        print("  python approve_users.py --all                               # Aprova todos pendentes")
        print("  python approve_users.py --email user@example.com --type transportador")

if __name__ == "__main__":
    main()

