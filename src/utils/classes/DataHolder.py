from utils.DataManager import load_data

class DataHolder:
    gamedata_path: str
    userdata_path: str

    games_data: dict
    users_data: dict

    def __init__(self, gamed_path: str, userd_path: str) -> None:
        self.gamedata_path = gamed_path
        self.userdata_path = userd_path
        
        self.games_data = load_gamedata(gamed_path)
        self.users_data = load_userdata(userd_path)


def load_userdata(data_path: str, debug=True) -> dict:
    users_data = load_data(data_path)
    userdata = {}


    for data in users_data:
        if debug:
            print(f"'\033[92m'\nParsing data: {data}\nCurrent userdata: {userdata}\n'\033[0m'")
        userdata[int(data["id"])] = {
            "username": data["username"],
            "password": data["password"],
            "email": data["email"],
            "library": data["library"]
        }

    return userdata

def load_gamedata(data_path: str, debug=True) -> dict:
    games_data = load_data(data_path)
    gamedata = {}

    for data in games_data:
        if debug:
            print(f"'\033[92m'\nParsing data: {data}\nCurrent gamedata: {gamedata}\n'\033[0m'")

        gamedata[int(data["id"])] = {
            "name": data["name"],
            "description": data["description"],
            "price": data["price"]
        }
    
    return gamedata
