from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient


PLAY_URL = reverse("service:play-list")


class UnauthenticatedPlayApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):

        # k = PLAY_URL
        play = self.client.get(PLAY_URL)
        self.assertEqual(401, 401)
