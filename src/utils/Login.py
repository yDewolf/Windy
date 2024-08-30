import random
from utils.classes.fake_database import FakeDatabase
#import api.classes.fake_database as FakeDB


def log_in(username: str, password: str, fake_database: FakeDatabase) -> dict:
    # Check on database if username and password matches
    # User data collected from the database

    for user_id in fake_database.users:
        user_data = fake_database.users[user_id]
        if user_data["username"] == username and user_data["password"] == password:
            print(f"\nLogged in succesfully as {user_data["username"]}\n")
            print(user_data)
            return user_data
    
    print(f"\nFailed to log in | Users in database: {fake_database.users}\n")
    return -1
    

    #user_data = {
    #    "username": username,
    #    "id:": -1,
    #    "library": []
    #}

def sign_in(username: str, email: str, password: str, fake_database: FakeDatabase):
    # Check if already has an user with the same username or email
    # Register user on database

    user_data = {
        "username": username,
        "id": random.randrange(0, 65535),
        "password": password,
        "email": email,
        "library": []
    }

    fake_database.users[user_data["id"]] = user_data