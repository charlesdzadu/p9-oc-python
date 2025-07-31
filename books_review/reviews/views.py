from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TicketForm, ReviewForm, TicketReviewForm
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
def create_standalone_review(request):
    """Create a review with its own ticket (standalone review)"""
    if request.method == 'POST':
        form = TicketReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the ticket first
            ticket = Ticket.objects.create(
                title=form.cleaned_data['ticket_title'],
                description=form.cleaned_data['ticket_description'],
                image=form.cleaned_data['ticket_image'],
                user=request.user
            )
            
            # Create the review
            review = Review.objects.create(
                ticket=ticket,
                headline=form.cleaned_data['review_headline'],
                rating=form.cleaned_data['review_rating'],
                body=form.cleaned_data['review_body'],
                user=request.user
            )
            
            messages.success(request, 'Critique créée avec succès!')
            return redirect('reviews:home')
    else:
        form = TicketReviewForm()
    
    return render(request, 'reviews/ticket_review_form.html', {
        'form': form,
        'action': 'Créer'
    })


@login_required
def edit_review(request, review_id):
    """Edit an existing review"""
    review = get_object_or_404(Review, id=review_id)
    
    # Only allow the owner to edit their review
    if review.user != request.user:
        messages.error(request, 'Vous ne pouvez modifier que vos propres critiques.')
        return redirect('reviews:home')
    
    # Check if user also owns the ticket to allow editing both
    can_edit_ticket = review.ticket.user == request.user
    
    if can_edit_ticket:
        # Use combined form if user owns both ticket and review
        if request.method == 'POST':
            form = TicketReviewForm(request.POST, request.FILES, review_instance=review)
            if form.is_valid():
                # Update the ticket
                ticket = review.ticket
                ticket.title = form.cleaned_data['ticket_title']
                ticket.description = form.cleaned_data['ticket_description']
                if form.cleaned_data['ticket_image']:
                    ticket.image = form.cleaned_data['ticket_image']
                ticket.save()
                
                # Update the review
                review.headline = form.cleaned_data['review_headline']
                review.rating = form.cleaned_data['review_rating']
                review.body = form.cleaned_data['review_body']
                review.save()
                
                messages.success(request, 'Critique modifiée avec succès!')
                return redirect('reviews:home')
        else:
            form = TicketReviewForm(review_instance=review)
        
        return render(request, 'reviews/ticket_review_form.html', {
            'form': form,
            'action': 'Modifier',
            'review': review,
            'ticket': review.ticket
        })
    else:
        # Use regular review form if user doesn't own the ticket
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
