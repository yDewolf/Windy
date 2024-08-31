import utils.Login as ApiLogin
import utils.GameInteractions as ApiGameInteractions

import utils.classes.Session as Session
from utils.classes.DataHolder import DataHolder

default_gamedata_path: str = "data/gamedata.csv"
default_userdata_path: str = "data/userdata.csv"

data_holder: DataHolder = DataHolder(default_gamedata_path, default_userdata_path)

current_session = Session.start_session(data_holder)


def main_menu():
    for menuKey in menus:
        print(f"{menuKey}-{menus[menuKey]["name"]}")
    print(f"0-Quit")

    input_char: int = int(input())
    if input_char == 0:
        return -1
    
    menus[input_char]["callable"]()

def login_menu():
    username = input("Username: ")
    password = input("Password: ")
    current_session.session_login(username, password)

def sign_in_menu():
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    ApiLogin.sign_in(username, email, password, data_holder)
    current_session.session_login(username, password)

menus = {
    1: {
        "name": "Login Menu",
        "callable": login_menu
    },
    2: {
        "name": "Sign in Menu",
        "callable": sign_in_menu
    }
}


while True:
    #print(f"1-Login Menu\n2-Sign In Menu\n3-Look For Games\n0-Quit")
    if main_menu() == -1:
        break

    # match input_char:
    #     case 0:
    #         break
    #     case 1:
    #         username = input("Username: ")
    #         password = input("Password: ")
    #         current_session.session_login(username, password)
    #     case 2:
    #         username = input("Username: ")
    #         password = input("Password: ")
    #         email = input("Email: ")
    #         ApiLogin.sign_in(username, email, password, data_holder)
    #         current_session.session_login(username, password)
    #     case 3:
    #         if not current_session.online:
    #             print("You need to log in to see the games \n")
    #             continue
            
            
            # game_ids = ApiGameInteractions.get_games(data_holder)
            # games_by_idx = []
            # for game_id in game_ids:
            #     games_by_idx.append(game_id)
            #     game_info = ApiGameInteractions.get_game_info(game_id, data_holder)
            #     print(f"\nGame name: {game_info["name"]}\nID: {game_id}\nPrice: {game_info["price"]}")
            
            # for i in range(len(games_by_idx)):
            #     game_info = ApiGameInteractions.get_game_info(games_by_idx[i], data_holder)
            #     print(f"Type {i} to buy {game_info["name"]}\n")
            
            # selected_game_idx = int(input())
            # if selected_game_idx > 0 and selected_game_idx < len(games_by_idx):
            #     if input("Confirm purchase? Y/N").lower() == 'N':
            #         continue
            
            # ApiGameInteractions.purchase_game(games_by_idx[int(input())], current_session.user_data, data_holder)
