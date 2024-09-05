import random
from utils.classes.DataHolder import DataHolder
import utils.CsvReader as CsvReader

import framework.PrintFramework as PrintFramework
from framework.PrintFramework import Colors

# Inserts a new game to the user data / csv
def purchase_game(game_id: int, user_data: dict, data_holder: DataHolder):
    if check_bought(game_id, user_data):
        return False

    user_data["library"].append(game_id)
    data_holder.users_data[user_data["id"]]["library"].append(game_id)
    CsvReader.overwrite_data(data_holder.users_data, data_holder.userdata_path)
    return True

# Inserts a new game on the games data / csv
def publish_game(name: str, description: str, price: float, user_data: dict, data_holder: DataHolder):
    # Add new game to the database
    game_id = random.randrange(0, 65535)
    #game_info["id"] = game_id

    game_info = {
        "id": game_id,
        "name": name,
        "description": description,
        "developer": user_data["id"],
        "publisher": user_data["id"],
        "price": price
    }
    data_holder.games_data[game_id] = game_info
    CsvReader.append_data(game_info, data_holder.gamedata_path)

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


def check_bought(game_id, user_data: dict):
    user_library: list = user_data["library"]
    if user_library.count(game_id) != 0:
        #PrintFramework.custom_print("This game is already in your library", Colors.WARNING)
        return True
    
    return False
