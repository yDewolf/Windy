import utils.Login as ApiLogin

import utils.classes.Session as Session
from utils.classes.DataHolder import DataHolder

import framework.MenuManager as MenuManager

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


menus = [
    # Show menuIdx as menuIdx + 1
    {
        "name": "Login Menu",
        "callable": login_menu
    },
    {
        "name": "Sign in Menu",
        "callable": sign_in_menu
    }
]


while True:
    if main_menu() == -1:
        break
