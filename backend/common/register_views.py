from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backend.transportador.models import UsuarioTransportador
from backend.motorista.models import UsuarioMotorista
from backend.borracharia.models import UsuarioBorracharia
from backend.revenda.models import UsuarioRevenda
from backend.recapagem.models import UsuarioRecapagem
from backend.transportador.motorista_externo.models import MotoristaExterno
from django.contrib.auth import get_user_model

@api_view(["POST"])
@permission_classes([AllowAny])
def register_full_view(request):
    tipo_usuario = request.data.get("tipo_usuario")
    
    if not tipo_usuario:
        return Response({
            "error": "Tipo de usuário é obrigatório",
            "tipos_validos": ["transportador", "motorista", "motorista_externo", "borracharia", "revenda", "recapagem"]
        }, status=status.HTTP_400_BAD_REQUEST)
    
    tipo_usuario = tipo_usuario.lower()
    
    tipo_map = {
        "transportador": {
            "model": UsuarioTransportador,
            "required_fields": ["email", "password", "nome_razao_social", "cnpj", "telefone"],
            "unique_fields": {"cnpj": "CNPJ já cadastrado"}
        },
        "motorista": {
            "model": UsuarioMotorista,
            "required_fields": ["email", "password", "nome_completo", "cpf", "cnh", "categoria_cnh", "telefone"],
            "unique_fields": {"cpf": "CPF já cadastrado", "cnh": "CNH já cadastrada"}
        },
        "motorista_externo": {
            "model": MotoristaExterno,
            "required_fields": ["email", "password", "nome_completo", "cpf", "cnh", "telefone"],
            "optional_fields": ["cnpj"],
            "unique_fields": {"cpf": "CPF já cadastrado", "cnh": "CNH já cadastrada", "cnpj": "CNPJ já cadastrado"}
        },
        "borracharia": {
            "model": UsuarioBorracharia,
            "required_fields": ["email", "password", "nome_razao_social", "cnpj", "telefone"],
            "unique_fields": {"cnpj": "CNPJ já cadastrado"}
        },
        "revenda": {
            "model": UsuarioRevenda,
            "required_fields": ["email", "password", "nome_razao_social", "cnpj", "telefone"],
            "unique_fields": {"cnpj": "CNPJ já cadastrado"}
        },
        "recapagem": {
            "model": UsuarioRecapagem,
            "required_fields": ["email", "password", "nome_razao_social", "cnpj", "telefone"],
            "unique_fields": {"cnpj": "CNPJ já cadastrado"}
        }
    }
    
    if tipo_usuario not in tipo_map:
        return Response({
            "error": f"Tipo de usuário inválido: {tipo_usuario}",
            "tipos_validos": list(tipo_map.keys())
        }, status=status.HTTP_400_BAD_REQUEST)
    
    config = tipo_map[tipo_usuario]
    model = config["model"]
    required_fields = config["required_fields"]
    optional_fields = config.get("optional_fields", [])
    unique_fields = config.get("unique_fields", {})
    
    missing_fields = []
    for field in required_fields:
        if field not in request.data or not request.data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return Response({
            "error": "Campos obrigatórios faltando",
            "campos_faltando": missing_fields
        }, status=status.HTTP_400_BAD_REQUEST)
    
    User = get_user_model()
    if User.objects.filter(email=request.data.get("email")).exists():
        return Response({
            "error": "Email já cadastrado"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Refatorar a lógica de verificação de campos únicos para ser mais específica
    for field, error_message in unique_fields.items():
        if field in request.data and request.data[field]: # Apenas verificar se o campo foi fornecido e não está vazio
            # Usar o modelo específico do perfil para a verificação de unicidade
            if model.objects.filter(**{field: request.data[field]}).exists():
                return Response({
                    "error": error_message
                }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(
            email=request.data["email"],
            password=request.data["password"],
            is_active=False
        )

        profile_data = {}
        for field in required_fields:
            if field not in ["email", "password"]:
                profile_data[field] = request.data[field]
        
        for field in optional_fields:
            if field in request.data and request.data[field]:
                profile_data[field] = request.data[field]

        optional_profile_fields = ["endereco", "cidade", "estado", "cep", "empresa", "filial", "categoria_cnh"]
        for field in optional_profile_fields:
            if field in request.data:
                profile_data[field] = request.data[field]
        
        profile_data["usuario"] = user

        model.objects.create(**profile_data)
        
        return Response({
            "message": "Cadastro realizado com sucesso! Aguarde aprovação do administrador.",
            "user": {
                "id": user.id,
                "email": user.email,
                "tipo_usuario": tipo_usuario,
                "aprovado": (MotoristaExterno.objects.get(usuario=user).aprovado if tipo_usuario == "motorista_externo" else user.is_active),
                "is_active": user.is_active
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        if "user" in locals() and user.pk:
            user.delete()
        return Response({
            "error": f"Erro ao criar usuário: {str(e)}"
        }, status=status.HTTP_400_BAD_REQUEST)

