from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game, Category, GameCategory, Review, Player, Rating

class Ratings(ViewSet):
    def create(self, request):
        rating = Rating()

        rating.player = Player.objects.get(user = request.auth.user)
        rating.rating = request.data['rating']
        rating.game = Game.objects.get(pk=request.data['game'])

        try:
            rating.save()
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'rating', 'player', 'game', )
