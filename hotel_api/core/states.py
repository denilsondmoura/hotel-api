from typing import Callable

from .contracts import SituacaoReserva
from .enums import ReservaSituacao


class ReservaPendente(SituacaoReserva):
    def cancelar(self, reserva, user):
        return self._atualizar(reserva, situacao=ReservaSituacao.CANCELADA, user=user)

    def checkin(self, reserva, user):
        return self._atualizar(reserva, situacao=ReservaSituacao.CONFIRMADA, user=user)

    def checkout(self, reserva, user):
        raise ValueError("Não é possível fazer checkout de uma reserva pendente.")


class ReservaConfirmada(SituacaoReserva):
    def cancelar(self, reserva, user):
        return self._atualizar(reserva, situacao=ReservaSituacao.CANCELADA, user=user)

    def checkin(self, reserva, user):
        return reserva

    def checkout(self, reserva, user):
        return self._atualizar(reserva, situacao=ReservaSituacao.FINALIZADA, user=user)


class ReservaCancelada(SituacaoReserva):
    def cancelar(self, reserva, user):
        return reserva

    def checkin(self, reserva, user):
        raise ValueError("Reserva cancelada não permite checkin.")

    def checkout(self, reserva, user):
        raise ValueError("Reserva cancelada não permite checkout.")


class ReservaFinalizada(SituacaoReserva):
    def cancelar(self, reserva, user):
        raise ValueError("Reserva finalizada não pode ser cancelada.")

    def checkin(self, reserva, user):
        return reserva

    def checkout(self, reserva, user):
        return reserva


def get_reserva_state(situacao: str) -> SituacaoReserva:
    if situacao == ReservaSituacao.PENDENTE:
        return ReservaPendente()
    if situacao == ReservaSituacao.CONFIRMADA:
        return ReservaConfirmada()
    if situacao == ReservaSituacao.CANCELADA:
        return ReservaCancelada()
    if situacao == ReservaSituacao.FINALIZADA:
        return ReservaFinalizada()
    
    return ReservaPendente()

