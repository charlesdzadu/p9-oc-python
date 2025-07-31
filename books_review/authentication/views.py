from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, SignUpForm


@login_required
def home(request):
    """Redirect to reviews home page"""
    return redirect('reviews:home')


def register(request):
    """Registration page"""
    if request.user.is_authenticated:
        return redirect('reviews:home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé avec succès pour {username}!')
            login(request, user)
            return redirect('reviews:home')
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('reviews:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Bienvenue {user.username}!')
                return redirect('reviews:home')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    """Logout user and redirect to login"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('authentication:login')


@login_required
def dashboard(request):
    """Dashboard view for authenticated users"""
    return render(request, 'dashboard.html')
