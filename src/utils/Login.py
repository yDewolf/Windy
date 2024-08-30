import random
from utils.classes.DataHolder import DataHolder
import utils.DataManager as DataManager


def log_in(username: str, password: str, data_holder: DataHolder) -> dict:
    # Check on database if username and password matches
    # User data collected from the database
    users = DataManager.load_csv_columns(data_holder.userdata_path, ["username", "password"])

    if users.get(username):
        if users[username]["password"] == password:
            print(f"\033[92m\nLogged in succesfully as {username}\n\033[0m")
            return users[username]
        else:
            print(f"\033[93m\nIncorrect Password\033[0m")
            return {}
    else:
        print("\033[91mERROR: User doesn't exist\033[0m")
    #for user_id in data_holder.users_data:
    #    user_data = data_holder.users_data[user_id]
    #    if user_data["username"] == username:
    #        if user_data["password"] == password:
    #            print(f"'\033[92m'\nLogged in succesfully as {user_data["username"]}\n'\033[0m'")
    #            print(user_data)
    #            return user_data
    #        else:
    #            print(f"'\033[92m'\nIncorrect Password'\033[0m'")
    #            return {}
    #            break

    print(f"\033[91m\nFailed to log in | Users in database: \n{users}\n\033[0m")
    return -1


def sign_in(username: str, email: str, password: str, data_holder: DataHolder):
    # Check if already has an user with the same username or email
    # Register user on database

    user_data = {
        "id": random.randrange(0, 65535),
        "username": username,
        "password": password,
        "email": email,
        "library": []
    }

    data_holder.users_data[user_data["id"]] = user_data
    DataManager.append_data(user_data, data_holder.userdata_path)