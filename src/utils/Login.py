import random
from utils.classes.DataHolder import DataHolder
import utils.DataManager as DataManager
import framework.PrintFramework as PrintFramework
from framework.PrintFramework import Colors

debug = True

# Really bad and unsafe login system
def log_in(username: str, password: str, data_holder: DataHolder) -> dict:
    # Check on database if username and password matches
    # User data collected from the database
    users = DataManager.load_csv_columns(data_holder.userdata_path, ["username", "password"])

    if users.get(username):
        if users[username]["password"] == password:
            PrintFramework.custom_print(f"Logged in succesfully as {username}", Colors.GREEN)
            return users[username]
        else:
            PrintFramework.custom_print(f"\nIncorrect Password", Colors.WARNING)
            return {}
    
    PrintFramework.custom_print(f"User not found in database", Colors.WARNING)

    if debug:
        PrintFramework.custom_print(f"^^^^^^^^^^^^^^^^^^^^^^^^^^\nIs this an Error?", Colors.WARNING)
        PrintFramework.custom_print(f"\nFailed to log in | Users in database: \n{users}", Colors.FAIL)
    
    return -1


def sign_in(username: str, email: str, password: str, data_holder: DataHolder):
    # Check if already has an user with the same username or email
    # Register user on database

    users = DataManager.load_csv_columns(data_holder.userdata_path, ["username"])
    if users.get(username):
        PrintFramework.custom_print("User already exists", Colors.WARNING)
        return
    
    emails = DataManager.load_csv_columns(data_holder.userdata_path, ["email"])
    if emails.get(email):
        PrintFramework.custom_print("Email is already in use", Colors.WARNING)
        return

    user_data = {
        "id": random.randrange(0, 65535),
        "username": username,
        "password": password,
        "email": email,
        "library": []
    }

    data_holder.users_data[user_data["id"]] = user_data
    DataManager.append_data(user_data, data_holder.userdata_path)