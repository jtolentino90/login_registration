from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def val_reg(self, request):
        errors = self.val_input(request)

        if len(errors) > 0:
            return(False, errors)

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = self.create(first_name=request.POST['first'], last_name=request.POST['last'], email=request.POST['email'], pw_hash=pw_hash)

        return (True, user)

    def val_login(self, request):
        try:
            #checks to see if email matches one in database, then will test password
            user = User.objects.get(email=request.POST['email'])
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()):
                return (True, user)

        except ObjectDoesNotExist:
            pass

        return(False, ['Email & Password do not match!'])


    def val_input(self, request):
        #check to validate the form, provides errors/feedback to user if otherwise
        errors = []
        if len(request.POST['first']) < 2 or len(request.POST['last']) < 2:
            errors.append("Name is too short!")
        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append("Invalid email!")
        if len(request.POST['password']) < 5:
            errors.append("Password must be more than 5 characters long!")
        if request.POST['password'] != request.POST['password2']:
            errors.append("Passwords must match!")

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    pw_hash = models.CharField(max_length=40)

    objects = UserManager()
