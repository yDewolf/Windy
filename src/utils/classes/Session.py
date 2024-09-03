from utils.AccountUtils import log_in
from utils.classes.DataHolder import DataHolder
from framework.PrintFramework import Colors
import framework.PrintFramework as PrintFramework

import utils.DataManager as DataManager
import utils.ConfigReader as CfgReader

debug = False

class Session:
    session_id: int
    user_data: dict
    
    online: bool
    is_developer: bool

    data_holder: DataHolder
    logged_accounts: dict

    cfg_path: str
    config: dict

    def __init__(self, data_holder: DataHolder, accounts_path: str="", cfg_path: str="") -> None:
        self.data_holder = data_holder

        self.cfg_path = cfg_path
        self.config = CfgReader.read_cfg_file(cfg_path)

        if self.config["auto_login"]:
            self.update_logged_accounts(accounts_path)

            accounts = self.logged_accounts
            if len(self.logged_accounts) == 0:
                self.session_login("", "")
                return

            username = list(enumerate(accounts))[self.config["last_logged_account"]][1]
            self.session_login(username, accounts[username]["password"])
            return

        if accounts_path != "":
            self.update_logged_accounts(accounts_path)

        self.session_id = -1
        self.user_data = {}
        self.online = False

    def update_logged_accounts(self, accounts_path: str):
        self.logged_accounts = DataManager.load_csv(accounts_path, ["username", "password"], True)

    def update_last_logged(self, last_idx: int):
        self.config["last_logged_account"] = last_idx
        CfgReader.write_cfg_file(self.cfg_path, self.config)


    def session_login(self, username: str, password: str):
        error = log_in(username, password, self.data_holder)
        if error != {} and error != -1:
            self.user_data = error
            self.online = True

            developers = DataManager.load_csv(self.data_holder.devdata_path, ["id", "dev_name"], True)
            self.is_developer = False
            if developers.get(self.user_data["id"]):
                self.is_developer = True
        
            if self.is_developer:
                PrintFramework.custom_print("Logged as a developer", Colors.GREEN)
            
            return True

        else:
            
            
            if debug:
                PrintFramework.custom_print(f"ERROR: Failed to log in", Colors.WARNING)
        
        self.online = False
        return False

    def session_signout(self):
        self.logged_accounts.pop(self.user_data["username"])
        DataManager.overwrite_data(self.logged_accounts, self.config["accounts_path"])

        self.user_data = {}
        self.online = False
        self.config["auto_login"] = False

    def save_cfg(self):
        PrintFramework.custom_print("Saving session config", Colors.CYAN)
        CfgReader.write_cfg_file(self.cfg_path, self.config)


def start_session(data_holder, accounts_path: str="", cfg_path: str="") -> Session:
    return Session(data_holder, accounts_path, cfg_path)

