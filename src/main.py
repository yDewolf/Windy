import api.classes.fake_database as FakeDB
import api.Login as ApiLogin
import api.GameInteractions as ApiGameInteractions

using_database = FakeDB.FakeDatabase()

test_games = [
    {
        "name": "Muck",
        "description": "Muck is a cool game :) (pls buy)",
        "price": 5.0,
    },
    {
        "name": "Sekiro",
        "description": "I like sekiro, sekiro has cool mechanics, give it a try",
        "price": 100.0,
    }
]

for game_info in test_games:
    ApiGameInteractions.publish_game(game_info, using_database)

user_data = {}

while True:
    print(f"1-Login Menu\n2-Sign In Menu\n3-Look For Games\n0-Quit")
    input_char: int = int(input())

    match input_char:
        case 0:
            break
        case 1:
            username = input("Username: ")
            password = input("Password: ")
            user_data = ApiLogin.log_in(username, password, using_database)
        case 2:
            username = input("Username: ")
            password = input("Password: ")
            email = input("Email: ")
            ApiLogin.sign_in(username, email, password, using_database)
            user_data = ApiLogin.log_in(username, password, using_database)
        case 3:
            if len(user_data.keys()) == 0:
                print("You need to log in to see the games \n")
                continue
            
            
            game_ids = ApiGameInteractions.get_games(using_database)
            games_by_idx = []
            for game_id in game_ids:
                games_by_idx.append(game_id)
                game_info = ApiGameInteractions.get_game_info(game_id, using_database)
                print(f"\nGame name: {game_info["name"]}\nID: {game_info["id"]}\nPrice: {game_info["price"]}")
            
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