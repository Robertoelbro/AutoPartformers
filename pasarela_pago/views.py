from django.shortcuts import render, redirect
from django.urls import reverse
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from transbank.error.transbank_error import TransbankError

Transaction.COMMERCE_CODE = '597055555532'
Transaction.API_KEY = '597055555532'
Transaction.INTEGRATION_TYPE = IntegrationType.TEST

def formulario_pago(request):
    return render(request, 'formulario_pago.html')

def iniciar_pago(request):
    if request.method == 'POST':
        try:
            monto = int(request.POST.get('monto'))
            buy_order = f'order-{monto}'
            session_id = 'demo-session'
            return_url = request.build_absolute_uri(reverse('confirmar_pago'))

            transaction = Transaction()
            response = transaction.create(buy_order, session_id, monto, return_url)

            return redirect(f"{response['url']}?token_ws={response['token']}")

        except TransbankError as e:
            return render(request, 'error_pago.html', {'error': str(e)})
        except Exception as e:
            return render(request, 'error_pago.html', {'error': 'Error inesperado: ' + str(e)})

    return redirect('formulario_pago')

def confirmar_pago(request):
    token = request.GET.get('token_ws')
    transaction = Transaction()

    try:
        response = transaction.commit(token)
        if response['status'] == 'AUTHORIZED':
            return render(request, 'exito.html', {
                'total': response.get('amount'),
                'codigo_autorizacion': response.get('authorization_code')
            })
        else:
            return render(request, 'error_pago.html', {'error': 'Pago no autorizado'})
    except TransbankError as e:
        return render(request, 'error_pago.html', {'error': str(e)})
