from django.core.management.base import BaseCommand

from app.models import Emoji
from app.slack.slack_client import client


class Command(BaseCommand):
    def handle(self, *args, **options):
        emojis = client.emoji_list()['emoji']
        for emoji, url in emojis.items():
            try:
                e = Emoji.objects.get(name=emoji)
                e.image_url = url
                e.save()
            except:
                pass
