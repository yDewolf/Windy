import utils.Login as ApiLogin
import utils.GameInteractions as ApiGameInteractions
import utils.DataManager as DataManager

import utils.classes.Session as Session
import utils.classes.DataHolder as DataHolder

default_gamedata_path: str = "data/gamedata.csv"
default_userdata_path: str = "data/userdata.csv"

data_holder: DataHolder = DataHolder()

data_holder.games_data = DataManager.load_gamedata(default_gamedata_path)
data_holder.users_data = DataManager.load_userdata(default_userdata_path)

current_session = Session.start_session()

while True:
    print(f"1-Login Menu\n2-Sign In Menu\n3-Look For Games\n0-Quit")
    input_char: int = int(input())

    match input_char:
        case 0:
            break
        case 1:
            username = input("Username: ")
            password = input("Password: ")
            current_session.session_login(username, password)
        case 2:
            username = input("Username: ")
            password = input("Password: ")
            email = input("Email: ")
            ApiLogin.sign_in(username, email, password, using_database)
            current_session.session_login(username, password)
        case 3:
            if not current_session.online:
                print("You need to log in to see the games \n")
                continue
            
            
            game_ids = ApiGameInteractions.get_games(using_database)
            games_by_idx = []
            for game_id in game_ids:
                games_by_idx.append(game_id)
                game_info = ApiGameInteractions.get_game_info(game_id, using_database)
                print(f"\nGame name: {game_info["name"]}\nID: {game_id}\nPrice: {game_info["price"]}")
            
            for i in range(len(games_by_idx)):
                game_info = ApiGameInteractions.get_game_info(games_by_idx[i], using_database)
                print(f"Type {i} to buy {game_info["name"]}\n")
            
            selected_game_idx = int(input())
            if selected_game_idx > 0 and selected_game_idx < len(games_by_idx):
                if input("Confirm purchase? Y/N").lower() == 'N':
                    continue
            
            ApiGameInteractions.purchase_game(games_by_idx[int(input())], user_data, using_database)


#while True:
#    error = main()
#    if error == -1:
#        break