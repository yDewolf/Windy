from utils.Login import log_in

class Session:
    session_id: int
    user_data: dict
    online: bool
    
    def __init__(self) -> None:
        self.session_id = -1
        self.user_data = {}

    def session_login(self, username: str, password: str):
        error = log_in(username, password)
        if error != {} and error != -1:
            self.user_data = error
            self.online = True
        
        else:
            print(f"ERROR: Failed to log in")


def start_session() -> Session:
    return Session()

