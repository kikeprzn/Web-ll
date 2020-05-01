# Create your views here.
#IMPORT models
from .models import Movie,ApiUsers

#IMPORT LIBRARIRES/FUNCTIONS
from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
import json
from firstapp.customClasses import *
#IMPORT DJANGO PASSWORD HASH GENERATOR AND COMPARE
from django.contrib.auth.hashers import make_password, check_password

#check_password(noHashPassword,HashedPassword) this funcion validate if the password match to the hash


def home(request):

    user_name = ""
    try:
        obj = ApiUsers.objects.get(user='kike')
        user_name = obj.user 
    except ApiUsers.DoesNotExist:
        user_name = "No está el nombre we"

    return render(request, 'dashboard.html', {'title': "usuario" , 'user_name':user_name})
    # return render(request, 'dashboard.html')


def products(request):
	return render(request, 'products.html')

def customer(request):
	return render(request, 'customer.html')

def todoList(request):
	return render(request, 'list.html')


def login(request):

    #VALIDATE METHOD
    if request.method == 'POST':
        response,status = getLogged(request)
        return JsonResponse(response, status= status)
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

def getMovies(request):
    if request.method == 'POST':

        # Comprobando que existe en el header la APIKey
        response_data={}
        api_check = ApiKey().check(request)
        if api_check != True:
            return JsonResponse(api_check,status = 400)

        # Comprobando que el login es correcto
        response, status = getLogged(request)
        if status != 200:
            return JsonResponse(response, status= status)
        
        # Probando que la credencial coincide con la del user
        if response['userApiKey'] != request.headers["user-api-key"]:
            response_data = {}
            response_data['result'] = 'error'
            response_data['message'] = 'Invalid Api-Key'
            return JsonResponse(response_data, status=400)

        # Si todo fue correcto añadimos las películas 
        obj = Movie.objects.all()
        response_data['result'] = "success"
        response_data['movies'] = []
        for item in obj:
                aux = {}
                aux['id'] = item.movieid
                aux['title'] = item.movietitle
                aux['releaseDate'] = item.releasedate
                aux['imageUrl'] = item.imageurl
                aux['description'] = item.description
                response_data['movies'].append(aux)
        
        return JsonResponse(response_data, status=200)
         
    else:
        response_data = {}
        response_data['result'] = 'error'
        response_data['message'] = 'Invalid Request'
        return JsonResponse(response_data, status=400)



def getLogged(request):

    #DECLARE RESPONSE
    response_data = {}
    body = {}

    #CHECK JSON STRUCTURE
    is_json = checkJson().isJson(request.body)
    if is_json != True :
        return is_json, 400
    
    #CHECK JSON CONTENT
    body = json.loads(request.body)

    if 'user' not in body:
        response_data = {}
        response_data['result'] = 'error'
        response_data['message'] = 'User is required'
        return response_data, 401
    elif 'password' not in body:
        response_data = {}
        response_data['result'] = 'error'
        response_data['message'] = 'Password is required'
        return response_data, 401

    #CHECK IF USER EXITST
    try:
        obj = ApiUsers.objects.get(user=body['user'])
    except ApiUsers.DoesNotExist:
        response_data ={}
        response_data['result'] = 'error'
        response_data['message'] = 'The user does not exist or the password is incorrect'
        return response_data, 401

    #TAKE PASSWORD OF THE USER
    hashed_password = obj.password
    #CHECK IF PASSWORD IS CORRECT
    if not check_password(body['password'],hashed_password) : 
        response_data ={}
        response_data['result'] = 'error'
        response_data['message'] = 'The user does not exist or the password is incorrect'
        return response_data, 401


    #CHECK IF USER HAS API-KEY
    if obj.api_key is None:
        obj.api_key = ApiKey().generate_key_complex()
        obj.save()

    #RETURN RESPONSE
    response_data['result'] = "success"
    response_data['message'] = "Valid credentials"
    response_data['userApiKey'] = obj.api_key

    return response_data, 200
