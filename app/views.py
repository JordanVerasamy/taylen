import json
import logging
import uuid

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.bot import handle_slack
from app.models import Emoji, EmojiMatch

logger = logging.getLogger('default')


def ping(request: HttpRequest):
    return HttpResponse("pong")


def emoji_tree(request: HttpRequest):
    # Nodes: {id: 0, "label": "Myriel", "group": 1},
    # Edges: {"from": 1, "to": 0},
    nodes = [{
        'id': str(emoji.id),
        'label': emoji.name,
        'shape': 'image',
        'image': emoji.image_url,
        'group': 1
    } for emoji in Emoji.objects.all()]
    edges = [{"from": str(match.winner.id), "to": str(match.loser.id)} for match in
             EmojiMatch.objects.exclude(tied=True).exclude(winner=None).exclude(loser=None).all()]
    return render(request, 'emoji_tree.html', {'nodes': nodes, 'edges': edges})


@csrf_exempt
def slack(request: HttpRequest):
    logger.info(f"[request.body=${request.body}]")
    body = json.loads(request.body)
    if body['token'] != settings.SLACK_EVENTS_TOKEN:
        raise HttpResponseForbidden
    if body.get('type') == 'url_verification':
        return HttpResponse(body['challenge'])

    # Events are often sent multiple times from slack, so we avoid double
    # processing by using redis. I should probably be using something like
    # https://redis.io/commands/setnx but this is fine for now. Possibly not
    # correct though.
    event_id = body['event_id']
    uid = uuid.uuid4()
    if cache.get_or_set(event_id, lambda: uid, stale_cache_timeout=0) != uid:
        return JsonResponse({'ok': True})

    event = body.get('event')
    if event.get('type') == 'message':
        handle_slack(event)

    return JsonResponse({'ok': True})
