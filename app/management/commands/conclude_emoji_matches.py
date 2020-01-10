from django.core.management.base import BaseCommand

from app.models import EmojiMatch
from app.src.slack.slack_client import client


class Command(BaseCommand):
    def handle(self, *args, **options):
        winning_emojis = []
        losing_emojis = []
        ties = []
        for match in EmojiMatch.objects.filter(winner=None, loser=None, tied=False).all():
            reactions = client.reactions_get(channel=match.slack_channel, timestamp=match.slack_ts)['message'][
                'reactions']
            reaction_to_count = {}
            for reaction in reactions:
                reaction_to_count[reaction['name']] = reaction['count']

            first_votes = reaction_to_count[match.first.name]
            second_votes = reaction_to_count[match.second.name]
            match.first_votes = first_votes
            match.second_votes = second_votes

            if first_votes > second_votes:
                winning_emojis.append(match.first)
                losing_emojis.append(match.second)
                match.winner = match.first
                match.loser = match.second
            elif first_votes < second_votes:
                winning_emojis.append(match.second)
                losing_emojis.append(match.first)
                match.winner = match.second
                match.loser = match.first
            else:
                ties.append(match.first)
                ties.append(match.second)
                match.tied = True

            match.save()

        text = '`Won:` '
        for emoji in winning_emojis:
            text += f':{emoji.name}: '

        text += '\n`Ded:` '
        for emoji in losing_emojis:
            text += f':{emoji.name}: '

        text += '\n`Tie:` '
        for emoji in ties:
            text += f':{emoji.name}: '

        client.chat_postMessage(channel='#emoji-fight', text=text)
