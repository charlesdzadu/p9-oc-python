from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.home, name='home'),
    
    # Ticket URLs
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('tickets/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    
    # Review URLs
    path('reviews/create/', views.create_standalone_review, name='create_standalone_review'),
    path('tickets/<int:ticket_id>/review/', views.create_review, name='create_review'),
    path('reviews/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
] 