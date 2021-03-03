import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterapi.models import Game, Category, GameCategory, Review, Player
from django.contrib.auth.models import User


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "preferredName": "Steve"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        category = Category()
        category.label = "adventure"
        category.save()

        game = Game()
        game.title = "Zelda"
        game.description = "Old"
        game.designer = "Miyamoto"
        game.num_of_players = 1
        game.time_to_beat = "10:00:00"
        game.release_year = 1987
        game.esrb_rating = "E"
        game.save()

        game_category = GameCategory()
        game_category.game = game
        game_category.category = category
        game_category.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "title": "Super Mario Bros.",
            "description": "Platformer game",
            "designer": "Miyamoto",
            "release_year": 1986,
            "num_of_players": 1,
            "time_to_beat": "10:00:00",
            "esrb_rating": "E",
            "category": 1
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "Super Mario Bros.")
        self.assertEqual(json_response["description"], "Platformer game")
        self.assertEqual(json_response["designer"], "Miyamoto")
        self.assertEqual(json_response["release_year"], 1986)
        self.assertEqual(json_response["num_of_players"], 1)
        self.assertEqual(json_response["time_to_beat"], "10:00:00")
        self.assertEqual(json_response["esrb_rating"], "E")

    def test_rate_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/ratings"
        data = {
            "rating": 10,
            "game": 1,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["rating"], 10)
        self.assertEqual(json_response["game"], 1)
        


    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.title = "Pokemon"
        game.description = "Old"
        game.designer = "Japanese"
        game.num_of_players = 1
        game.time_to_beat = "10:00:00"
        game.release_year = 1995
        game.esrb_rating = "E"
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "title": "Pokemon Red",
            "description": "Catch em' All",
            "designer": "Sakaguchi",
            "num_of_players": 2,
            "time_to_beat": "12:00:00",
            "release_year": 1995,
            "esrb_rating": "eC"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "Pokemon Red")
        self.assertEqual(json_response["description"], "Catch em' All")
        self.assertEqual(json_response["designer"], "Sakaguchi")
        self.assertEqual(json_response["num_of_players"], 2)
        self.assertEqual(json_response["time_to_beat"], "12:00:00")
        self.assertEqual(json_response["release_year"], 1995)
        self.assertEqual(json_response["esrb_rating"], "eC")



    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.title = "Pokemon"
        game.description = "Old"
        game.designer = "Japanese"
        game.num_of_players = 1
        game.time_to_beat = "10:00:00"
        game.release_year = 1995
        game.esrb_rating = "E"
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    def test_get_single_game(self):

        game = Game()
        game.title = "Pokemon"
        game.description = "Old"
        game.designer = "Japanese"
        game.num_of_players = 1
        game.time_to_beat = "10:00:00"
        game.release_year = 1995
        game.esrb_rating = "E"
        game.save()
        

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(json_response["title"], "Pokemon")
        self.assertEqual(json_response["description"], "Old")
        self.assertEqual(json_response["designer"], "Japanese")
        self.assertEqual(json_response["num_of_players"], 1)
        self.assertEqual(json_response["time_to_beat"], "10:00:00")
        self.assertEqual(json_response["release_year"], 1995)
        self.assertEqual(json_response["esrb_rating"], "E")

    def test_all_games(self):

        game = Game()
        game.title = "Pokemon"
        game.description = "Old"
        game.designer = "Japanese"
        game.num_of_players = 1
        game.time_to_beat = "10:00:00"
        game.release_year = 1995
        game.esrb_rating = "E"
        game.save()
        

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/games")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[1]["title"], "Pokemon")
        self.assertEqual(json_response[1]["description"], "Old")
        self.assertEqual(json_response[1]["designer"], "Japanese")
        self.assertEqual(json_response[1]["num_of_players"], 1)
        self.assertEqual(json_response[1]["time_to_beat"], "10:00:00")
        self.assertEqual(json_response[1]["release_year"], 1995)
        self.assertEqual(json_response[1]["esrb_rating"], "E")

    def test_review_game(self):
        url = "/reviews"
        data = {
            "body": "Review body",
            "game": 1,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["body"], "Review body")
        self.assertEqual(json_response["game"], 1)

    def test_change_review(self):
      
        game = Game()
        game.title = "Pokemon"
        game.description = "Old"
        game.designer = "Japanese"
        game.num_of_players = 1
        game.time_to_beat = "10:00:00"
        game.release_year = 1995
        game.esrb_rating = "E"
        game.save()

        user = User()
        user.username = "dillon"
        user.email = "hi@gmail.com"
        user.password = "admin"
        user.address = "ssitja"
        user.phone_number = "555-2222"
        user.first_name = "dillon"
        user.last_name = "draper"
        user.save()

        player = Player()
        player.name = "Super Steve"
        player.user = user
        player.save()

        review = Review()
        review.body = "Body"
        review.game = game
        review.player = player
        review.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "body": "Smaller Body",
            "game": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/reviews/{review.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/reviews/{review.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response[0]["body"], "Smaller Body")
        # self.assertEqual(json_response["game"], 1)

        
