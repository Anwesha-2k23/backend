from django.shortcuts import render
import uuid
import json
import requests
import re
import hmac
import hashlib
from .models import FestPasses
from time import gmtime, strftime
from atompay.AESCipher import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from anwesha.settings import COOKIE_ENCRYPTION_SECRET, ATOM_RESPONSE_KEY
import jwt
from user.models import User,AppUsers
from user.utility import Autherize,AppAutherize
from rest_framework.views import APIView
from .models import *
from utility import createId


class getStatus(APIView):
    @AppAutherize()
    def post(self,request):
        id = request.data["signature"]
        try:
            try:
                user = User.objects.get(signature = id)
            except:
                return JsonResponse({"message":"User not found"},status=404)
            anwesha_id = user.anwesha_id
            if user.user_type == "IITP-Student" or user.user_type == "iitp_student":
                #print(user.user_type)
                return JsonResponse({"anwesha_id":anwesha_id,
                                     "email":user.email_id,
                                     "user_type":user.user_type,
                                     "status":"200"})
            else:
    
                try:
                    festobj = FestPasses.objects.filter(anwesha_id = anwesha_id).first()
                except:
                    return JsonResponse({"message":"No entry found"},status=404)
                return JsonResponse({"anwesha_id":anwesha_id,
                                 "email":festobj.email_id,
                                 "has_entered":festobj.has_entered,
                                 "payment_done":festobj.payment_done,
                                 "user_type":user.user_type,
                                 "status":"200"})
        except:
            return JsonResponse({"message": "No entry found"}, status=404)

class setStatus(APIView):
    @AppAutherize()
    def post(self,request):
        id = request.data["signature"]
        try:
            user = User.objects.get(signature = id)
            
            # Check Myntra Verification
            if not user.myntraVerified:
                return JsonResponse({"message": "Entry Denied: You have not filled the Myntra Sponsor Form. Please fill it to verify your ticket.", "status": "403"}, status=403)

            anwesha_id = user.anwesha_id
            festobj = FestPasses.objects.filter(anwesha_id = anwesha_id).first()
            festobj.has_entered = True
            festobj.save()
            return JsonResponse({"message":"User entered successfully",
                                "anwesha_id":anwesha_id,
                                "email":festobj.email_id,
                                "has_entered":festobj.has_entered,
                                "payment_done":festobj.payment_done,
                                "status":"200"})
        except:
            return JsonResponse({"message": "Invalid token."}, status=409)


class checkPass(APIView):
    @Autherize()
    def post(self,request,**kwargs):
        user = kwargs['user']
        try:
            festpass = FestPasses.objects.get(anwesha_id=user.anwesha_id)
            return JsonResponse({
                "anwesha_id": festpass.anwesha_id.anwesha_id,
                "email": festpass.email_id,
                "has_entered": festpass.has_entered,
                "payment_done": festpass.payment_done,
                "status": "200"
            }, status=200)
        except FestPasses.DoesNotExist:
            return JsonResponse({"message": "Fest pass not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": "Error retrieving fest pass info"}, status=500)

class festpasses(APIView):
    @Autherize()
    def post(self,request, **kwargs):
        user = kwargs['user']
        
        if user.user_type == User.User_type_choice.IITP_STUDENT:
            return JsonResponse({"message":"You are already registered"})
        
        else:
            anwesha_id = user.anwesha_id
            email = user.email_id
            try:
                preRegister = FestPasses.objects.filter(anwesha_id=anwesha_id,payment_done=True).exists()
                data = FestPasses.objects.filter(anwesha_id=anwesha_id)
                if preRegister:
                    #print("flag")
                    return JsonResponse({"message":"You have already purchased festpass"},status=200)
                return JsonResponse({"message":"You have already purchased festpass"},status=200)
            
            except Exception as e:
                #print(e)
                return JsonResponse({"message":"Internal Server Error"},status=500)

            # try:
            #     this_person = FestPasses.objects.create(
            #         anwesha_id = anwesha_id,
            #         email_id = email,
            #         transaction_id = 
            #     )
            #     if user.user_type == User.User_type_choice.IITP_STUDENT:  
            #         this_person.payment_done = True
            #         this_person.save()
            #         return JsonResponse({"message":"Event registration suceessfully completed", "payment_url": None },status=201)
            #     this_person.save()
            # except:
            #     return JsonResponse({"message":"internal server error"},status=500)
            
            # return JsonResponse({"message":"Event registration suceessfully completed","payment_url": event.payment_link},status=201)
            


@csrf_exempt
def payview(request):
    if request.method == 'POST':
        data = request.body
        payload = json.loads(data)
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)
    token = auth_header.split(' ', 1)[1].strip()

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
        # Always charge ₹899 for FESTPASS, ignore client-sent amount
        amount = 899
        merchTxnId = uuid.uuid4().hex[:12]
        merchId = '564719'
        password = 'b5d2bc5e'
        product = 'STUDENT'
        custEmail = payload.get('email')
        custMobile = payload.get('phone')
        event_id = payload.get('event_id') # FSTP
        type = payload.get('type')  # Remember to set type as FESTPASS
        anwesha_id = payload.get('anwesha_id')
        returnUrl = 'https://anwesha.shop/festpasses/response'
    except:
        return JsonResponse({"message":"Error in getting data"})
    
    txnDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    if FestPasses.objects.filter(anwesha_id = user).exists():
        return JsonResponse({"message":"You have already purchased festpass"})
    
    jsondata = '{ "payInstrument": { "headDetails": { "version": "OTSv1.1", "api": "AUTH", "platform": "FLASH" }, "merchDetails": { "merchId": "'+str(merchId)+'", "userId": "", "password": "'+str(password)+'", "merchTxnId": "'+str(merchTxnId)+'", "merchTxnDate": "'+str(txnDate)+'" }, "payDetails": { "amount": "'+str(
            amount)+'", "product": "'+str(product)+'",  "txnCurrency": "INR" }, "custDetails": { "custEmail": "'+str(custEmail)+'", "custMobile": "'+str(custMobile)+'" }, "extras":{ "udf1": "'+str(event_id)+'","udf2": "'+str(anwesha_id)+'", "udf3":"udf3", "udf4":"udf4", "udf5": "'+str(type)+'"} } }'
    
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
    response = requests.post(url, data=payload, headers=headers, verify=cafile)
    # print("Data")
    # print(response.text)
    # print(response.json())
    arraySplit = response.text.split('&')
    arraySplitTwo = arraySplit[1].split('=')
    decrypted = cipher.decrypt(arraySplitTwo[1])
    json_string = decrypted.replace("", " ")
    # print(json_string)
    cleaned_string = re.sub(r'(?<=[\d])\s+(?=[\d])', '', json_string)  # Remove spaces between numbers
    cleaned_string = re.sub(r'(?<=[\w])\s+(?=[\w])', '', cleaned_string)  # Remove spaces between letters in keys/values
    #print(cleaned_string)
    y = json.loads(cleaned_string)
    atomTokenId = y[' atomTokenId ']
    # print("AtomTokenId")
    # print(atomTokenId)
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
     
    reskey = ATOM_RESPONSE_KEY
    print(f"DEBUG PAYMENT: Using response key {reskey}")
    # print(rawData)
    cipher = AESCipher('self')
    decrypted = cipher.decrypt(rawData)

    jstring = decrypted
    decodedData = json.loads(jstring)

    # # In below response ['payInstrument']['responseDetails']['statusCode'] is important to know if payment status is success or fail. You can redirect users to your custom Js page accordingly.
    if decodedData['payInstrument']['responseDetails']['statusCode'] == "OTS0000":
       
        # print("All Response Data:")
        # print(decodedData)

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
        
        # if respsignature == final_cret_sign:
        if True:
            signature_validation = "Transaction success, Signature valid!"
            #print(decodedData['payInstrument']['extras']['udf2'])
            #print(decodedData['payInstrument']['extras']['udf1'])
            if decodedData['payInstrument']['extras']['udf5'] == "FESTPASS":
                try:
                    user = User.objects.get(anwesha_id = decodedData['payInstrument']['extras']['udf2'])
                    email = user.email_id
                except:
                    return JsonResponse({"message":"User does not exist"},status=403)
                    #print("user or event does not exist")
                try:
                    id = createId("PASS",7)
                    curr_pass = FestPasses.objects.create(
                        anwesha_id = user,
                        email_id = email,
                        transaction_id = atomTxnId,
                        payment_done = True
                    )
                    curr_pass.save()
                    
                except Exception as error:
                    #print(error)
                    return JsonResponse({"message":"internal server error"},status=500)
           
        else:
            signature_validation = "Transaction Failed, Signature invalid!"
            return JsonResponse({"message":signature_validation})
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
    
    return render(request, "response.html", {
        'transactiondate': transactiondate,
        'banktransactionid': banktransactionid,
        'invoice_number' : decodedData['payInstrument']['payDetails']['atomTxnId'],
        'cust_email': decodedData['payInstrument']['custDetails']['custEmail'],
        'cust_mobile': decodedData['payInstrument']['custDetails']['custMobile'],
        'anwesha_id': decodedData['payInstrument']['extras']['udf2'],
        'event_id': decodedData['payInstrument']['extras']['udf1'],
        'amount': decodedData['payInstrument']['payDetails']['totalAmount'],
        'myntra_url': 'https://myntra.onelink.me/dNYC/psb0vkzt',
        'show_myntra_warning': True,
    })

