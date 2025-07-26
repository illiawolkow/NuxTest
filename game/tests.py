from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status

from .views import calculate_prize
from .models import GameResult


class PrizeCalculationTests(TestCase):
    def test_prize_calculation(self):
        self.assertEqual(calculate_prize(950), 665.0)
        self.assertEqual(calculate_prize(700), 350.0)
        self.assertEqual(calculate_prize(450), 135.0)
        self.assertEqual(calculate_prize(200), 20.0)


@override_settings(
    CHANNEL_LAYERS={
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }
)
class GamePlayAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="tester@example.com", password="strongpass123")
        self.client = APIClient()
        self.client.login(username="tester", password="strongpass123")
        self.url_play = "/api/game/play"
        self.url_history = "/api/game/history"

    def test_even_number_win(self):
        response = self.client.post(self.url_play, {"number": 842}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data["result"], "win")
        self.assertAlmostEqual(float(data["prize"]), 421.0)
        self.assertEqual(GameResult.objects.count(), 1)

    def test_odd_number_lose(self):
        response = self.client.post(self.url_play, {"number": 123}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data["result"], "lose")
        self.assertIsNone(data["prize"])
        self.assertEqual(GameResult.objects.count(), 1)

    def test_history_endpoint(self):
        # create 4 results
        for n in [100, 200, 300, 400]:
            self.client.post(self.url_play, {"number": n}, format="json")
        response = self.client.get(self.url_history)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 3)  # last 3 results
        self.assertEqual(data[0]["number"], 400) 