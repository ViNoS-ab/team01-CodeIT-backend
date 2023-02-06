import requests
import pyrebase
import firebase_admin
from firebase_admin import credentials,auth
import google.auth
from google.cloud import firestore
import os
import pyrebase
import json

config = {
   "apiKey": "AIzaSyDiYBfEwnDG3t5_XvJslXfKJbP4_68p8bo",
  "authDomain": "gip-codeit-01.firebaseapp.com",
  "databaseURL": "https://gip-codeit-01-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "gip-codeit-01",
  "storageBucket": "gip-codeit-01.appspot.com",
  "messagingSenderId": "9367679166",
  "appId": "1:9367679166:web:d14c004efff7b47e1c2eef",
  "measurementId": "G-F3VBXSGWJ5"
}

# In order for Firebase to work , change


firebase = pyrebase.initialize_app(config)  #   Config Pyrebase
authen = firebase.auth()    # Pyrebase authentification system

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
    print(json_user_details)
    data = json_user_details.dict()  # Getting dict
    data = data['']
    return json.loads(data)  # Loading data from Json

def create_user(id,email,password):
    # Before creating a new user you have to make sure that you activated the
    # Authentification option from your Firebase console
    try:

        user = auth.create_user(uid=id, email=email , password=password)
        print('Sucessfully created new user: {0}'.format(user.uid))
        return (0,user.uid)
    except Exception as e:
        print("Login Failed. Reason:", e)
        return (str(e),0)

def delete_user(uid):
    try :
        auth.delete_user(uid)
        print('Successfully deleted user')
        return 0
    except Exception as e:
        print("Deleting Failed. Reason:", e)
        return 1

def auth_user(email,password):
    try:
        user = authen.sign_in_with_email_and_password(email, password)
        print("Logged in as user:", user["localId"])
        return (0,user["localId"])
    except requests.exceptions.HTTPError as e:
        return (e.args[1].replace("\n",""),0)