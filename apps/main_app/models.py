from django.db import models
import re
import bcrypt
from datetime import date
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

now = date.today().isoformat()

# Create your models here.
class UserManager(models.Manager):
    def registrationValidate(self, postData):
        error = {}
        #VALIDATE FIRST AND LAST NAME
        if len(postData['first_name']) < 3:
            error['first_name'] = 'Your first name must be longer than 3 characters'
        if not postData['first_name'].isalpha():
            error['first_name'] = 'Your name must only be alphabets'
        if len(postData['last_name']) < 1:
            error['last_name'] = 'Your last name must be longer than 3 characters'

        # VALIDATE FOR DOB
        if len(postData['dob']) < 1:
            error['dob'] = "Enter your DOB"
        if postData['dob'] > now:
            error['dob'] = "Your birthday must before today you walnut"
        
        #VALIDATE WITH EMAIL REGEX AND CHECK FOR DUPES
        if not EMAIL_REGEX.match(postData['email']):
            error['email'] = 'Your email must be in valid format'
        if User.objects.filter(email=postData['email']):
            error['emaildupe'] = 'Your email is already registered'
        
        #VALIDATE PASSWORD AND CONFIRM THAT PASSWORD AND C_PASSWORD MATCHES
        if len(postData['password']) < 8:
            error['password'] = 'Your password must be longer than 8 characters'
        if postData['password'] != postData['c_password']:
            error['passwordmatch'] = 'Your password and confirm passowrd does not match'
        return error

    def loginValidate(self, postData):
        error = {}
        #VALIDATE WITH REGEX AND CHECK FOR EMAIL IN DB
        if not EMAIL_REGEX.match(postData['email']):
            error['email'] = 'Your email must be in valid format'
    
        #CHECK IF PASSWORD GIVEN MATCHES THE PASSWORD IN DB
        if not User.objects.filter(email=postData['email']):
            error['loginemail'] = 'Email does not exist within DB'
            return error
        else:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                pass
            else:
                error['password'] = 'Your credentials do not match'
        return error

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(auto_now_add=False, auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()