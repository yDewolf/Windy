
class DataHolder:
    gamedata_path: str
    userdata_path: str

    games_data: dict
    users_data: dict

    def __init__(self) -> None:
        self.games_data = {}
        self.users_data = {}