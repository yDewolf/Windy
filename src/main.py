import utils.AccountUtils as ApiLogin
import utils.CsvReader as CsvReader

import utils.classes.Session as Session
from utils.classes.DataHolder import DataHolder

import framework.MenuManager as MenuManager

import utils.GameInteractions as GameInteractions
import utils.AccountUtils as AccountUtils

import framework.PrintFramework as PrintFramework
from framework.PrintFramework import Colors

default_gamedata_path: str = "data/gamedata.csv"
default_userdata_path: str = "data/userdata.csv"
default_devdata_path: str = "data/developerdata.csv"

default_logged_accounts_path: str = "session_data/logged_accounts.csv"
default_session_cfg_path: str = "config/session_config.cfg"

data_holder: DataHolder = DataHolder(default_gamedata_path, default_userdata_path, default_devdata_path)

current_session = Session.start_session(data_holder, default_logged_accounts_path, default_session_cfg_path)

# Menu Callables

def main_menu():
    return MenuManager.option_menu(menus, "Quit", "Main Menu")


def login_menu():
    if MenuManager.option_menu([{"name": "Main Menu"}], "Continue", f"Login Menu"):
        return

    if len(current_session.logged_accounts) != 0:
        menu_lines = []

        menu_lines.append(f"You have logged accounts:")
        
        # If not selected Log in Previous Accounts
        if MenuManager.option_menu([{"name": "Log in another account", "callable": login_new_account}], "Log in previous accounts"):
            return
        
        menu_lines.append(" ")

        accounts = current_session.logged_accounts
        account_list = []
        for username in accounts:
            menu_lines.append(f"To log in as {username}, type {len(account_list)}")
            account_list.append(username)
        
        menu_lines.append(" ")
        menu_lines.append("Type the account number to log in")
        MenuManager.generate_menu_ui(menu_lines, MenuManager.console_size, [0, len(menu_lines) -1])
        menu_lines = []


        account_number = -1
        while account_number < 0 or account_number > len(account_list):
            account_number = int(input())
            if account_number < 0 or account_number > len(account_list):
                PrintFramework.custom_print("Invalid account number", Colors.WARNING)
        
        current_session.session_login(account_list[account_number], accounts[account_list[account_number]]["password"])
        current_session.update_last_logged(account_number)
        return

    login_new_account()

def login_new_account():
    username = input("Username: ")
    password = input("Password: ")
    
    # If logged in succesfully
    if current_session.session_login(username, password):
        remember_account(username, password)


def sign_in_menu():
    if MenuManager.option_menu([{"name": "Main Menu"}], "Continue", f"{Colors.HEADER.value}Sign in{Colors.ENDC.value}"):
        return

    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    ApiLogin.sign_in(username, email, password, data_holder)
    if current_session.session_login(username, password):
        remember_account(username, password)

def sign_out_menu():
    if MenuManager.option_menu([{"name": "Main Menu"}], "I'm sure I want to sign out", "Sign out Menu"):
        return

    current_session.session_signout()
    PrintFramework.custom_print("Signed out succesfully | You are now offline", Colors.GREEN)

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
        CsvReader.append_data({"username": username, "password": password}, default_logged_accounts_path)
        current_session.update_last_logged(-1)



def game_catalog_menu():
    print(f"{"-" * MenuManager.console_size}")
    PrintFramework.custom_print("Games in Catalog:", Colors.HEADER)

    buy_options: list[int] = []
    for gameId in data_holder.games_data:
        game_info = data_holder.games_data[gameId]
        game_status: bool = current_session.user_data["library"].count(gameId) > 0

        PrintFramework.custom_print(f"\n--- {game_info["name"]} --- Already Owned: {game_status}", Colors.HEADER)
        PrintFramework.custom_print(f"{game_info["description"]}", Colors.CYAN)
        PrintFramework.custom_print(f"Game price: {game_info["price"]}", Colors.WARNING)
        print(f"{Colors.CYAN.value}[{gameId}]{Colors.ENDC.value}-buy {Colors.HEADER.value}{game_info["name"]}{Colors.ENDC.value}")

        buy_options.append(gameId)
    
    print(f"\n{"-" * MenuManager.console_size}\n")

    game_id = -1
    while not data_holder.games_data.get(game_id) or GameInteractions.check_bought(game_id, current_session.user_data):
        if not MenuManager.option_menu([{"name": "Purchase Games"}], "Go back to Main Menu", " ", ""):
            return

        game_id = int(input("Type the game id to purchase it: "))

        if not data_holder.games_data.get(game_id):
            PrintFramework.custom_print(f"Invalid game id", Colors.WARNING)
    
        if GameInteractions.check_bought(game_id, current_session.user_data):
            PrintFramework.custom_print("You already have this game", Colors.WARNING)

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
    #print("-----------------------")
    PrintFramework.custom_print("Games in Library:", Colors.HEADER)

    for gameId in current_session.user_data["library"]:
        game_info = data_holder.games_data[gameId]
        PrintFramework.custom_print(f"\n--- {game_info["name"]} ---", Colors.HEADER)
        PrintFramework.custom_print(f"{game_info["description"]}", Colors.CYAN)
    
    #print("-----------------------")

    MenuManager.option_menu([{"name": "Main Menu"}], "Do nothing", "", " ")


def account_settings_menu():
    settings = [
        {
            "name": "Be a developer",
            "callable": be_a_developer_menu
        },
        {
            "name": "Delete my account",
            "callable": delete_account_menu
        }
    ]

    MenuManager.option_menu(settings, "Go back to Main Menu", "", " ")
    # match menu_idx:
    #     case 0:
    #         return
    #     case 1:
    #         be_a_developer_menu()

def delete_account_menu():
    PrintFramework.custom_print("Do you want to delete your account?", Colors.HEADER)
    PrintFramework.custom_print("This action can't be undone", Colors.WARNING)

    if not MenuManager.option_menu([{"name": "Go back to Main Menu"}], "Proceed to delete my account", "", " "):
        PrintFramework.custom_print(f"Type your username ({current_session.user_data["username"]}) to agree with the following statement", Colors.HEADER)
        PrintFramework.custom_print("I know that I'm deleting my account forever and this action cannot be undone:", Colors.WARNING)
        username = input()
        
        PrintFramework.custom_print("Type your password to confirm your action", Colors.HEADER)
        password = input()

        PrintFramework.custom_print("Are you sure you want to delete your account?", Colors.WARNING)

        if not MenuManager.option_menu([{"name": "I changed my mind"}], "I really want to delete my account", " ", " "):
            AccountUtils.delete_account(current_session.user_data["id"], username, password, data_holder)
            current_session.session_signout()


def be_a_developer_menu():
    PrintFramework.custom_print("Do you want to enter the Developers Project?", Colors.HEADER)
    PrintFramework.custom_print("What is the Developers Project?", Colors.WARNING)
    print("The Developers Project is a group of developers that develop for the Windy Platform")
    PrintFramework.custom_print("What can I do as a Developer?", Colors.WARNING)
    print("As a developer, you can publish your own games to our platform and earn money with its sells")
    PrintFramework.custom_print("What I need to be a Developer?", Colors.WARNING)
    print("To be a developer you only need to assign your account as a developer account, to do this you need to fulfill some personal info:")
    print("(CNPJ or CPF, First and Last name, Address)")

    sign_in_error = 0
    while not sign_in_error:
        PrintFramework.custom_print("\nDo you want to proceed to be a Developer?", Colors.WARNING)
        if MenuManager.option_menu([{"name": f"{Colors.FAIL.value}I don't want to be a Developer{Colors.ENDC.value}"}], f"{Colors.GREEN.value}I want to be a Developer{Colors.ENDC.value}", " ", " "):
            return

        print("Please fill the fields with your info")

        PrintFramework.custom_print(f"Fill this field with your first and last name: ", Colors.HEADER)
        name = input()

        PrintFramework.custom_print(f"Fill this field with your address", Colors.HEADER)
        address = input()

        cpf = 0
        cnpj = 0
        PrintFramework.custom_print(f"When filling the CNPJ and CPF USE ONLY NUMBERS", Colors.WARNING)
        while cnpj == 0 and cpf == 0:
            cpf = (input("If you don't want to register as a Physical Person, please let this field empty and fill the CNPJ: \nCPF: "))
            cnpj = (input("If you don't have a CNPJ, please let this field empty and fill the CPF: \nCNPJ: "))
            if cnpj == "":
                cnpj = 0
            if cpf == "":
                cpf = 0
            
            cpf = int(cpf)
            cnpj = int(cnpj)

            if cnpj == 0 and cpf == 0:
                PrintFramework.custom_print("You can't leave both CNPJ and CPF empty, you need to fill at least one of them", Colors.WARNING)

        PrintFramework.custom_print(f"\nNow you need to give your developer account a name", Colors.HEADER)
        dev_name = input()

        sign_in_error = AccountUtils.sign_as_dev(current_session.user_data["id"], dev_name, cpf, cnpj, name, address, data_holder)
    
    PrintFramework.custom_print("You are now registered as a Developer", Colors.GREEN)

def publish_game_menu():
    if MenuManager.option_menu([{"name": "Main Menu"}], "Continue", f"Publish Game Menu"):
        return

    #print("-----------")
    PrintFramework.custom_print("Publishing games: ", Colors.HEADER)
    print("To publish a game you need to fill these information about your game:")
    PrintFramework.custom_print("- Its name;\n- A description of it;\n- Its price", Colors.CYAN)
    PrintFramework.custom_print("\nDo you want to publish a game?", Colors.WARNING)
    if MenuManager.option_menu([{"name": f"{Colors.FAIL.value}No{Colors.ENDC.value}"}], f"{Colors.GREEN.value}Yes{Colors.ENDC.value}", ""):
        return
    
    PrintFramework.custom_print("What is the name of your game?", Colors.CYAN)
    game_name = input()

    PrintFramework.custom_print("Give your game a cool description", Colors.CYAN)
    game_description = input()

    PrintFramework.custom_print("How much your game will cost? (R$)", Colors.CYAN)
    price = float(input())

    GameInteractions.publish_game(game_name, game_description, price, current_session.user_data, data_holder)

    PrintFramework.custom_print("Your game was published successfully!", Colors.GREEN)

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

def is_developer():
    if is_online():
        return current_session.is_developer

    return False

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
    },
    {
        "name": "Publish Games",
        "condition": is_developer,
        "callable": publish_game_menu
    },
    {
        "name": "Account Settings",
        "condition": is_online,
        "callable": account_settings_menu
    }
]


print(f"+{"-" * MenuManager.console_size}+")

while True:
    if main_menu() == 0:
        current_session.save_cfg()
        break
