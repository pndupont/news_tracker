from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


def index(request):
    return redirect ('/login')


def login(request):
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')

def create_user(request):

    errors = User.objects.validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        this_user = User.objects.create(
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        username=request.POST['username'],
                                        email=request.POST['email'],
                                        password= request.POST['password'],
                                        )
        request.session['first_name'] = this_user.first_name
        request.session['last_name'] = this_user.last_name
        request.session['email'] = this_user.email
        request.session['username'] = this_user.username
        request.session['id'] = this_user.id
        messages.success(request, 'User Successfully Created')
        return redirect('/tracker/',)

def login_check(request):
    all_users = User.objects.all()
    is_user = False
    for user in all_users:
        if user.username == request.POST['username']:
            is_user = True
    if is_user == False:
        messages.error(request, 'User does not exist', request)
        return redirect('/')
    this_user = User.objects.get(username = request.POST['username'])
    if request.POST['password'] != this_user.password:
        messages.error(request, 'incorrect password')
        return redirect('/', request)
    request.session['first_name'] = this_user.first_name
    request.session['last_name'] = this_user.last_name
    request.session['email'] = this_user.email
    request.session['username'] = this_user.username
    request.session['id'] = this_user.id
    return redirect('/tracker/',)

def logout(request,):
    request.session.clear()
    return redirect('/')