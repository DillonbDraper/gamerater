from django.db import models
from django.db.models.fields.related import ForeignKey
from raterapi.models.players import Player


class Rating(models.Model):

    rating = models.IntegerField()
    player = ForeignKey(Player, on_delete=models.CASCADE)
    game = ForeignKey("Game", on_delete=models.CASCADE)

