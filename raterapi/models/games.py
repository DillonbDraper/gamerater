from django.db import models
from .ratings import Rating


class Game(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, default="Game description")
    designer = models.CharField(max_length=100)
    release_year =  models.IntegerField()
    num_of_players = models.IntegerField()
    time_to_beat = models.TimeField()
    esrb_rating = models.CharField(max_length=20)

    @property
    def categories(self):
        return self.__categories

    @categories.setter
    def categories(self, value):
        self.__categories = value

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating

        average_rating = total_rating / len(ratings)
        return average_rating

        # Calculate the averge and return it.
        # If you don't know how to calculate averge, Google it.