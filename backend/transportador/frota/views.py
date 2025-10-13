from rest_framework import viewsets, permissions, filters
from backend.common.permissions import OptionalRolePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.common.audit import AuditedModelViewSet
from backend.common.export import export_csv, export_xlsx, export_csv_streaming
from .models import Vehicle, Position
from .serializers import VehicleSerializer, PositionSerializer

class VehicleViewSet(AuditedModelViewSet):
    queryset = Vehicle.objects.select_related('empresa', 'filial').all().order_by("id")
    serializer_class = VehicleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'placa', 'modelo', 'marca', 'chassi']
    ordering_fields = ['id', 'placa', 'modelo', 'km']
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['placa', 'modelo', 'motorista', 'empresa', 'filial', 'tipo', 'status']

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        fmt = request.query_params.get("format", "csv")
        qs = self.filter_queryset(self.get_queryset())
        fields = ['id', 'placa', 'modelo', 'km', 'motorista']
        filename = f"vehicleviewset." + ("xlsx" if fmt == "xlsx" else "csv")
        if fmt == "xlsx":
            return export_xlsx(qs, fields, filename=filename)
        return export_csv_streaming(qs, fields, filename=filename) if request.query_params.get("stream") in {"1","true","True"} else export_csv(qs, fields, filename=filename)
class PositionViewSet(AuditedModelViewSet):
    queryset = Position.objects.all().order_by("id")
    serializer_class = PositionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['veiculo','posicao','medida']
