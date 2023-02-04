from django.shortcuts import render
import json
from django.http import HttpResponse , JsonResponse
from django.views.decorators.csrf import csrf_exempt
import firebase_admin
from firebase_admin import credentials
import google.auth
from google.cloud import firestore
import os


# This is an important step to login to database , please Amine do'nt change anything
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./gip-codeit-01-firebase-adminsdk-xan5d-efd6bf3deb.json"

cred = credentials.Certificate("./gip-codeit-01-firebase-adminsdk-xan5d-efd6bf3deb.json")


credentials, project_id = google.auth.default()
db = firestore.Client(credentials=credentials, project=project_id)
firebase_admin.initialize_app(cred)

# Initialize a Firestore client
db = firestore.Client()

def store_to_database(collection , document , query_dict):
    doc_ref = db.collection(collection).document(document)
    doc_ref.set(query_dict)

def request_to_dict(json_user_details):
    data = json_user_details.dict()  # Getting dict
    data = data['']
    return json.loads(data)  # Loading data from Json


@csrf_exempt
def authentification(request):
    if request.method == 'POST':
        json_user_details = request.POST                        # Getting data from the request
        details_dict = request_to_dict(json_user_details)                     # Loading data from Json
        store_to_database("users","wkdN4NKpXJ5NBcya3mBN",details_dict)        # Store data to database
        return JsonResponse(details_dict, status=200)
    else :
        return HttpResponse("Hello World", status=200)



def homepage(request):
  return HttpResponse("In this page , we will render the Admin Dashboard HTML / CSS")

