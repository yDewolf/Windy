import random
#import api.classes.fake_database as FakeDB
from api.classes.fake_database import FakeDatabase

def purchase_game(game_id: int, user_data: dict, fake_database: FakeDatabase):
    if user_data["library"].has(game_id):
        print("WARNING: Game is already purchased")
        return -1

    user_data["library"].append(game_id)
    fake_database.users[user_data["id"]]["library"].append(game_id)

def publish_game(game_info: dict, fake_database: FakeDatabase):
    # Add new game to the database
    game_id = random.randrange(0, 65535)
    game_info["id"] = game_id

    fake_database.games[game_id] = game_info


def get_games(fake_database: FakeDatabase) -> list:
    # Get all games in the database
    if len(fake_database.games) <= 0:
        return []

    games = []
    for id in fake_database.games.keys():
        games.append(id)
    
    return games

def get_game_info(game_id: int, fake_database: FakeDatabase) -> dict:
    # Get game info from database using id

    return fake_database.games[game_id]

    #game_info = {
    #    "name": "",
    #    "id": 0,
    #    "description": "",
    #    "price": 0.0,
    #}

    #return game_info
