from rest_framework import viewsets, mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Hotel, Quarto, Reserva
from .serializers import HotelSerializer, QuartoSerializer, ReservaSerializer
from .enums import QuartoSituacao, ReservaSituacao
from .states import get_reserva_state
from .tasks import encaminha_email_confirmacao_reserva_task


class IsAdminGroupPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return super().has_permission(request, view)
        
        user = request.user
        if not (super().has_permission(request, view) and user.groups.filter(name="ADMINISTRADOR").exists()):
            return False
        
        return True


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all().order_by("id")
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, IsAdminGroupPermission]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


@extend_schema_view(
    list=extend_schema(tags=["quartos"]),
    retrieve=extend_schema(tags=["quartos"]),
    create=extend_schema(tags=["quartos"]),
    partial_update=extend_schema(tags=["quartos"]),
    destroy=extend_schema(tags=["quartos"]),
)
class QuartoViewSet(viewsets.ModelViewSet):
    serializer_class = QuartoSerializer
    permission_classes = [IsAuthenticated, IsAdminGroupPermission]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]


    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_id")
        qs = Quarto.objects.all().order_by("id")
        if hotel_id:
            qs = qs.filter(hotel_id=hotel_id)

        situacao = self.request.query_params.get("situacao")
        tipo = self.request.query_params.get("tipo")
        if situacao:
            qs = qs.filter(situacao=situacao)
            
        if tipo:
            qs = qs.filter(tipo=tipo)
            
        return qs


    def perform_create(self, serializer):
        hotel_id = self.kwargs.get("hotel_id")
        serializer.save(
            hotel_id=hotel_id,
            created_by=self.request.user,
            updated_by=self.request.user,
        )


    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all().order_by("id")
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def perform_create(self, serializer):
        from .enums import QuartoSituacao
        
        attrs = serializer.validated_data

        data_checkin = attrs.get("data_checkin")
        data_checkout = attrs.get("data_checkout")
        quarto = attrs.get("quarto")
        valor_total = attrs.get("valor_total")

        if not data_checkin or not data_checkout or not quarto:
            raise serializers.ValidationError("data_checkin, data_checkout e quarto são obrigatórios.")

        dias = (data_checkout - data_checkin).days
        if dias <= 0:
            raise serializers.ValidationError("data_checkout deve ser maior que data_checkin.")

        if hasattr(quarto, "situacao") and hasattr(quarto.__class__, "QuartoSituacao"):
            
            if quarto.situacao != QuartoSituacao.DISPONIVEL:
                raise serializers.ValidationError("O quarto selecionado não está disponível.")
            
        elif hasattr(quarto, "situacao"):
            if str(quarto.situacao) != "disponivel":
                raise serializers.ValidationError("O quarto selecionado não está disponível.")

        conflitos = quarto.reservas.filter(
            data_checkout__gt=data_checkin,
            data_checkin__lt=data_checkout,
        )
        if conflitos.exists():
            raise serializers.ValidationError("O quarto já está reservado no intervalo de datas escolhido.")

        valor_calculado = dias * quarto.preco_diario
        if valor_total != valor_calculado:
            raise serializers.ValidationError(f"valor_total inválido. Esperado: R${valor_calculado}")
            
        reserva = serializer.save(
            cliente=self.request.user,
            created_by=self.request.user,
            updated_by=self.request.user,
            valor_total=valor_calculado
        )
        
        encaminha_email_confirmacao_reserva_task.delay(reserva.id)
        

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


    @action(detail=True, methods=["patch"])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        try:
            state = get_reserva_state(reserva.situacao)
            updated = state.cancelar(reserva, request.user)
            return Response(self.get_serializer(updated).data)
        
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["patch"])
    def checkin(self, request, pk=None):
        reserva = self.get_object()
        try:
            state = get_reserva_state(reserva.situacao)
            updated = state.checkin(reserva, request.user)
            return Response(self.get_serializer(updated).data)
        
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["patch"])
    def checkout(self, request, pk=None):
        reserva = self.get_object()
        try:
            state = get_reserva_state(reserva.situacao)
            updated = state.checkout(reserva, request.user)
            return Response(self.get_serializer(updated).data)
        
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

