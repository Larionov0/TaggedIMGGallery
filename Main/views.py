from django.core.paginator import Paginator
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
import uuid
import json

logging.basicConfig(level=logging.INFO)


def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    return render(request, 'card_detail.html',
                  {
                      'card': card,
                      'tags': [tag.name for tag in card.tags.all()],
                      'all_tags': [tag.name for tag in Tag.objects.all()]
                  })


def save_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        card_id = data.get('card_id', None)
        title = data.get('title', 'base')
        description = data.get('description', None)
        tags = data.get('tags', None)
        image_data = data.get('image', None)

        logging.info(f'card_id: {card_id}; title: {title}; description: {description}; tags: {tags}')

        if card_id:
            card = get_object_or_404(Card, id=card_id)
        else:
            card = Card()

        card.title = title
        card.description = description

        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            card.image.save(str(uuid.uuid4()), data, save=True)
        else:
            if not card_id:
                return JsonResponse({"message": "Image is required."}, status=400)

        card.save()

        tags = [tag.strip() for tag in tags]
        tags = Tag.objects.filter(name__in=tags)
        card.tags.clear()
        card.add_tags_and_parents(tags)

        logging.info(f'card_id: {card_id}; title: {title}; description: {description}; tags: {tags}; image: {card.image.url}')
        return JsonResponse({"message": "Card saved successfully."}, status=200)


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

