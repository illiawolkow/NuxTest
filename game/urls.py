from django.urls import path

from .views import GamePlayView, GameHistoryView

urlpatterns = [
    path('play', GamePlayView.as_view(), name='game-play'),
    path('history', GameHistoryView.as_view(), name='game-history'),
] 