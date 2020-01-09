import datetime
import uuid

from django.db import models


class User(models.Model):
    id: uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    friendly_name: str = models.CharField(max_length=30)
    slack_id: str = models.CharField(max_length=30, unique=True)
    splitwise_id: str = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.friendly_name


class Emoji(models.Model):
    id: uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: str = models.CharField(max_length=100, unique=True)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EmojiMatch(models.Model):
    id: uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first: Emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='first_emojis')
    first_votes: int = models.IntegerField(null=True, blank=True)

    second: Emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='second_emojis')
    second_votes: int = models.IntegerField(null=True, blank=True)

    winner: Emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='winning_matches', null=True,
                                      blank=True)
    loser: Emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='losing_matches', null=True,
                                     blank=True)

    slack_channel: str = models.CharField(max_length=30)
    slack_ts: str = models.CharField(max_length=30)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first} vs {self.second}"
