from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game, Category, GameCategory, Review, Player, reviews

class Reviews(ViewSet):
    
    def create(self, request):
        """Handle POST operations for games

        Returns:
            Response -- JSON serialized game instance
        """

        review = Review()
        review.body = request.data["body"]
        review.game = Game.objects.get(pk=request.data["game"])
        review.player = Player.objects.get(user=request.auth.user)
            


        try:
            review.save()
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, pk=None):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database

        reviews = Review.objects.all()


        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(selt, request, pk=None):

        reviews = Review.objects.filter(game=pk)

        for rev in reviews:
            rev.user = Player.objects.get(pk=rev.player.id).name

        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        review = Review.objects.get(pk=pk)
        review.body = request.data["body"]
        review.game = Game.objects.get(pk=request.data["game"])

        review.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  
    
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'body', 'player', 'game', 'user')