from raterapi.models.players import Player
from raterapi.models.games import Game
from django.db import models
from django.db.models.fields.related import ForeignKey


class Picture(models.Model):

    photo = models.CharField(max_length=250)
    player = ForeignKey(Player, on_delete=models.CASCADE)
    game = ForeignKey(Game, on_delete=models.CASCADE)

