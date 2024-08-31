import utils.Login as ApiLogin

import utils.classes.Session as Session
from utils.classes.DataHolder import DataHolder

import framework.MenuManager as MenuManager

import utils.GameInteractions as GameInteractions

import framework.PrintFramework as PrintFramework
from framework.PrintFramework import Colors

default_gamedata_path: str = "data/gamedata.csv"
default_userdata_path: str = "data/userdata.csv"

data_holder: DataHolder = DataHolder(default_gamedata_path, default_userdata_path)

current_session = Session.start_session(data_holder)


def main_menu():
    return MenuManager.option_menu(menus)


def login_menu():
    MenuManager.option_menu([{"name": "Main Menu", "callable": main_menu}], "Continue")

    username = input("Username: ")
    password = input("Password: ")
    current_session.session_login(username, password)


def sign_in_menu():
    MenuManager.option_menu([{"name": "Main Menu", "callable": main_menu}], "Continue")

    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    ApiLogin.sign_in(username, email, password, data_holder)
    current_session.session_login(username, password)


def game_catalog_menu():
    print("-----------------------")
    print("Games in Catalog:")

    buy_options: list[int] = []
    for gameId in data_holder.games_data:
        game_info = data_holder.games_data[gameId]
        PrintFramework.custom_print(f"\n--- {game_info["name"]} ---", Colors.HEADER)
        PrintFramework.custom_print(f"{game_info["description"]}", Colors.CYAN)
        PrintFramework.custom_print(f"Game price: {game_info["price"]}", Colors.WARNING, False)
        print(f" | Select Purchase game and then type: {gameId}, to buy {game_info["name"]}")

        buy_options.append(gameId)
    
    print("\n-----------------------\n")

    game_id = -1
    while not data_holder.games_data.get(game_id):
        MenuManager.option_menu([{"name": "Main Menu", "callable": main_menu}], "Purchase games")
        game_id = int(input("Type the game id to purchase it: "))

        if not data_holder.games_data.get(game_id):
            PrintFramework.custom_print(f"Invalid game id", Colors.WARNING)
    
    confirm = -1
    while confirm != 0 and confirm != 1:
        PrintFramework.custom_print("Type 1 to confirm purchase", Colors.GREEN)
        PrintFramework.custom_print("Type 0 to deny purchase\n", Colors.FAIL)
        confirm = int(input(""))
        if confirm != 0 and confirm != 1:
            PrintFramework.custom_print("Invalid option", Colors.WARNING)
    
    if not confirm:
        return
    
    # FIX ME
    GameInteractions.purchase_game(game_id, current_session.user_data, data_holder)


def show_catalog():
    # if session is online: 
    #   Show catalog menu option
    # else:
    #   Don't show catalog menu option
    return current_session.online


menus = [
    # Show menuIdx as menuIdx + 1
    {
        "name": "Login Menu",
        "callable": login_menu
    },
    {
        "name": "Sign in Menu",
        "callable": sign_in_menu
    },
    {
        "name": "Game catalog",
        "condition": show_catalog,
        "callable": game_catalog_menu
    }
]

while True:
    if main_menu() == -1:
        break
