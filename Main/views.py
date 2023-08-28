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
                      'all_tags': [tag.name for tag in Tag.objects.all()],
                      'image_parts': [part.to_dict() for part in card.imagepart_set.all()],
                  })


def create_card(request):
    return render(request, 'card_detail.html',
                  {
                      'card': None,
                      'tags': [],
                      'all_tags': [tag.name for tag in Tag.objects.all()],
                      'image_parts': []
                  })


def create_card_from_card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    return render(request, 'card_detail.html',
                  {
                      'card': None,
                      'tags': [tag.name for tag in card.tags.all()],
                      'all_tags': [tag.name for tag in Tag.objects.all()],
                      'image_parts': []
                  })


def delete_card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    card.delete()
    return redirect('card_list')


def save_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        card_id = data.get('card_id', None)
        title = data.get('title', 'base')
        description = data.get('description', None)
        tags = data.get('tags', None)
        content_data = data.get('content', None)
        card_type = data.get('card_type', None)  # може бути "image" або "video"
        image_parts = data.get('image_parts', None)

        logging.info(f'card_id: {card_id}; title: {title}; description: {description}; tags: {tags} image_parts: {image_parts}')

        if card_id:
            card = get_object_or_404(Card, id=card_id)
        else:
            card = Card()

        card.title = title
        card.description = description
        card.type = 1 if card_type == "image" else 2

        if content_data:
            format, content_str = content_data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(content_str), name='temp.' + ext)

            if card_type == "image":
                card.image.save(str(uuid.uuid4()), data, save=True)
            elif card_type == "video":
                card.video.save(str(uuid.uuid4()), data, save=True)
        else:
            if not card_id:
                return JsonResponse({"message": "Content (image or video) is required."}, status=400)

        card.save()

        tags = [tag.strip() for tag in tags]
        tags = Tag.objects.filter(name__in=tags)
        card.tags.clear()
        card.add_tags_and_parents(tags)

        if card_type == "image":
            # Image parts tags validation
            for image_part_dct in image_parts:
                image_part_tags = image_part_dct['tags']
                image_part_tags = [tag.strip() for tag in image_part_tags]
                logging.info(f'image_part_tags: {image_part_tags}')

                for tag_got in image_part_tags:
                    tag = Tag.objects.filter(name=tag_got).first()
                    logging.info(f'tag: {tag_got} {tag}')
                    if not tag:
                        return JsonResponse({"message": f"Tag '{tag_got}' does not exist."}, status=400)

            # Delete old image parts
            card.imagepart_set.all().delete()

            added_parts = 0
            for image_part_dct in image_parts:
                image_part = ImagePart()
                image_part.card = card
                image_part.start_x = image_part_dct['start_x']
                image_part.start_y = image_part_dct['start_y']
                image_part.width = image_part_dct['width']
                image_part.height = image_part_dct['height']

                image_part.save()

                image_part_tags = image_part_dct['tags']
                image_part_tags = [tag.strip() for tag in image_part_tags]
                image_part_tags = Tag.objects.filter(name__in=image_part_tags)
                image_part.tags.add(*image_part_tags)
                added_parts += 1

            logging.info(f'added_parts: {added_parts}')

        # logging.info(f'card_id: {card_id}; title: {title}; description: {description}; tags: {tags}; image: {card.image.url}')
        return JsonResponse({"saved": True, "message": "Card saved successfully.", "card_id": card.id}, status=200)


def card_list(request):
    tags = request.GET.get('tags', None)
    cards_amount = request.GET.get('cards_amount', 10)  # Default
    page = request.GET.get('page', 1)  # Default is first page

    # Get all cards
    cards = Card.objects.all().order_by('-created_at')

    # Filter cards by tags if tags are provided
    if tags:
        tags = tags.split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        for tag in tags:
            cards = cards.filter(tags__name=tag)

    # Create paginator
    paginator = Paginator(cards, cards_amount)
    cards = paginator.get_page(page)

    # Page numbers range
    page_range = list(paginator.page_range)[max(0, cards.number - 3):min(cards.paginator.num_pages, cards.number + 2)]

    return render(request, 'card_list.html', {'cards': cards, 'page_range': page_range, 'all_tags': [tag.name for tag in Tag.objects.all()], 'tags_string': ','.join(tags) if tags else ''})
