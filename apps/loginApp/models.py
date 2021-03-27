
from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField, DateField, EmailField
from datetime import datetime
import bcrypt
import re #Regex

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def strToDate(dateString):
    return datetime(int(dateString[:4]),int(dateString[5:7]),int(dateString[-2:]))

def getDateStringXYearsAgo(dateString,xYears):
    #dateString format: YYYY-MM-DD
    year = dateString[:4]
    month = dateString[5:7]
    day = dateString[-2:]
    if day == "29" and month == "02":
        day == "28"
    return f"{int(year)-xYears}-{month}-{day}"

class UserManager(models.Manager):

    def full_name(self,id):
        user = self.get(id = id)
        return(f"{user.first_name} {user.last_name}")

    def chk_pass(self,email,passwd):
        user = self.filter(email = email)
        print(user)

        if user:
            return bcrypt.checkpw(passwd.encode(),user[0].password.encode())

        return False

    def email_exists(self,email):
        return self.filter(email = email)

    def email_validator(self,email,tipo): #'tipo: register o login'
        errors = {}
        if email == "":
            errors["email"] = "Email is required!"
        elif not EMAIL_REGEX.match(email):    # probar si un campo coincide con el patrón        
            errors["email"] = "Invalid email address!"
        elif tipo == "register":
            if self.email_exists(email):
                errors["email"] = "Email already exists in the DB!"

        return errors

    def login_validator(self,post_data): #para el login
        errors = {}

        field_name = "email"
        field_value = post_data["email"]
        if field_value == "":
            errors[field_name] = "Email is required!"
        
        #if not self.email_exists(field_value) or not self.chk_pass(post_data["password"]):
        if not self.chk_pass(post_data["email"],post_data["password"]): #esta rutina chequea la existencia del mail...
            errors[field_name] = "Incorrect email and/or password!"

        return errors

    def user_validator(self,post_data):
        errors = {}

        field_name = "first_name"
        field_value = post_data[field_name]
        if field_value == "":
            errors[field_name] = "First Name is required!"
        elif len(field_value)<2 or len(field_value)>100:
            errors[field_name] = "First Name must be between 2 and 100 characters."


        field_name = "last_name"
        field_value = post_data[field_name]
        if field_value == "":
            errors[field_name] = "Last Name is required!"
        elif len(field_value)<2 or len(field_value)>100:
            errors[field_name] = "Last Name must be between 2 and 100 characters."

        field_name = "email"
        field_value = post_data[field_name]
        email_errors = self.email_validator(field_value,"register")
        if email_errors:
            errors[field_name] = email_errors["email"]

        field_name = "birth_date"
        field_value = post_data[field_name]
        if not field_value:
            errors[field_name] = "Release Date is missing!"
        elif not ("1900-01-01" <= field_value <= datetime.now().strftime("%Y-%m-%d")):
            errors[field_name] = "Invalid date!"
        elif strToDate(getDateStringXYearsAgo(datetime.now().strftime("%Y-%m-%d"),13)) < strToDate(field_value):

            errors[field_name] = "User must be at least 13 years old!"

        field_name = "password"
        field_value = post_data[field_name]
        if field_value == "":
            errors[field_name] = "Password is required!"
        elif len(field_value)<8 or len(field_value)>50:
            errors[field_name] = "Password must be between 8 and 100 characters."
        elif post_data['confirm_password'] == "":
            errors["confirm_password"] = "Confirm password please!"
        elif field_value != post_data["confirm_password"]:
            errors["confirm_password"] = "Password and confirmation do not match. Please check!" 
        
        return errors

class User(models.Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = EmailField(max_length=100, unique = True)
    birth_date = DateField()
    password = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    #comments
    #messages

    objects = UserManager()


