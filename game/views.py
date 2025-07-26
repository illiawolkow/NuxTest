from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import GameResult
from .serializers import GameResultSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from drf_spectacular.utils import extend_schema
from .serializers import GamePlayInputSerializer


def calculate_prize(number: int) -> float:
    if number > 900:
        return number * 0.7
    elif number > 600:
        return number * 0.5
    elif number > 300:
        return number * 0.3
    else:
        return number * 0.1


@method_decorator(csrf_exempt, name='dispatch')
class GamePlayView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=GamePlayInputSerializer, responses=GameResultSerializer)
    def post(self, request, *args, **kwargs):
        number = request.data.get("number")
        try:
            number = int(number)
        except (TypeError, ValueError):
            return Response({"detail": "Invalid number"}, status=status.HTTP_400_BAD_REQUEST)

        result = "win" if number % 2 == 0 else "lose"
        prize = calculate_prize(number) if result == "win" else None

        game_result = GameResult.objects.create(
            user=request.user,
            number=number,
            result=result,
            prize=prize,
        )

        # Send result over websocket to the user-specific group
        channel_layer = get_channel_layer()
        group_name = f"user_{request.user.id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "game.result",
                "content": GameResultSerializer(game_result).data,
            },
        )

        return Response(GameResultSerializer(game_result).data, status=status.HTTP_201_CREATED)


class GameHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        results = GameResult.objects.filter(user=request.user)[:3]
        serializer = GameResultSerializer(results, many=True)
        return Response(serializer.data) 