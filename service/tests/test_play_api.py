from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from service.models import Play, Actor, Genre
from service.serializers import PlaySerializer, PlayListSerializer, PlayDetailSerializer

PLAY_URL = reverse("service:play-list")


def detail_play(play_id: int):
    return reverse("service:play-detail", args=[play_id])


def template_play(**params):
    default = {
        "title": "Way",
        "description": "Film"
    }

    default.update(**params)

    return Play.objects.create(**default)


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        play = self.client.get(PLAY_URL)
        self.assertEqual(play.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@gmail.com"
            "test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_plays(self):
        template_play()

        response = self.client.get(PLAY_URL)

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_plays_by_actors(self):
        template_play_without_actor = template_play(title="The wolf")
        template_play_with_actor = template_play(title="The gun")

        actor = Actor.objects.create(
            first_name="Oleg",
            last_name="Gordienko"
        )

        template_play_with_actor.actors.add(actor)

        response = self.client.get(PLAY_URL, {"actors": f"{actor.id}"})

        serializer1 = PlayListSerializer(template_play_without_actor)
        serializer2 = PlayListSerializer(template_play_with_actor)

        self.assertNotIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)

    def test_list_plays_by_genres(self):
        template_play_without_genre = template_play(title="The wolf")
        template_play_with_genre = template_play(title="The gun")

        genre = Genre.objects.create(
            name="Comedy"
        )

        template_play_with_genre.genres.add(genre)

        response = self.client.get(PLAY_URL, {"genres": f"{genre.id}"})

        serializer1 = PlayListSerializer(template_play_without_genre)
        serializer2 = PlayListSerializer(template_play_with_genre)

        self.assertNotIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)

    def test_list_plays_by_genres_and_actors(self):
        template_play_without_genre_and_actor = template_play(title="The wolf")
        template_play_with_genre_and_actor = template_play(title="The gun")

        actor = Actor.objects.create(
            first_name="Oleg",
            last_name="Gordienko"
        )
        genre = Genre.objects.create(
            name="Comedy"
        )

        template_play_with_genre_and_actor.actors.add(actor)
        template_play_with_genre_and_actor.genres.add(genre)

        response = self.client.get(PLAY_URL, {"genres": f"{genre.id}", "actors": f"{actor.id}"})

        serializer1 = PlayListSerializer(template_play_without_genre_and_actor)
        serializer2 = PlayListSerializer(template_play_with_genre_and_actor)

        self.assertNotIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)

    def test_retrieve_play_detail(self):
        play = template_play()
        play.actors.add(Actor.objects.create(first_name="Oleg", last_name="Gordienko"))
        play.genres.add(Genre.objects.create(name="drama"))

        url = detail_play(play.id)

        response = self.client.get(url)

        serializer = PlayDetailSerializer(play)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_play(self):
        payload = {
            "title": "The film",
            "description": "The description"
        }

        response = self.client.post(PLAY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlatApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin1@gmail.com",
            "admin12345",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_play(self):
        payload = {
            "title": "The film",
            "description": "The description",
        }

        response = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(play, key))

    def test_create_play_with_actors(self):
        actor1 = Actor.objects.create(first_name="Oleg", last_name="Gordienko")
        actor2 = Actor.objects.create(first_name="John", last_name="Gordienko")

        payload = {
            "title": "The film",
            "description": "The description",
            "actors": [actor1.id, actor2.id]
        }

        response = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=response.data["id"])
        actors = play.actors.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(actor1, actors)
        self.assertIn(actor2, actors)

    def test_create_play_with_genres(self):
        genre1 = Genre.objects.create(name="Drama")
        genre2 = Genre.objects.create(name="comedy")

        payload = {
            "title": "The film",
            "description": "The description",
            "genres": [genre1.id, genre2.id]
        }

        response = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=response.data["id"])
        genres = play.genres.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(genre1, genres)
        self.assertIn(genre2, genres)

    def test_create_play_with_actors_and_genres(self):
        actor = Actor.objects.create(first_name="Oleg", last_name="Gordienko")
        genre = Genre.objects.create(name="comedy")

        payload = {
            "title": "The film",
            "description": "The description",
            "actors": [actor.id],
            "genres": [genre.id]
        }

        response = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=response.data["id"])
        actors = play.actors.all()
        genres = play.genres.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(actor, actors)
        self.assertIn(genre, genres)
