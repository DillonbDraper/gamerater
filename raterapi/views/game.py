from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game, Category, GameCategory


class Games(ViewSet):

    def create(self, request):
        """Handle POST operations for games

        Returns:
            Response -- JSON serialized game instance
        """

        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.num_of_players = request.data["num_of_players"]
        game.time_to_beat = request.data["time_to_beat"]
        game.release_year = request.data["release_year"]
        game.esrb_rating = request.data["esrb_rating"]
        


        try:
            game.save()
            game_category=GameCategory()
            category = Category.objects.get(pk=request.data['category'])
            game_category.category = category
            game_category.game = game
            game_category.save()
            serializer = TestSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        # try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
        game = Game.objects.get(pk=pk)
        game.categories = Category.objects.filter(games__game=game)
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)
        # except Exception as ex:
            # return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        games = Game.objects.all()

        for game in games:
            game.categories = Category.objects.filter(games__game=game)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GameCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('label',)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    categories=GameCategoriesSerializer(many=True)
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'release_year', 'num_of_players', 'time_to_beat', 'esrb_rating', 'categories')

class TestSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'release_year', 'num_of_players', 'time_to_beat', 'esrb_rating', )