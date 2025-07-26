from rest_framework import serializers
from .models import GameResult


class GamePlayInputSerializer(serializers.Serializer):
    number = serializers.IntegerField(min_value=0, help_text="Number to play the game with")


class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = ["id", "number", "result", "prize", "created_at"] 