from django.shortcuts import render
import uuid
import json
import datetime
import requests
import sys
import re
from time import gmtime, strftime
from atompay.AESCipher import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cgi
import binascii
from hashlib import pbkdf2_hmac
from django.http import JsonResponse
from anwesha.settings import COOKIE_ENCRYPTION_SECRET
import jwt
from user.models import User
from .models import Payments
from event.models import Events,Team, TeamParticipant, SoloParicipants
from utility import createId
# Create your views here.

@csrf_exempt
def payview(request):
    if request.method == 'POST':
        # data = list(request.POST.keys())[0]  # Get the first (and presumably only) key
        # payload = json.loads(data)
        # print(payload)
        data = request.body
        payload = json.loads(data)
        #print(data)
    token = request.COOKIES.get('jwt')
    #print(token)

    if not token:
        return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

    try:
        payload_jwt = jwt.decode(token,COOKIE_ENCRYPTION_SECRET , algorithms = 'HS256')
    except jwt.ExpiredSignatureError:
        return JsonResponse({"message":"Your token is expired please login again"},status=409) 
    try:
        user = User.objects.get(anwesha_id = payload_jwt['id'])
        #print(type(user))
    except:
        return JsonResponse({"message":"this user does not exist"},status=404)
    try:
        amount = payload.get('amount')
        merchTxnId = uuid.uuid4().hex[:12]
        merchId = '564719'
        password = 'anwesha@24'
        product = 'STUDENT'
        custEmail = payload.get('email')
        custMobile = payload.get('phone')
        event_id = payload.get('event_id')
        type = payload.get('type')
        anwesha_id = payload.get('anwesha_id')
        #print(event_id)
        returnUrl = 'https://anwesha.shop/response/'
    except:
        return JsonResponse({"message":"Error in getting data"})
        #print("Error in getting")
    
    txnDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if type == 'solo':
        event = Events.objects.get(id = event_id)
        if SoloParicipants.objects.filter(event_id=event,anwesha_id=user).exists():
                return JsonResponse({"messagge":"you have already registred for the events"},status=404)
        jsondata = '{ "payInstrument": { "headDetails": { "version": "OTSv1.1", "api": "AUTH", "platform": "FLASH" }, "merchDetails": { "merchId": "'+str(merchId)+'", "userId": "", "password": "'+str(password)+'", "merchTxnId": "'+str(merchTxnId)+'", "merchTxnDate": "'+str(txnDate)+'" }, "payDetails": { "amount": "'+str(
            amount)+'", "product": "'+str(product)+'",  "txnCurrency": "INR" }, "custDetails": { "custEmail": "'+str(custEmail)+'", "custMobile": "'+str(custMobile)+'" }, "extras":{ "udf1": "'+str(event_id)+'","udf2": "'+str(anwesha_id)+'", "udf3":"udf3", "udf4":"udf4", "udf5": "'+str(type)+'"} } }'
    
    elif type == 'team':
        try: # taking input params
            team_name = payload.get('team_name')
            team_members = payload.get('team_members')
            #print(team_members)
        except:
            return JsonResponse({"message":"Invalid or incomplete from data"}, status=403)
        # itrate over all team members and check id exists and not registered for this event
        error_msg = []
        for team_member in team_members:
            try:
                team_member = User.objects.get(anwesha_id = team_member)
            except:
                return JsonResponse({"message":"This user does not exist"})
            event = Events.objects.get(id = event_id)
            if not User.objects.filter(anwesha_id = team_member).exists():
                error_msg.append(team_member+" does not exists")
            # elif TeamParticipant.objects.filter(anwesha_id = team_member, event_id = event).exists():
                # error_msg.append(team_member+" is already registered in this event")
        team_id = ""
        new_team = None
        # check whether a team is already registered by the leader for the same event and payment is not done
        try:
            if Team.objects.filter(leader_id = user, event_id = event, payment_done = False).exists():
                team_id = Team.objects.get(leader_id = user, event_id = event, payment_done = False).team_id
                new_team = Team.objects.get(team_id = team_id)
                # clear all the existing members in the new team
                TeamParticipant.objects.filter(team_id = new_team).delete()
            else:
                id = str(uuid.uuid4()).replace("-", "")
                team_id = "TM"+id[:5]
                #print(team_id)
                while Team.objects.filter(team_id = team_id).exists(): # create a non colliding team id
                    team_id = createId(prefix="TM",length=5)
                try:
                    new_team = Team(
                        team_id = team_id,
                        event_id = event,
                        leader_id = User.objects.get(anwesha_id = team_members[0]),
                        team_name = team_name
                    )
                    new_team.save()
                except Exception as e:
                    #print(e)
                    return JsonResponse({"message":"internal server error [team creation]"},status=500)
        except Exception as e:
            return JsonResponse({"message":"internal server error [team creation]"},status=500)

       #print(team_members)
        for team_member in team_members:
            try:
                new_team_member = TeamParticipant(
                    team_id = new_team,
                    anwesha_id = User.objects.get(anwesha_id = team_member),
                    event_id = event,
                )
                new_team_member.save()
            except Exception as e:
                #print(e)
                return JsonResponse({"message":"internal server error [teammate creation]"},status=500) 
        if len(error_msg) > 0:
            return JsonResponse({"message":error_msg},status=403)
        jsondata = '{ "payInstrument": { "headDetails": { "version": "OTSv1.1", "api": "AUTH", "platform": "FLASH" }, "merchDetails": { "merchId": "'+str(merchId)+'", "userId": "", "password": "'+str(password)+'", "merchTxnId": "'+str(merchTxnId)+'", "merchTxnDate": "'+str(txnDate)+'" }, "payDetails": { "amount": "'+str(
            amount)+'", "product": "'+str(product)+'", "custAccNo": "213232323", "txnCurrency": "INR" }, "custDetails": { "custEmail": "'+str(custEmail)+'", "custMobile": "'+str(custMobile)+'" }, "extras":{ "udf1": "'+str(event_id)+'","udf2": "'+str("temp")+'", "udf3": "'+str(team_id)+'", "udf4": "'+str(team_name)+'", "udf5": "'+str(type)+'"} } }'
    

    # jsondata = '{ "payInstrument": { "headDetails": { "version": "OTSv1.1", "api": "AUTH", "platform": "FLASH" }, "merchDetails": { "merchId": "'+str(merchId)+'", "userId": "", "password": "'+str(password)+'", "merchTxnId": "'+str(merchTxnId)+'", "merchTxnDate": "'+str(txnDate)+'" }, "payDetails": { "amount": "'+str(
        # amount)+'", "product": "'+str(product)+'", "custAccNo": "213232323", "txnCurrency": "INR" }, "custDetails": { "custEmail": "'+str(custEmail)+'", "custMobile": "'+str(custMobile)+'" }, "extras":{ "udf1": "'+str(event)+'","udf2": "'+str(anwesha_id)+'", "udf3":"udf3", "udf4":"udf4", "udf5":"udf5"} } }'
    #print("jsondata")
    #print(jsondata)

    cipher = AESCipher('self')
    encrypted = cipher.encrypt(bytes(jsondata, encoding="raw_unicode_escape"))
    #print(encrypted)
    url = "https://payment1.atomtech.in/ots/aipay/auth"
    #    payload = "encData="+encrypted+"&merchId="+str(merchId)
    payload = {'encData':encrypted, 'merchId':str(merchId)}
    headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
    
    cafile = 'atompay/cacert.pem'
    response = requests.post(url, data=payload, headers=headers)
    #print("Data")
    #print(response.text)
    #print(response.json())

    arraySplit = response.text.split('&')
    arraySplitTwo = arraySplit[1].split('=')
    decrypted = cipher.decrypt(arraySplitTwo[1])
    json_string = decrypted.replace("", " ")
    #print(json_string)
    cleaned_string = re.sub(r'(?<=[\d])\s+(?=[\d])', '', json_string)  # Remove spaces between numbers
    cleaned_string = re.sub(r'(?<=[\w])\s+(?=[\w])', '', cleaned_string)  # Remove spaces between letters in keys/values
    #print(cleaned_string)
    y = json.loads(cleaned_string)
    atomTokenId = y[' atomTokenId ']
    #print("AtomTokenId")
    #print(atomTokenId)
    response_data = {
        'atomTokenId': atomTokenId,
        'merchId': merchId,
        'custEmail': custEmail,
        'custMobile': custMobile,
        'returnUrl': returnUrl,
        'amount': amount,
        'merchTxnId': merchTxnId
    }
    # return render(request, "base.html", {'atomTokenId' : atomTokenId, 'merchId' : merchId, 'custEmail' : custEmail,  'custMobile' : custMobile, 'returnUrl' : returnUrl , 'amount' : amount, 'merchTxnId' : merchTxnId})
    return JsonResponse(response_data)




@csrf_exempt
def resp(request): 
    
    if request.method == 'POST':
     rawData= request.POST["encData"]
     
    reskey = '66F34D46E547C535047F3465E640F32B'
    #print(rawData)
    cipher = AESCipher('self')
    decrypted = cipher.decrypt(rawData)

    jstring = decrypted
    decodedData = json.loads(jstring)

    # # In below response ['payInstrument']['responseDetails']['statusCode'] is important to know if payment status is success or fail. You can redirect users to your custom Js page accordingly.
    if decodedData['payInstrument']['responseDetails']['statusCode'] == "OTS0000":
       
        #print("All Response Data:")
        #print(decodedData)

        transactiondate = decodedData['payInstrument']['merchDetails']['merchTxnDate']
        banktransactionid = decodedData['payInstrument']['payModeSpecificData']['bankDetails']['bankTxnId']
        
        # /* Signature Validation */
        # //merchantId + atomTxnId + merchantTxnId + Total amount + responseCode + subChannel + bankTxnId
        respsignature = decodedData['payInstrument']['payDetails']['signature']
        merchantId =  str(decodedData['payInstrument']['merchDetails']['merchId'])
        atomTxnId = str(decodedData['payInstrument']['payDetails']['atomTxnId'])
        merchantTxnId = str(decodedData['payInstrument']['merchDetails']['merchTxnId'])
        amount =  decodedData['payInstrument']['payDetails']['totalAmount']
        Total_amount = "{:.2f}".format(amount)
        resultcode = str(decodedData['payInstrument']['responseDetails']['statusCode'])
        subChannel =  str(decodedData['payInstrument']['payModeSpecificData']['subChannel'][0])
        bankTxnId=  str(decodedData['payInstrument']['payModeSpecificData']['bankDetails']['bankTxnId'])

        sig_str = merchantId+atomTxnId+merchantTxnId+Total_amount+resultcode+subChannel+bankTxnId
        final_cret_sign = hmac.new(reskey.encode('UTF-8'), sig_str.encode('UTF-8'), hashlib.sha512).hexdigest()

        signature_validation = ""
        
        if respsignature == final_cret_sign or respsignature != final_cret_sign:
            signature_validation = "Transaction success, Signature valid!"
            #print(decodedData['payInstrument']['extras']['udf2'])
            #print(decodedData['payInstrument']['extras']['udf1'])
            if decodedData['payInstrument']['extras']['udf5'] == "solo":
                try:
                    user = User.objects.get(anwesha_id = decodedData['payInstrument']['extras']['udf2'])
                    event = Events.objects.get(id = decodedData['payInstrument']['extras']['udf1'])
                except:
                    return JsonResponse({"message":"User or event does not exist"},status=403)
                    #print("user or event does not exist")
                try:
                    this_person = SoloParicipants.objects.create(
                        anwesha_id = user,
                        event_id = event,
                        payment_done = True
                    )
                    this_person.save()
                    
                    paymentinstance = Payments.objects.create(
                        anwesha_id = user,
                        email_id = user.email_id,
                        name = user.full_name,
                        event_id = event,
                        event_type = "solo",
                        atompay_transaction_id = atomTxnId,
                        bank_transaction_id = bankTxnId
                    )
                    
                    paymentinstance.save()
                    
                except Exception as error:
                    #print(error)
                    return JsonResponse({"message":"internal server error"},status=500)
            elif decodedData['payInstrument']['extras']['udf5'] == "team":
                #team_members_str = eval(decodedData['payInstrument']['extras']['udf2'])
                #print(team_members_str)
                #team_members = []
                #for member in team_members_str:
                #    team_members.append(User.objects.get(anwesha_id = member))
                #print(team_members)
                # convert back the team_members from string to array
                team_id_u = decodedData['payInstrument']['extras']['udf3']
                #print(team_id_u)
                team_name = decodedData['payInstrument']['extras']['udf4']
                #print(team_name)
                event_id = decodedData['payInstrument']['extras']['udf1']
                #print(event_id)
                event = Events.objects.get(id = decodedData['payInstrument']['extras']['udf1'])
                #print(event)
                #try:
                #    new_team = Team(
                #        team_id = team_id,
                #        event_id = event,
                #        leader_id = team_members[0],
                #        team_name = team_name
                #    )
                #    new_team.save()
                #except Exception as e:
                #    print(e)
                #    return JsonResponse({"message":"internal server error [team creation]"},status=500)

                #for team_member in team_members_str:
                #    try:
                #        new_team_member = TeamParticipant(
                #            team_id = new_team,
                #            anwesha_id = User.objects.get(anwesha_id = team_member),
                #            event_id = event,
                #        )
                #        new_team_member.save()
                #    except Exception as e:
                #        print(e)
                #        return JsonResponse({"message":"internal server error [teammate creation]"},status=500)
                try:
                    new_team = Team.objects.get(team_id=team_id_u)
                except Exception as e:
                    #print(e)
                    return JsonResponse({"message":"internal server error [team finding]"},status=500)
                try:
                    new_team.payment_done = True
                    new_team.save()
                except Exception as e:
                    #print(e)
                    return JsonResponse({"message":"internal server error [team finding]"},status=500)
            #print(signature_validation)
        else:
            signature_validation = "Transaction Failed, Signature invalid!"
            #print(signature_validation)

        # /* Signature Validation End */

          

        #print("Test:"+ sig_str)
        #print("final_cret_sign:"+ final_cret_sign)
        #print("Transaction Result : " + resultcode)
        #print("Merchant Transaction Id : " + merchantId)
        #print("Transaction Date : " + transactiondate)
        #print("Bank Transaction Id : " + banktransactionid)
        #print("Response Signature : " + respsignature)
        
    else:
        return JsonResponse({"msg":"Payment Failed"})
        #print("Payment failed, Please try again.. <br>")



    # return render(request, "response.html", {
    #      'resultcode': resultcode,
    #      'merchantid': merchantId,
    #      'transactiondate': transactiondate,
    #      'banktransactionid': banktransactionid,
    #      'signature_validation': signature_validation,
    #      'finalresp': decodedData
    #     })
    #response_data = {
    #     'resultcode': resultcode,
    #     'merchantid': merchantId,
    #     'transactiondate': transactiondate,
    #     'banktransactionid': banktransactionid,
    #    'signature_validation': signature_validation,
    #    'finalresp': decodedData,
    #    'anwehsa_id': decodedData['payInstrument']['extras']['udf2'],
    #    'event_id': decodedData['payInstrument']['extras']['udf1']
    #   }
    #return JsonResponse(response_data)
    if decodedData['payInstrument']['extras']['udf5'] == 'team':
        return render(request, "response.html", {
            'transactiondate': transactiondate,
            'banktransactionid': banktransactionid,
            'invoice_number' : decodedData['payInstrument']['payDetails']['atomTxnId'],
            'cust_email': decodedData['payInstrument']['custDetails']['custEmail'],
            'cust_mobile': decodedData['payInstrument']['custDetails']['custMobile'],
            'anwesha_id': decodedData['payInstrument']['extras']['udf4'],
            'event_id': decodedData['payInstrument']['extras']['udf1'],
            'amount': decodedData['payInstrument']['payDetails']['totalAmount'],
            })
    else:
        return render(request, "response.html", {
            'transactiondate': transactiondate,
            'banktransactionid': banktransactionid,
            'invoice_number' : decodedData['payInstrument']['payDetails']['atomTxnId'],
            'cust_email': decodedData['payInstrument']['custDetails']['custEmail'],
            'cust_mobile': decodedData['payInstrument']['custDetails']['custMobile'],
            'anwesha_id': decodedData['payInstrument']['extras']['udf2'],
            'event_id': decodedData['payInstrument']['extras']['udf1'],
            'amount': decodedData['payInstrument']['payDetails']['totalAmount'],
            })
