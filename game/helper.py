from .models import Game, GameMatrix
from channels.db import database_sync_to_async
import json

@database_sync_to_async
def initialize_game(game_code, game_matrix_id, player_name, player_type):
    game_matrix = GameMatrix.objects.get(id=game_matrix_id)
    if player_type == 'null':
        game = Game.objects.create(game_code=game_code, game_creator=player_name, game_matrix=game_matrix)
        return game.id
    elif player_type == 'on':
        Game.objects.filter(game_code=game_code).update(game_opponent=player_name)
        return game.id

@database_sync_to_async
def modify_matrix(matrix_id, box_id, player_type):
    game_matrix_map = GameMatrix.objects.get(id=matrix_id).get_map()
    box_id = int(box_id) - 1
    game_matrix_map[box_id] = 44 if player_type == 'null' else 11
    GameMatrix.objects.filter(id=matrix_id).update(matrix_map=json.dumps(game_matrix_map))

@database_sync_to_async
def determine_winner(matrix_id):
    base_map = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    gm_map = GameMatrix.objects.get(id=matrix_id).get_map()
    
    win_conditions = [
        (gm_map[0], gm_map[1], gm_map[2]),
        (gm_map[3], gm_map[4], gm_map[5]),
        (gm_map[6], gm_map[7], gm_map[8]),
        (gm_map[0], gm_map[3], gm_map[6]),
        (gm_map[1], gm_map[4], gm_map[7]),
        (gm_map[2], gm_map[5], gm_map[8]),
        (gm_map[0], gm_map[4], gm_map[8]),
        (gm_map[2], gm_map[4], gm_map[6]),
    ]
    
    for condition in win_conditions:
        if all(x == 11 for x in condition):
            return 11
        elif all(x == 44 for x in condition):
            return 44
            
    return any(element in gm_map for element in base_map)
