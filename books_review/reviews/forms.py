from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': 'Titre du livre ou article'
        })
    )
    description = forms.CharField(
        max_length=2048,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': 'Description (optionnelle)',
            'rows': 4
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (0, '0 étoile'),
        (1, '1 étoile'),
        (2, '2 étoiles'),
        (3, '3 étoiles'),
        (4, '4 étoiles'),
        (5, '5 étoiles'),
    ]

    headline = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': 'Titre de votre critique'
        })
    )
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-radio text-primary-600 focus:ring-primary-500'
        })
    )
    body = forms.CharField(
        max_length=8192,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': 'Votre critique (optionnelle)',
            'rows': 6
        })
    )

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body'] 