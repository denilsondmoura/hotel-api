from django.db import models


class QuartoTipo(models.TextChoices):
    STANDARD = "standard", "standard"
    LUXO = "luxo", "luxo"
    SUITE = "suíte", "suíte"


class QuartoSituacao(models.TextChoices):
    DISPONIVEL = "disponivel", "disponivel"
    INDISPONIVEL = "indisponivel", "indisponivel"


class QuartoMotivoIndisponivel(models.TextChoices):
    MANUTENCAO = "manutencao", "manutencao"
    LIMPEZA_PROFUNDA = "limpeza_profunda", "limpeza_profunda"


class ReservaSituacao(models.TextChoices):
    PENDENTE = "pendente", "pendente"
    CONFIRMADA = "confirmada", "confirmada"
    CANCELADA = "cancelada", "cancelada"
    FINALIZADA = "finalizada", "finalizada"

