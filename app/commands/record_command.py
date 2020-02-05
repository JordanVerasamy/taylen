import logging

from django.core.exceptions import ObjectDoesNotExist

from app.models import Emoji
from app.slack.slack_client import SlackClient

logger = logging.getLogger('default')

help_message = """```
The bot will respond with the given emoji's record in the form {wins} {losses} {ties}.

Usage: 
> .record <emoji> <detail_level>

Arguments:
- emoji: an emoji
- detail_level: either nothing or "full"

Examples:
> .record :simple_smile:
> .record :simple_smile: full
```"""

number_map = {
    0: ':zero:',
    1: ':one:',
    2: ':two:',
    3: ':three:',
    4: ':four:',
    5: ':five:',
    6: ':six:',
    7: ':seven:',
    8: ':eight:',
    9: ':nine:'
}


class RecordCommand:
    @staticmethod
    async def handle_discord(message):
        logger.info("")

    @staticmethod
    def handle_slack(client: SlackClient, event: dict, emoji_name: str, detail_level: str = None):
        logger.info(f"[emoji_name={emoji_name}]")
        try:
            emoji = Emoji.objects.get(name=emoji_name)
            full_record = f' Defeated: {" ".join(emoji.defeated())}' if detail_level == 'full' else ''
            wins, losses, ties = emoji.record()
            client.post_message(event, f"{number_map.get(wins, wins)} {number_map.get(losses, losses)}"
                                       f" {number_map.get(ties, ties)} {full_record}")
        except ObjectDoesNotExist:
            client.post_message(event, 'Could not found that emoji sry')
