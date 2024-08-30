import random
#from utils.classes.fake_database import FakeDatabase
from classes.DataHolder import DataHolder
import utils.DataManager as DataManager
#import api.classes.fake_database as FakeDB


def log_in(username: str, password: str, data_holder: DataHolder) -> dict:
    # Check on database if username and password matches
    # User data collected from the database

    for user_id in data_holder.users:
        user_data = data_holder.users[user_id]
        if user_data["username"] == username:
            if user_data["password"] == password:
                print(f"\nLogged in succesfully as {user_data["username"]}\n")
                print(user_data)
                return user_data
            else:
                print(f"\nIncorrect Password")
                return {}
                break

    print(f"\nFailed to log in | Users in database: \n{data_holder.users_data}\n")
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

    data_holder.users[user_data["id"]] = user_data
    DataManager.append_data(user_data, data_holder.userdata_path)