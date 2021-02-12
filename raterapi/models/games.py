from django.db import models


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

