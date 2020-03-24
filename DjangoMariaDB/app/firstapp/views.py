# Create your views here.
#IMPORT models
from .models import Movie,ApiUsers

#IMPORT LIBRARIRES/FUNCTIONS
#from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
import json
from firstapp.customClasses import *
#IMPORT DJANGO PASSWORD HASH GENERATOR AND COMPARE
from django.contrib.auth.hashers import make_password, check_password

#check_password(noHashPassword,HashedPassword) this funcion validate if the password match to the hash

def login(request):

    #VALIDATE METHOD
    if request.method == 'POST': 

        #DECLARE RESPONSE
        response_data = {}
        body = {}

        #CHECK JSON STRUCTURE
        is_json = checkJson().isJson(request.body)
        if is_json != True :
            return JsonResponse(is_json, status=400)
        
        #CHECK JSON CONTENT
        body = json.loads(request.body)

        if 'user' not in body:
            response_data = {}
            response_data['result'] = 'error'
            response_data['message'] = 'User is required'
            return JsonResponse(response_data, status=401)
        elif 'password' not in body:
            response_data = {}
            response_data['result'] = 'error'
            response_data['message'] = 'Password is required'
            return JsonResponse(response_data, status=401)


        #CHECK IF USER EXITST
        try:
            obj = ApiUsers.objects.get(user=body['user'])
        except ApiUsers.DoesNotExist:
            response_data ={}
            response_data['result'] = 'error'
            response_data['message'] = 'The user does not exist or the password is incorrect'
            return JsonResponse(response_data, status = 401)

        #TAKE PASSWORD OF THE USER
        hashed_password = obj.password
        #CHECK IF PASSWORD IS CORRECT
        if not check_password(body['password'],hashed_password) : 
            response_data ={}
            response_data['result'] = 'error'
            response_data['message'] = 'The user does not exist or the password is incorrect'
            return JsonResponse(response_data, status = 401)


        #CHECK IF USER HAS API-KEY
        if obj.api_key is None:
            obj.api_key = ApiKey().generate_key_complex()
            obj.save()

        #RETURN RESPONSE
        response_data['result'] = "success"
        response_data['message'] = "Valid credentials"
        response_data['userApiKey'] = obj.api_key
        return JsonResponse(response_data, status=200)

    else:
        response_data = {}
        response_data['result'] = 'error'
        response_data['message'] = 'Invalid Request'
        return JsonResponse(response_data, status=400)


def makePassword(request,password):
    hashPassword = make_password(password)
    response_data = {}
    response_data['password'] = hashPassword
    return JsonResponse(response_data, status=200)
