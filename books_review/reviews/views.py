from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review


@login_required
def home(request):
    """Home page showing all tickets and reviews"""
    # Get all tickets and reviews
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    
    # Create a combined list of tickets and reviews for the feed
    feed_items = []
    
    for ticket in tickets:
        feed_items.append({
            'type': 'ticket',
            'object': ticket,
            'time_created': ticket.time_created
        })
    
    for review in reviews:
        feed_items.append({
            'type': 'review',
            'object': review,
            'time_created': review.time_created
        })
    
    # Sort by creation time (newest first)
    feed_items.sort(key=lambda x: x['time_created'], reverse=True)
    
    return render(request, 'reviews/home.html', {'feed_items': feed_items})


# Ticket CRUD Views
@login_required
def create_ticket(request):
    """Create a new ticket"""
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Ticket créé avec succès!')
            return redirect('reviews:home')
    else:
        form = TicketForm()
    
    return render(request, 'reviews/ticket_form.html', {'form': form, 'action': 'Créer'})


@login_required
def edit_ticket(request, ticket_id):
    """Edit an existing ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Only allow the owner to edit their ticket
    if ticket.user != request.user:
        messages.error(request, 'Vous ne pouvez modifier que vos propres tickets.')
        return redirect('reviews:home')
    
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket modifié avec succès!')
            return redirect('reviews:home')
    else:
        form = TicketForm(instance=ticket)
    
    return render(request, 'reviews/ticket_form.html', {
        'form': form, 
        'action': 'Modifier', 
        'ticket': ticket
    })


@login_required
def delete_ticket(request, ticket_id):
    """Delete a ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Only allow the owner to delete their ticket
    if ticket.user != request.user:
        messages.error(request, 'Vous ne pouvez supprimer que vos propres tickets.')
        return redirect('reviews:home')
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket supprimé avec succès!')
        return redirect('reviews:home')
    
    return render(request, 'reviews/confirm_delete.html', {
        'object': ticket,
        'object_type': 'ticket'
    })


# Review CRUD Views
@login_required
def create_review(request, ticket_id):
    """Create a review for a ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check if user already reviewed this ticket
    existing_review = Review.objects.filter(ticket=ticket, user=request.user).first()
    if existing_review:
        messages.warning(request, 'Vous avez déjà écrit une critique pour ce ticket.')
        return redirect('reviews:home')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, 'Critique créée avec succès!')
            return redirect('reviews:home')
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/review_form.html', {
        'form': form, 
        'action': 'Créer', 
        'ticket': ticket
    })


@login_required
def edit_review(request, review_id):
    """Edit an existing review"""
    review = get_object_or_404(Review, id=review_id)
    
    # Only allow the owner to edit their review
    if review.user != request.user:
        messages.error(request, 'Vous ne pouvez modifier que vos propres critiques.')
        return redirect('reviews:home')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Critique modifiée avec succès!')
            return redirect('reviews:home')
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/review_form.html', {
        'form': form, 
        'action': 'Modifier', 
        'review': review,
        'ticket': review.ticket
    })


@login_required
def delete_review(request, review_id):
    """Delete a review"""
    review = get_object_or_404(Review, id=review_id)
    
    # Only allow the owner to delete their review
    if review.user != request.user:
        messages.error(request, 'Vous ne pouvez supprimer que vos propres critiques.')
        return redirect('reviews:home')
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Critique supprimée avec succès!')
        return redirect('reviews:home')
    
    return render(request, 'reviews/confirm_delete.html', {
        'object': review,
        'object_type': 'critique'
    })
