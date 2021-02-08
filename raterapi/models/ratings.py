from raterapi.models.players import Player
from raterapi.models.games import Game
from django.db import models
from django.db.models.fields.related import ForeignKey


class Rating(models.Model):

    rating = models.IntegerField()
    player = ForeignKey(Player, on_delete=models.CASCADE)
    game = ForeignKey(Game, on_delete=models.CASCADE)

