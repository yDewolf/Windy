import random
from utils.classes.DataHolder import DataHolder
import utils.DataManager as DataManager

import framework.PrintFramework as PrintFramework
from framework.PrintFramework import Colors

# Inserts a new game to the user data / csv
def purchase_game(game_id: int, user_data: dict, data_holder: DataHolder):
    user_library: list = user_data["library"]
    if user_library.count(game_id) != 0:
        PrintFramework.custom_print("This game is already in your library", Colors.WARNING)
        return -1

    user_data["library"].append(game_id)
    data_holder.users_data[user_data["id"]]["library"].append(game_id)
    DataManager.overwrite_data(data_holder.users_data, data_holder.userdata_path)

# Inserts a new game on the games data / csv
def publish_game(game_info: dict, data_holder: DataHolder):
    # Add new game to the database
    game_id = random.randrange(0, 65535)
    game_info["id"] = game_id

    data_holder.games_data[game_id] = game_info

# Returns all games listed on the DataHolder
def get_games(data_holder: DataHolder) -> list:
    # Get all games in the database
    if len(data_holder.games_data) <= 0:
        return []

    games = []
    for id in data_holder.games_data.keys():
        games.append(id)
    
    return games

# Returns the selected game info using game_id
def get_game_info(game_id: int, data_holder: DataHolder) -> dict:
    # Get game info from database using id

    return data_holder.games_data[game_id]


