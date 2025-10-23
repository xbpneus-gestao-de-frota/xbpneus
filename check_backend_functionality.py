
import requests

def check_backend_endpoints():
    endpoints = [
        "http://localhost:8000/api/schema/swagger/",
        "http://localhost:8000/api/create/",
        "http://localhost:8000/api/run/",
        "http://localhost:8000/api/show/",
        "http://localhost:8000/api/make/",
        "http://localhost:8000/api/schema/",
        "http://localhost:8000/api/docs/",
        "http://localhost:8000/api/token/",
        "http://localhost:8000/api/token/refresh/",
        "http://localhost:8000/api/token/verify/",
        "http://localhost:8000/api/auth/logout/",
        "http://localhost:8000/api/auth/me/",
        "http://localhost:8000/api/users/register_full/",
        "http://localhost:8000/api/approve/",
        "http://localhost:8000/api/transportador/",
        "http://localhost:8000/api/motorista/",
        "http://localhost:8000/api/borracharia/",
        "http://localhost:8000/api/revenda/",
        "http://localhost:8000/api/recapagem/",
        "http://localhost:8000/api/transportador/motorista/",
        "http://localhost:8000/api/transportador/frota/",
        "http://localhost:8000/api/transportador/pneus/",
        "http://localhost:8000/api/transportador/manutencao/",
        "http://localhost:8000/api/transportador/estoque/",
        "http://localhost:8000/api/transportador/loja/",
        "http://localhost:8000/api/transportador/custos/",
        "http://localhost:8000/api/transportador/combustivel/",
        "http://localhost:8000/api/transportador/multas/",
        "http://localhost:8000/api/transportador/documentos/",
        "http://localhost:8000/api/transportador/viagens/",
        "http://localhost:8000/api/transportador/clientes/",
        "http://localhost:8000/api/transportador/fornecedores/",
        "http://localhost:8000/api/transportador/seguros/",
        "http://localhost:8000/api/transportador/contratos/",
        "http://localhost:8000/api/transportador/faturamento/",
        "http://localhost:8000/api/transportador/pagamentos/",
        "http://localhost:8000/api/transportador/telemetria/",
        "http://localhost:8000/api/transportador/rastreamento/",
        "http://localhost:8000/api/transportador/rotas/",
        "http://localhost:8000/api/transportador/entregas/",
        "http://localhost:8000/api/transportador/dashboards/",
        "http://localhost:8000/api/transportador/notificacoes/",
        "http://localhost:8000/api/transportador/almoxarifado/",
        "http://localhost:8000/api/transportador/relatorios/",
        "http://localhost:8000/api/transportador/cargas/",
        "http://localhost:8000/api/transportador/pecas/",
        "http://localhost:8000/api/transportador/ferramentas/",
        "http://localhost:8000/api/transportador/epis/",
        "http://localhost:8000/api/transportador/treinamentos/",
        "http://localhost:8000/api/transportador/compliance/",
        "http://localhost:8000/api/transportador/alertas/",
        "http://localhost:8000/api/transportador/integracoes/",
        "http://localhost:8000/api/transportador/configuracoes/",
        "http://localhost:8000/api/transportador/empresas/",
        "http://localhost:8000/api/transportador/financeiro/",
        "http://localhost:8000/api/transportador/motorista/",
        "http://localhost:8000/api/transportador/relatorios_transportador/",
        "http://localhost:8000/api/transportador/tr/",
        "http://localhost:8000/api/transportador/implemento/",
        "http://localhost:8000/api/transportador/analise_pneus/",
        "http://localhost:8000/api/transportador/garantias/",
        "http://localhost:8000/api/transportador/auditoria/",
        "http://localhost:8000/api/transportador/notas_fiscais/",
        "http://localhost:8000/api/transportador/ia/",
        "http://localhost:8000/api/reports/",
        "http://localhost:8000/api/jobs/"
    ]

    print("\n--- Verificação de Funcionalidades de Backend ---")
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print(f"[OK] {endpoint} - Status: {response.status_code}")
            else:
                print(f"[ERRO] {endpoint} - Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"[ERRO] {endpoint} - Não foi possível conectar ao endpoint.")
        except Exception as e:
            print(f"[ERRO] {endpoint} - Erro inesperado: {e}")

if __name__ == "__main__":
    check_backend_endpoints()

