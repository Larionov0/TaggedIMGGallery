from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Card, Tag


def card_list(request):
    tags = request.GET.get('tags', None)
    cards_amount = request.GET.get('cards_amount', 10)  # Default is 10 cards per page
    page = request.GET.get('page', 1)  # Default is first page

    # Get all cards
    cards = Card.objects.all()

    # Filter cards by tags if tags are provided
    if tags:
        tags = tags.split(',')
        cards = cards.filter(tags__name__in=tags)

    # Create paginator
    paginator = Paginator(cards, cards_amount)
    cards = paginator.get_page(page)

    return render(request, 'card_list.html', {'cards': cards})

