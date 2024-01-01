from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests

# from .models import PlayerCredit
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .usecase import payments
from text_to_speech.constants import *
from usercredits.models import *

@login_required
def initiate_phonepe_payment(request):
    
        
    credits_to_purchase = 100

    payload = payments.get_payload(request,MERCHANT_ID,MERCHANT_TRANSACTION_ID,credits_to_purchase)

    base64String = payments.base64_encode(payload)
    mainString = base64String + ENDPOINT + SALTKEY
    sha256Val = payments.calculate_sha256_string(mainString)
    checkSum = sha256Val + '###' + INDEX

    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': checkSum,
        'accept': 'application/json',
    }
    json_data = {
        'request': base64String,
    }
    
    response = requests.post('https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay', headers=headers, json=json_data)
    response_data = response.json()
    success = response_data.get('success', False)

    if success:
        redirect_url = response_data['data']['instrumentResponse']['redirectInfo']['url']
        return render(request, 'usercredits/phonepe_payment.html', {'payment_url': redirect_url})
    else:
        # Handle the case where payment initiation failed
        error_message = response_data.get('message', 'Payment initiation failed.')
        return render(request, 'credit/payment_failed.html', {'error_message': error_message})
   




from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        print( request.POST)
        print(request.POST.get('transactionId'))
        request_url = 'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT/' + request.POST['transactionId']
        sha256_Pay_load_String = '/pg/v1/status/PGTESTPAYUAT/' + request.POST['transactionId'] + SALTKEY
        sha256_val = payments.calculate_sha256_string(sha256_Pay_load_String)
        checksum = sha256_val + '###' + INDEX
      
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
            'X-MERCHANT-ID': request.POST['transactionId'],
            'accept': 'application/json',
        }
        response = requests.get(request_url, headers=headers)
        response_data = response.json()
        success = response_data.get('success', False)
        if(success):
            current_user = request.user
            try:
                user_profile = UserCredits.objects.get(pk = current_user.id)
            except UserCredits.DoesNotExist:
                return render(request, 'error_template.html', {'error_message': 'Account not found for the current user'})
            
            user_profile.is_premium_user = True
            return JsonResponse({'SUCESS':success})
        
            #print(response.text);
    return JsonResponse({'SUCESS':"TRUE"})

