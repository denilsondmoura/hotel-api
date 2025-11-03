from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Reserva
    from django.contrib.auth.models import AbstractBaseUser


class SituacaoReserva(ABC):

    @abstractmethod
    def cancelar(self, reserva: "Reserva", user: "AbstractBaseUser") -> "Reserva":
        raise NotImplementedError

    @abstractmethod
    def checkin(self, reserva: "Reserva", user: "AbstractBaseUser") -> "Reserva":
        raise NotImplementedError

    @abstractmethod
    def checkout(self, reserva: "Reserva", user: "AbstractBaseUser") -> "Reserva":
        raise NotImplementedError

    def _atualizar(self, reserva: "Reserva", *, situacao: str, user: "AbstractBaseUser") -> "Reserva":
        reserva.situacao = situacao
        reserva.updated_by = user
        reserva.save(update_fields=["situacao", "updated_by", "updated_at"])
        return reserva

