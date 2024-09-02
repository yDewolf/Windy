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
    users = DataManager.load_csv(data_holder.userdata_path, ["username", "password", "id", "library"], True)

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
    users_data = DataManager.get_csv_columns(data_holder.userdata_path, ["username", "email"])
    if users_data["username"].get(username):
        PrintFramework.custom_print("User already exists", Colors.WARNING)
        return

    if users_data["email"].get(email):
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


def sign_as_dev(user_id: int,  dev_name: str, cpf: int, cnpj: int, name: str, address: str, data_holder: DataHolder):
    developers = DataManager.load_csv(data_holder.devdata_path, ["id", "dev_name", "cpf", "cnpj"], True)

    if cpf == 0 and cnpj == 0:
        PrintFramework.custom_print("You can't leave CNPJ and CPF in blank, assign at least one of them", Colors.WARNING)
        return

    developers_data = DataManager.get_csv_columns(data_holder.devdata_path, ["id", "dev_name", "cpf", "cnpj"])

    # Testing for duplicated info
    if developers_data["id"].get(user_id):
        PrintFramework.custom_print("You are already registered as a developer", Colors.WARNING)
        return
    elif developers_data["cpf"].get(cpf) and cpf != 0:
        PrintFramework.custom_print("This CPF is already registered as a developer", Colors.WARNING)
        PrintFramework.custom_print("If you are the owner of this CPF and didn't register it, please look for a police department to report it")
        return
    elif developers_data["cnpj"].get(cnpj) and cnpj != 0:
        PrintFramework.custom_print("This CNPJ is already registered", Colors.WARNING)
        PrintFramework.custom_print("If you are the owner of this CNPJ and didn't register it, please look for a police department to report it")
        return
    elif developers_data["dev_name"].get(dev_name):
        PrintFramework.custom_print("This developer name is already in use, try another", Colors.WARNING)
        return
    
    dev_data = {
        "id": user_id,
        "dev_name": dev_name,
        "cpf": cpf,
        "cnpj": cnpj,
        "name": name,
        "address": address,
        "published_games": []
    }

    DataManager.append_data(dev_data, data_holder.devdata_path)
    return True
