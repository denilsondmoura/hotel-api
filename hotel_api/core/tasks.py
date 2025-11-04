from celery import shared_task
import time
from datetime import date
from .enums import ReservaSituacao
from .models import Reserva
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def encaminha_email_confirmacao_reserva_task(reserva_id):
    from .models import Reserva
    reserva = Reserva.objects.get(id=reserva_id)

    assunto = f"Confirmação da sua reserva #{reserva.codigo}"
    mensagem = (
        f"Olá, {reserva.cliente.username}!\n\n"
        f"Sua reserva no {reserva.quarto.hotel.nome} - quarto {reserva.quarto.numero} foi confirmada.\n"
        f"Check-in: {reserva.data_checkin.strftime('%d/%m/%Y')}\n"
        f"Check-out: {reserva.data_checkout.strftime('%d/%m/%Y')}\n\n"
        f"Valor total: R${reserva.valor_total:.2f}\n\n"
        f"Agradecemos pela preferência!"
    )

    destinatario = [reserva.cliente.email]

    send_mail(
        assunto,
        mensagem,
        settings.DEFAULT_FROM_EMAIL,
        destinatario,
        fail_silently=False,
    )

    print(f"E-mail de confirmação enviado para {reserva.cliente.email}")
    print(f"Assunto: Confirmação da sua reserva #{reserva.codigo}")
    print(f"Mensagem: {mensagem}")


@shared_task
def verifica_reservas_concluidas_task():
    print("verificando reservas concluidas")
    hoje = date.today()
    reservas = Reserva.objects.filter(
        data_checkout__lte=hoje
    ).exclude(
        situacao__in=[ReservaSituacao.CANCELADA, ReservaSituacao.FINALIZADA]
    )
    
    for reserva in reservas:
        try:
            state = get_reserva_state(reserva.situacao)
            updated = state.checkout(reserva, None)
        
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    