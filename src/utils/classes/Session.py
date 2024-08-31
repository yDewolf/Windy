from utils.Login import log_in
from utils.classes.DataHolder import DataHolder
from framework.PrintFramework import Colors
import framework.PrintFramework as PrintFramework

import utils.DataManager as DataManager

debug = False

class Session:
    session_id: int
    user_data: dict
    
    online: bool
    data_holder: DataHolder
    logged_accounts: dict

    def __init__(self, data_holder: DataHolder) -> None:
        self.session_id = -1
        self.user_data = {}
        self.data_holder = data_holder
        self.online = False

    def update_logged_accounts(self, accounts_path: str):
        self.logged_accounts = DataManager.load_csv_columns(accounts_path, ["username", "password"])

    def session_login(self, username: str, password: str):
        error = log_in(username, password, self.data_holder)
        if error != {} and error != -1:
            self.user_data = error
            self.online = True
            return True

        elif debug:
            PrintFramework.custom_print(f"ERROR: Failed to log in", Colors.WARNING)
        
        return False

    def session_signout(self):
        self.user_data = {}
        self.online = False


def start_session(data_holder) -> Session:
    return Session(data_holder)

