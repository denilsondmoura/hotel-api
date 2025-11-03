from django.conf import settings
from django.db import models
from .enums import (
    QuartoTipo,
    QuartoSituacao,
    QuartoMotivoIndisponivel,
    ReservaSituacao,
)


class Hotel(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=32)
    email = models.EmailField(max_length=255)
    descricao = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="hotels_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="hotels_updated",
    )

    def __str__(self) -> str:
        return self.nome


class Quarto(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="quartos")
    numero = models.CharField(max_length=32)
    tipo = models.CharField(max_length=16, choices=QuartoTipo.choices)
    preco_diario = models.DecimalField(max_digits=10, decimal_places=2)
    situacao = models.CharField(max_length=16, choices=QuartoSituacao.choices, default=QuartoSituacao.DISPONIVEL)
    motivo_indisponivel = models.CharField(
        max_length=32,
        choices=QuartoMotivoIndisponivel.choices,
        null=True,
        blank=True,
    )

    ar_condicionado = models.BooleanField(default=False)
    beliche = models.BooleanField(default=False)
    qtd_cama_casal = models.PositiveIntegerField(default=0)
    qtd_cama_solteiro = models.PositiveIntegerField(default=0)
    tv = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    lavanderia = models.BooleanField(default=False)
    frigobar = models.BooleanField(default=False)
    varanda = models.BooleanField(default=False)
    banheiro_privativo = models.BooleanField(default=True)
    secador_cabelo = models.BooleanField(default=False)
    cofre = models.BooleanField(default=False)
    escritorio = models.BooleanField(default=False)
    acessibilidade = models.BooleanField(default=False)
    microondas = models.BooleanField(default=False)
    aquecedor = models.BooleanField(default=False)
    telefone = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms_updated",
    )

    def __str__(self) -> str:
        return f"{self.hotel.nome} - Quarto {self.numero}"


import uuid

class Reserva(models.Model):
    codigo = models.CharField(max_length=32, unique=True, blank=True)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="minhas_reservas",
    )
    quarto = models.ForeignKey(Quarto, on_delete=models.PROTECT, related_name="reservas")
    data_checkin = models.DateField()
    data_checkout = models.DateField()
    situacao = models.CharField(max_length=16, choices=ReservaSituacao.choices, default=ReservaSituacao.PENDENTE)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings_updated",
    )

    def save(self, *args, **kwargs):
        if not self.codigo:
            while True:
                codigo = uuid.uuid4().hex[:12].upper()
                if not Reserva.objects.filter(codigo=codigo).exists():
                    self.codigo = codigo
                    break
                
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Reserva {self.codigo} - {self.cliente}"

