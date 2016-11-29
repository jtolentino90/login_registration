from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    print ('*'*100)
    return render (request, 'login_reg/index.html')

def register(request):
    result = User.objects.val_reg(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('index'))
    return log_user_in(request, result[1])

def login(request):
    result = User.objects.val_login(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('index'))
    return log_user_in(request, result[1])

def success(request):
    if not 'user' in request.session:
        return redirect(reverse['index'])
    return render(request, 'login_reg/success.html')

def logout(request):
    request.session.pop('user')
    return redirect(reverse('index'))


def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.INFO, message)
def log_user_in(request, user):
    request.session['user'] = {
        'id': user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    return redirect(reverse('success'))
