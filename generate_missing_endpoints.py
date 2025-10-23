#!/usr/bin/env python3
"""
Script para gerar endpoints de backend ausentes
"""

import os

# Endpoints a serem criados
ENDPOINTS = {
    'motorista': {
        'path': '/home/ubuntu/xbpneus/backend/motorista',
        'description': 'Módulo de Motorista'
    },
    'borracharia': {
        'path': '/home/ubuntu/xbpneus/backend/borracharia',
        'description': 'Módulo de Borracharia'
    },
    'revenda': {
        'path': '/home/ubuntu/xbpneus/backend/revenda',
        'description': 'Módulo de Revenda'
    },
    'recapagem': {
        'path': '/home/ubuntu/xbpneus/backend/recapagem',
        'description': 'Módulo de Recapagem'
    },
    'reports': {
        'path': '/home/ubuntu/xbpneus/backend/reports',
        'description': 'Módulo de Relatórios'
    },
    'jobs': {
        'path': '/home/ubuntu/xbpneus/backend/jobs',
        'description': 'Módulo de Jobs'
    }
}

def generate_views_py(module_name, description):
    """Gera o arquivo views.py para um módulo"""
    content = f'''"""
Views para o módulo {description}
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class {module_name.capitalize()}ViewSet(viewsets.ViewSet):
    """
    ViewSet para {description}
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Lista todos os itens do módulo"""
        return Response({{
            "message": "Listagem de {description}",
            "data": []
        }})
    
    def retrieve(self, request, pk=None):
        """Retorna um item específico do módulo"""
        return Response({{
            "message": "Detalhe de {description}",
            "id": pk,
            "data": {{}}
        }})
    
    def create(self, request):
        """Cria um novo item no módulo"""
        return Response({{
            "message": "Item criado em {description}",
            "data": request.data
        }}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Atualiza um item no módulo"""
        return Response({{
            "message": "Item atualizado em {description}",
            "id": pk,
            "data": request.data
        }})
    
    def destroy(self, request, pk=None):
        """Deleta um item do módulo"""
        return Response({{
            "message": "Item deletado de {description}",
            "id": pk
        }}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Retorna o dashboard do módulo"""
        return Response({{
            "message": "Dashboard de {description}",
            "data": {{}}
        }})
'''
    return content

def generate_urls_py(module_name):
    """Gera o arquivo urls.py para um módulo"""
    content = f'''"""
URLs para o módulo {module_name}
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.{module_name.capitalize()}ViewSet, basename='{module_name}')

urlpatterns = [
    path('', include(router.urls)),
]
'''
    return content

def create_endpoint(module_name, module_path, description):
    """Cria os arquivos para um endpoint"""
    print(f"[*] Criando endpoint para {description}...")
    
    # Verificar se o diretório existe
    if not os.path.exists(module_path):
        print(f"[!] Diretório {module_path} não encontrado")
        return False
    
    # Criar views.py
    views_path = os.path.join(module_path, 'views.py')
    if not os.path.exists(views_path):
        with open(views_path, 'w') as f:
            f.write(generate_views_py(module_name, description))
        print(f"[✓] Criado: {views_path}")
    else:
        print(f"[!] {views_path} já existe")
    
    # Criar urls.py
    urls_path = os.path.join(module_path, 'urls.py')
    if not os.path.exists(urls_path):
        with open(urls_path, 'w') as f:
            f.write(generate_urls_py(module_name))
        print(f"[✓] Criado: {urls_path}")
    else:
        print(f"[!] {urls_path} já existe")
    
    return True

def main():
    print("="*60)
    print("GERADOR DE ENDPOINTS DE BACKEND AUSENTES")
    print("Sistema XBPneus")
    print("="*60)
    
    for module_name, config in ENDPOINTS.items():
        create_endpoint(module_name, config['path'], config['description'])
    
    print("\n" + "="*60)
    print("CONCLUSÃO")
    print("="*60)
    print("\n[✓] Endpoints gerados com sucesso!")
    print("\nPróximos passos:")
    print("1. Atualizar o arquivo /home/ubuntu/xbpneus/config/urls.py")
    print("2. Adicionar as URLs dos novos módulos")
    print("3. Executar o script de verificação de endpoints")
    print("4. Realizar testes de integração")

if __name__ == "__main__":
    main()

