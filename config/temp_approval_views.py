from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from backend.transportador.motorista_externo.models import MotoristaExterno

@api_view(["POST"])
@permission_classes([IsAdminUser])
def approve_motorista_externo(request, user_id):
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if not hasattr(user, 'motorista_externo_perfil'):
        return Response({"detail": "Usuário não é um motorista externo."}, status=status.HTTP_400_BAD_REQUEST)

    motorista_externo = user.motorista_externo_perfil
    motorista_externo.aprovado = True
    motorista_externo.save()
    user.is_active = True # Ativar o usuário Django também
    user.save()

    return Response({"detail": "Motorista externo aprovado com sucesso.", "user_id": user_id, "aprovado": True}, status=status.HTTP_200_OK)

