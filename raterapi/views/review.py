from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game, Category, GameCategory, Review, Player

class Reviews(ViewSet):
    
    def create(self, request):
        """Handle POST operations for games

        Returns:
            Response -- JSON serialized game instance
        """

        review = Review()
        review.body = request.data["body"]
        review.game = Game.objects.get(pk=request.data["game"])
        review.player = Player.objects.get(pk=request.data["player"])
            


        try:
            review.save()
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
  
    
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'body', 'player', 'game')