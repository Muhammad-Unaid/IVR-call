from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
import json

account_sid = 'AC48cfa245381df454027305d01375ca59'
auth_token = '07edfa5e9d474b9fe449fb168bfe1621'
twilio_number = '+16203178280'
client = Client(account_sid, auth_token)

@csrf_exempt
def shopify_webhook(request):
    data = json.loads(request.body)
    phone = data['shipping_address']['phone']

    call = client.calls.create(
        to=phone,
        from_=twilio_number,
        url='https://yourdomain.com/ivr/'
    )
    return HttpResponse("Call started", status=200)

@csrf_exempt
def ivr(request):
    response = VoiceResponse()
    gather = Gather(num_digits=1, action='/ivr/handle-input/', method='POST')
    gather.say("Hello! Ye call Royal Trends ki taraf se hai. Aap ne ek order place kiya hai. Agar aap order confirm karna chahte hain to 1 dabayein, warna 0 dabayein.", language="ur-PK")
    response.append(gather)
    response.redirect('/ivr/')
    return HttpResponse(str(response), content_type='text/xml')

@csrf_exempt
def handle_input(request):
    digit = request.POST.get('Digits')
    response = VoiceResponse()

    if digit == '1':
        response.say("Aap ka order confirm ho gaya hai. Shukriya!", language='ur-PK')
    elif digit == '0':
        response.say("Aap ka order cancel kar diya gaya hai.", language='ur-PK')
    else:
        response.say("Invalid input. Dubara koshish karein.", language='ur-PK')
        response.redirect('/ivr/')

    return HttpResponse(str(response), content_type='text/xml')
