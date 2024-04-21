from django.shortcuts import render, HttpResponse
from .forms import PlayerForm
from .models import GameMatrix
import random

def home(request):
    unique_code = str(random.randint(111111, 999999))
    player_form = PlayerForm(initial={'game_code': unique_code})
    return render(request, 'game/index.html', {'player_form': player_form})

def play(request):
    game_matrix_instance, _ = GameMatrix.objects.get_or_create(game_code=request.POST.get('game_code'))
    matrix_id = game_matrix_instance.id
    if request.method == 'POST':
        player_data = {
            'player_name': request.POST.get('player_name'),
            'game_code': request.POST.get('game_code'),
            'i_have_game_code': request.POST.get('i_have_game_code'),
            'game_matrix_id': matrix_id,
        }
        return render(request, 'game/game.html', player_data)
    return HttpResponse('<h1>Invalid Request...</h1>')
