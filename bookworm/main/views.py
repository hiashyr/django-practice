from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib import messages

def home(request):
	return render(request, 'home.html')

def catalog(request):
	return render(request, 'catalog.html')

def contact(request):
	return render(request, 'contact.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            else:
                form.add_error(None, 'Неверный логин или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            patronymic = form.cleaned_data['patronymic']
            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=login).exists() or User.objects.filter(email=email).exists():
                form.add_error(None, 'Пользователь с таким логином или email уже существует')
            else:
                user = User.objects.create_user(username=login, email=email, password=password)
                user.first_name = name
                user.last_name = surname
                user.save()
                return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
