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
import uuid


@csrf_exempt
def authentification(request):      #Fully working
    # Request : {"email":"example@gmail.com","password":"some_password"}
    if request.method == 'POST':
        details_dict = tests.request_to_dict(request)                     # Loading data from Json
        email = details_dict["email"]
        password = details_dict["password"]
        (response,user_id) = tests.auth_user(email,password)
        if response == 0:                                           # Login successul
            return JsonResponse({"Success":True,"user_id":user_id}, status=200)
        else :                                                      # Login error
            return JsonResponse({"Success":False,"errer":response})
    else :
        return HttpResponse("There is no HTML in here")

@csrf_exempt
def signup(request):            #Fully working

    if request.method == 'POST':
        # Request example : {"username":"Sofiane","email":"example@gmail.com","password":"mypass"}
        details_dict = tests.request_to_dict(request)                     # Loading data from Json
        details_dict['IsAdmin'] = False
        email = details_dict["email"]
        password = details_dict["password"]
        username = details_dict["username"]
        id = tests.id_by_username(username)
        if id == 1:
            id_account = str(uuid.uuid4())
            (response,uid) = tests.create_user(id_account,email,password)
            if response == 0:  # Login successful
                details_dict.pop("password")
                tests.store_to_database("User",id_account,details_dict)
                return JsonResponse({"Success": True,"user_id": uid}, status=200)
            else :
                return JsonResponse({"Success":False,"error":response})
        else: return JsonResponse({"Success": False, "error": "username taken"})
    else :
        return HttpResponse("No HTML here !")

@csrf_exempt
def event(request):
    details_dict = tests.request_to_dict(request)
    # Request example :
    # {"organizer_id":"someid","name":"EventName","description":"event_description","participants":["id1","id2"]}
    if request.method == 'POST':        # Fully working
        ide = str(uuid.uuid4())
        (success , error) = tests.store_to_database("Event",ide,details_dict)
        if success == 0:
            return JsonResponse({"Success": True,"event_id":ide})
        else:
            return JsonResponse({"Success": False, "error": error})
    if request.method == "GET":     #Fully working
    # Request example :
    # http://127.0.0.1:8000/event?event_id=695a5d4c-1ba8-4e50-80d1-f631485dd32e
        event_id = request.GET['event_id']
        (success, task_data) = tests.read_from_database("Event", event_id)
        if task_data.exists:
            tasks_array = task_data.to_dict()
            return JsonResponse({"Success": True, "Event": tasks_array})
        else:
            return JsonResponse({"Success": False, "error": "invalid event_id"})

    if request.method == "PUT":          # Fully working
        # request : {"event_id":"someid","*The fields you want to change*":"New_value"}
        event_id = details_dict["event_id"]
        details_dict.pop("event_id")
        (success,error) = tests.edit_from_database("Event",event_id,details_dict)
    if request.method == "DELETE":      # Fully working
        # request : {"event_id":"someid"}
        event_id = details_dict["event_id"]
        (success,error) = tests.delete_from_database("Event",event_id)
    if success == 0:
        return JsonResponse({"Success": True})
    else:
        return JsonResponse({"Success": False, "error": error})


@csrf_exempt
def tasks(request):
    details_dict = tests.request_to_dict(request)
    if request.method == 'POST':            # Working  (no error handling sometimes)

    # Request example : {"user_id":"someid","event_id":"someid","description":"Finish the UI","deadline":"24 feb 2023"}

        details_dict['IsDone'] = False
        idt = str(uuid.uuid4())
        (success , error) = tests.store_to_database("Tasks",idt,details_dict)
        if success == 0:
            # Get the tasks array from the event:
            event_id = details_dict["event_id"]
            user_id = details_dict["user_id"]

            (success,event_data) = tests.read_from_database("Event",event_id)
            event_data = event_data.to_dict()
            try :
                tasks_dict = event_data.pop(u'tasks_dict', None)
            except:
                tasks_dict = []
            if type(tasks_dict) is list:
                tasks_dict.append(idt)
            else:
                tasks_dict = [idt]
            (success,error) = tests.edit_from_database("Event",event_id,{"tasks_dict":tasks_dict})

            #--------------------------------------------------------------------------------

            (success, user_data) = tests.read_from_database("User", user_id)
            user_data = user_data.to_dict()
            try:
                tasks_dict = user_data.pop(u'tasks_dict', None)
            except:
                tasks_dict = []
            if type(tasks_dict) is list:
                tasks_dict.append(idt)
            else:
                tasks_dict = [idt]
            (success, error) = tests.edit_from_database("User", user_id, {"tasks_dict": tasks_dict})
            #---------------------------------------------------------------------------------

    if request.method == "GET":         # Fully working
        # example : http://127.0.0.1:8000/tasks?task_id=9af9f567-2de2-4e7b-8ece-14dfa6a3a118
        task_id = request.GET['task_id']
        (success, task_data) = tests.read_from_database("Tasks", task_id)
        if task_data.exists:
            tasks_array = task_data.to_dict()
            return JsonResponse({"Success": True, "Tasks": tasks_array})
        else:
            return JsonResponse({"Success":False,"error":"invalid task_id"})


    if request.method == "PUT":         # Fully working
        # Request example : {"task_id":"Someid","Field_you_change":"New_value"}
        task_id = details_dict["task_id"]
        details_dict.pop("task_id")
        (success,error) = tests.edit_from_database("Tasks",task_id,details_dict)
    if request.method == "DELETE":      # Fully working
        # Request example : {"task_id":"Someid"}
        task_id = details_dict["task_id"]
        (success,error) = tests.delete_from_database("Tasks",task_id)
    if success == 0:
        return JsonResponse({"Success": True})
    else:
        return JsonResponse({"Success": False, "error": error})

def homepage(request):
  return HttpResponse("In this page , we will render the Admin Dashboard HTML / CSS")

