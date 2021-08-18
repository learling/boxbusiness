from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.conf import settings
from .models import *
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def register_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='customer'))
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    context = {}
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def users(request):
    User = get_user_model()
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'accounts/users.html', context)
