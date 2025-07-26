from django.db import models
from django.contrib.auth.models import User


class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_results")
    number = models.PositiveIntegerField()
    result = models.CharField(max_length=4, choices=[("win", "Win"), ("lose", "Lose")])
    prize = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.number} -> {self.result}" 