import random
from utils.classes.DataHolder import DataHolder
import utils.CsvReader as CsvReader

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


def check_bought(game_id, user_data: dict):
    user_library: list = user_data["library"]
    if user_library.count(game_id) != 0:
        #PrintFramework.custom_print("This game is already in your library", Colors.WARNING)
        return True
    
    return False
