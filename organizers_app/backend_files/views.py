from django.shortcuts import render
import json
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt
import firebase_admin
from firebase_admin import credentials,auth
import google.auth
from google.cloud import firestore
import pyrebase
from . import tests

id_counter = 0

@csrf_exempt
def authentification(request):
    if request.method == 'POST':
        json_user_details = request.POST                        # Getting data from the request
        details_dict = tests.request_to_dict(json_user_details)                     # Loading data from Json
        email = details_dict["email"]
        password = details_dict["password"]
        (response,user_id) = tests.auth_user(email,password)
        if response == 0:                                           # Login successul
            return JsonResponse({"Success":True,"user_id":user_id}, status=200)
        else :                                                      # Login error
            json_object = json.loads(response)
            return JsonResponse(json_object)
    else :
        return HttpResponse("There is no HTML in here")

@csrf_exempt
def signup(request):
    global id_counter
    if request.method == 'POST':
        json_user_details = request.POST

        details_dict = tests.request_to_dict(json_user_details)                     # Loading data from Json
        email = details_dict["email"]
        password = details_dict["password"]
        id_account = str(id_counter)
        (response,uid) = tests.create_user(id_account,email,password)
        if response == 0:  # Login successful
            id_counter += 1
            return JsonResponse({"Success": True,"user_id": uid}, status=200)
        else :
                                # Login error
            error = '{"Success": "False", "Error": "'+response+'"}'
            json_object = json.loads(error)
            return JsonResponse(json_object)
    else :
        return HttpResponse("No HTML here !")
def homepage(request):
  return HttpResponse("In this page , we will render the Admin Dashboard HTML / CSS")

