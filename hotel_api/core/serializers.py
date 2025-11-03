from rest_framework import serializers

from .models import Hotel, Quarto, Reserva
from .enums import QuartoSituacao, QuartoTipo, QuartoMotivoIndisponivel, ReservaSituacao


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            "id",
            "nome",
            "endereco",
            "telefone",
            "email",
            "descricao",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]


class QuartoSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=False)

    class Meta:
        model = Quarto
        fields = [
            "id",
            "hotel",
            "numero",
            "tipo",
            "preco_diario",
            "situacao",
            "motivo_indisponivel",
            "ar_condicionado",
            "beliche",
            "qtd_cama_casal",
            "qtd_cama_solteiro",
            "tv",
            "wifi",
            "lavanderia",
            "frigobar",
            "varanda",
            "banheiro_privativo",
            "secador_cabelo",
            "cofre",
            "escritorio",
            "acessibilidade",
            "microondas",
            "aquecedor",
            "telefone",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]

    def validate(self, attrs):
        situacao = attrs.get("situacao", getattr(self.instance, "situacao", None))
        motivo = attrs.get("motivo_indisponivel", getattr(self.instance, "motivo_indisponivel", None))
        if situacao == QuartoSituacao.DISPONIVEL and motivo:
            raise serializers.ValidationError("motivo_indisponivel deve ser vazio quando situacao=disponivel.")
        return attrs


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = [
            "id",
            "codigo",
            "cliente",
            "quarto",
            "data_checkin",
            "data_checkout",
            "situacao",
            "valor_total",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]

    def validate(self, attrs):
        checkin = attrs.get("data_checkin", getattr(self.instance, "data_checkin", None))
        checkout = attrs.get("data_checkout", getattr(self.instance, "data_checkout", None))
        if checkin and checkout and checkout <= checkin:
            raise serializers.ValidationError("data_checkout deve ser maior que data_checkin.")
        return attrs

