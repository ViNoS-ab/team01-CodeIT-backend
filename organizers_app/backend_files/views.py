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

event_index = 0
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

@csrf_exempt
def event(request):
    global event_index
    if request.method == 'POST':
        json_user_details = request.POST                        # Getting data from the request
        details_dict = tests.request_to_dict(json_user_details)                     # Loading data from Json
        name = details_dict["name"]
        (success , error) = tests.store_to_database("Event",name+str(event_index),details_dict)
        if success == 0:
           event_index+=1
           return JsonResponse({"Success":True})
        else:
            return JsonResponse({"Success":False,"error":error})
    if request.method == "GET":
        my_data = request.GET.get("name")
        print(my_data)
        return HttpResponse("ok")
    if request.method == "PUT":
        # Split the request body into parts
        parts = request.body.split(b'\r\n')
        # Find the part that contains the JSON data
        json_part = next(p for p in parts if p.startswith(b'{"'))
        # Parse the JSON data into a Python object
        details_dict = json.loads(json_part.decode('utf-8'))
        event_id = details_dict["event_id"]
        details_dict.pop("event_id")
        (response,error) = tests.edit_from_database("Event",event_id,details_dict)
        if response == 0:
            return JsonResponse({"Success": True})
        else:
            return JsonResponse({"Success": False, "error": error})
    if request.method == "DELETE":
        parts = request.body.split(b'\r\n')
        # Find the part that contains the JSON data
        json_part = next(p for p in parts if p.startswith(b'{"'))

        # Parse the JSON data into a Python object
        details_dict = json.loads(json_part.decode('utf-8'))
        event_id = details_dict["event_id"]
        (response,error) = tests.delete_from_database("Event",event_id)
        if response == 0:
            return JsonResponse({"Success": True})
        else:
            return JsonResponse({"Success": False, "error": error})



def homepage(request):
  return HttpResponse("In this page , we will render the Admin Dashboard HTML / CSS")

