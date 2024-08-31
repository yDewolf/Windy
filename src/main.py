import utils.Login as ApiLogin
import utils.DataManager as DataManager

import utils.classes.Session as Session
from utils.classes.DataHolder import DataHolder

import framework.MenuManager as MenuManager

import utils.GameInteractions as GameInteractions

import framework.PrintFramework as PrintFramework
from framework.PrintFramework import Colors

default_gamedata_path: str = "data/gamedata.csv"
default_userdata_path: str = "data/userdata.csv"

default_logged_accounts_path: str = "session_data/logged_accounts.csv"

data_holder: DataHolder = DataHolder(default_gamedata_path, default_userdata_path)

auto_login = True

current_session = Session.start_session(data_holder, default_logged_accounts_path, auto_login)


# Menu Callables

def main_menu():
    return MenuManager.option_menu(menus)


def login_menu():
    if not MenuManager.option_menu([{"name": "Main Menu", "callable": main_menu}], "Continue") == -1:
        return

    if len(current_session.logged_accounts) != 0:
        PrintFramework.custom_print(f"You have logged accounts: ", Colors.HEADER)

        accounts = current_session.logged_accounts
        account_list = []
        
        for username in accounts:
            PrintFramework.custom_print(f"To log in as {Colors.CYAN.value}{username}{Colors.ENDC.value}{Colors.HEADER.value}, type {len(account_list)}", Colors.HEADER)
            account_list.append(username)
        
        # If not selected Log in Previous Accounts
        if not MenuManager.option_menu([{"name": "Log in another account", "callable": login_new_account}], "Log in previous accounts") == -1:
            return
        
        PrintFramework.custom_print("Type the account number to log in", Colors.ENDC)
        account_number = -1
        while account_number < 0 or account_number > len(account_list):
            account_number = int(input())
            if account_number < 0 or account_number > len(account_list):
                PrintFramework.custom_print("Invalid account number", Colors.WARNING)
        
        current_session.session_login(account_list[account_number], accounts[account_list[account_number]]["password"])
        return

    login_new_account()

def login_new_account():
    username = input("Username: ")
    password = input("Password: ")
    
    # If logged in succesfully
    if current_session.session_login(username, password):
        remember_account(username, password)


def sign_in_menu():
    MenuManager.option_menu([{"name": "Main Menu", "callable": main_menu}], "Continue")

    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    ApiLogin.sign_in(username, email, password, data_holder)
    if current_session.session_login(username, password):
        remember_account(username, password)


def remember_account(username, password):
    remember = -1
    PrintFramework.custom_print("Remember account?\n", Colors.ENDC)
    PrintFramework.custom_print("1-Yes", Colors.GREEN)
    PrintFramework.custom_print("0-No", Colors.FAIL)
    while remember != 1 and remember != 0:
        remember = int(input())
        if remember != 1 and remember != 0:
            PrintFramework.custom_print("Invalid option", Colors.WARNING)
    
    if remember:
        DataManager.append_data({"username": username, "password": password}, default_logged_accounts_path)


def sign_out_menu():
    MenuManager.option_menu([{"name": "Main Menu", "callable": main_menu}], "I'm sure I want to sign out")
    current_session.session_signout()
    PrintFramework.custom_print("Signed out succesfully | You are now offline", Colors.GREEN)


def game_catalog_menu():
    print("-----------------------")
    print("Games in Catalog:")

    buy_options: list[int] = []
    for gameId in data_holder.games_data:
        game_info = data_holder.games_data[gameId]
        game_status: bool = current_session.user_data["library"].count(gameId) > 0

        PrintFramework.custom_print(f"\n--- {game_info["name"]} --- Already Owned: {game_status}", Colors.HEADER)
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

def library_menu():
    print("-----------------------")
    print("Games in Library:")

    for gameId in current_session.user_data["library"]:
        game_info = data_holder.games_data[gameId]
        PrintFramework.custom_print(f"\n--- {game_info["name"]} ---", Colors.HEADER)
        PrintFramework.custom_print(f"{game_info["description"]}", Colors.CYAN)
    
    print("-----------------------")

    MenuManager.option_menu([{"name": "Main Menu", "callable": main_menu}], "Do nothing")

# Menu Conditions

def is_online():
    # if session is online: 
    #   Show catalog menu option
    # else:
    #   Don't show catalog menu option
    return current_session.online

# Dumb way of solving the "not is_online" not working on menu["condition"]()
def is_offline():
    return not is_online()


# Menu Indexing
menus = [
    # Show menuIdx as menuIdx + 1
    {
        "name": "Login Menu",
        "condition": is_offline,
        "callable": login_menu
    },
    {
        "name": "Sign in Menu",
        "condition": is_offline,
        "callable": sign_in_menu
    },
    {
        "name": "Sign out",
        "condition": is_online,
        "callable": sign_out_menu,
    },
    {
        "name": "My Library",
        "condition": is_online,
        "callable": library_menu
    },
    {
        "name": "Game catalog",
        "condition": is_online,
        "callable": game_catalog_menu
    }
]


while True:
    if main_menu() == -1:
        break
