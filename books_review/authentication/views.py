from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, SignUpForm
from reviews.models import Ticket, Review


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
    """Dashboard view showing user's own tickets and reviews"""
    # Get user's tickets and reviews
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    
    # Create a combined list of user's posts
    user_posts = []
    
    for ticket in user_tickets:
        user_posts.append({
            'type': 'ticket',
            'object': ticket,
            'time_created': ticket.time_created
        })
    
    for review in user_reviews:
        user_posts.append({
            'type': 'review',
            'object': review,
            'time_created': review.time_created
        })
    
    # Sort by creation time (newest first)
    user_posts.sort(key=lambda x: x['time_created'], reverse=True)
    
    return render(request, 'dashboard.html', {'user_posts': user_posts})
