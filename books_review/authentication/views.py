from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import LoginForm, SignUpForm, FollowUserForm
from .models import User
from reviews.models import Ticket, Review, UserFollows


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


@login_required
def subscriptions(request):
    """Subscriptions page - following and followers management"""
    follow_form = FollowUserForm(current_user=request.user)
    
    if request.method == 'POST':
        follow_form = FollowUserForm(request.POST, current_user=request.user)
        if follow_form.is_valid():
            username = follow_form.cleaned_data['username']
            try:
                user_to_follow = User.objects.get(username=username)
                following, created = UserFollows.objects.get_or_create(
                    user=request.user,
                    followed_user=user_to_follow
                )
                if created:
                    messages.success(request, f'Vous suivez maintenant {user_to_follow.username}!')
                else:
                    messages.info(request, f'Vous suivez déjà {user_to_follow.username}.')
            except User.DoesNotExist:
                messages.error(request, 'Utilisateur introuvable.')
            
            return redirect('authentication:subscriptions')
    
    # Get users the current user is following
    following_users = User.objects.filter(
        followed_by__user=request.user
    ).order_by('username')
    
    # Get users who follow the current user
    followers = User.objects.filter(
        following__followed_user=request.user
    ).order_by('username')
    
    context = {
        'follow_form': follow_form,
        'following_users': following_users,
        'followers': followers,
    }
    
    return render(request, 'subscriptions.html', context)


@login_required
def unfollow_user(request, username):
    """Unfollow a user"""
    if request.method == 'POST':
        user_to_unfollow = get_object_or_404(User, username=username)
        try:
            following = UserFollows.objects.get(
                user=request.user,
                followed_user=user_to_unfollow
            )
            following.delete()
            messages.success(request, f'Vous ne suivez plus {user_to_unfollow.username}.')
        except UserFollows.DoesNotExist:
            messages.error(request, 'Vous ne suivez pas cet utilisateur.')
    
    return redirect('authentication:subscriptions')
