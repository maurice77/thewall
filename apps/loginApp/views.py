from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User, UserManager
from datetime import datetime
import bcrypt
from django.contrib import messages

DATE_FORMAT = "%Y-%m-%d"
SESSION_KEYS = [
    'id',
]

#SESSION
def resetSession(request):
    for key in SESSION_KEYS:
        if key in request.session:
            del request.session[key]
    request.session["id"] = 0 #initialize

def addCurrPostToSession(request):
    for key in SESSION_KEYS:
        if key in request.POST:
            request.session[key] = request.POST[key]
    request.session.save()

#CRUD
def addToDB(first_name,last_name,email,birth_date,password):
    user = User.objects.create(
        first_name = first_name,
        last_name = last_name,
        email = email,
        birth_date = birth_date,
        password = passEncryptDecoded(password),
    )
    return user.id

#MISC FUNCTIONS
def passEncryptDecoded(passwd):
    return bcrypt.hashpw(passwd.encode(),bcrypt.gensalt()).decode()

#ROUTES
def gotoLogin0(request):
    return redirect('/login')

def gotoLogin(request):

    if not("id" in request.session):
        resetSession(request)

    if request.session["id"] > 0:
        return redirect('/wall') #user is already logged in

    elif request.method == 'POST': #esto para evitar que se entre directo a esta ruta
            
            errors = User.objects.login_validator(request.POST)
            
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)

                    context = {
                        'email' : request.POST['email'],
                        'password' : request.POST['password']
                    }

                return render(request,'login.html',context)

            else:
                request.session["id"] = User.objects.get(email = request.POST["email"]).id
                return redirect('/wall')

    return render(request,'login.html') #GET method, i.e. first time in login


def showSuccess(request):

    if not("id" in request.session):
        resetSession(request)

    if request.session["id"] > 0:
        #context = {
        #    'user': User.objects.get(id = request.session["id"])
        #}
        return redirect('/wall')
        #return render(request,'success.html',context)
    else:
        return redirect('/login')

def gotoRegister(request):

    if request.method == 'POST': #esto para evitar que se entre directo a esta ruta
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value) 

            context = {
                'first_name' : request.POST['first_name'],
                'last_name' : request.POST['last_name'],
                'birth_date' : request.POST['birth_date'],
                'email' : request.POST['email'],
                'password' : request.POST['password'],
                'confirm_password' : request.POST['confirm_password'],
            }
            
            return render(request,'register.html',context) #go back to "register" keeping data

        else:
            id = addToDB(
                request.POST['first_name'],
                request.POST['last_name'],
                request.POST['email'],
                request.POST['birth_date'],
                request.POST['password']
            )
            messages.success(request, f"User {request.POST['first_name']} {request.POST['last_name']} successfully created!")
            
            request.session['id'] = id
            return redirect('/wall')
            #return redirect('/login') #when redirecting to login with session.id > 0 goes to success
    
    return render(request,'register.html') #Es GET (primera entrada)


def signOut(request):
    resetSession(request)
    print(f"sign out {request.session['id']}")
    return redirect('/login')

def checkEmail(request):
    errors = User.objects.email_validator(request.POST["email"],"register")
    return JsonResponse(errors)
