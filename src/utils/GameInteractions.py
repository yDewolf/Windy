import random
from utils.classes.DataHolder import DataHolder

def purchase_game(game_id: int, user_data: dict, data_holder: DataHolder):
    if user_data["library"].has(game_id):
        print("WARNING: Game is already purchased")
        return -1

    user_data["library"].append(game_id)
    data_holder.users_data[user_data["id"]]["library"].append(game_id)

def publish_game(game_info: dict, data_holder: DataHolder):
    # Add new game to the database
    game_id = random.randrange(0, 65535)
    game_info["id"] = game_id

    data_holder.games_data[game_id] = game_info


def get_games(data_holder: DataHolder) -> list:
    # Get all games in the database
    if len(data_holder.games_data) <= 0:
        return []

    games = []
    for id in data_holder.games_data.keys():
        games.append(id)
    
    return games

def get_game_info(game_id: int, data_holder: DataHolder) -> dict:
    # Get game info from database using id

    return data_holder.games_data[game_id]
