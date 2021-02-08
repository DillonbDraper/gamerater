from raterapi.models.categories import Category
from raterapi.models.games import Game
from django.db import models
from django.db.models.fields.related import ForeignKey


class GameCategory(models.Model):

    game = ForeignKey(Game, on_delete=models.CASCADE)
    category = ForeignKey(Category, on_delete=models.CASCADE)

