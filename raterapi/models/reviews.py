from raterapi.models.players import Player
from raterapi.models.games import Game
from django.db import models
from django.db.models.fields.related import ForeignKey


class Review(models.Model):

    body = models.CharField(max_length=5000)
    player = ForeignKey(Player, on_delete=models.CASCADE)
    game = ForeignKey(Game, on_delete=models.CASCADE)
