import datetime
default_backup_path: str = "data/backup/"

def save_data(data_path: str, data: dict, backup: bool=True, backup_path: str=default_backup_path):
    file = open(data_path, "r")
    if backup:
        file_name = data_path.split("/")[-1]
        backup = open(backup_path + file_name.split(".")[0] + "_" + (datetime.datetime.now()).strftime("%d%m%Y_%H-%M-%S") + "." + file_name.split(".")[-1], "w")
        backup.write(file.read())
    
    header = file.readline().replace("\n", "").split(",")
    csv_text = dict_to_csv(data, header)
    file.write(csv_text)



def load_data(data_path: str):
    file = open(data_path, 'r')
    header = file.readline().replace("\n", "").split(",")

    values = []

    for line in file:
        line_dict = {}
        line_values = line.split(",")

        for valueIdx in range(len(line_values)):
            line_dict[header[valueIdx]] = line_values[valueIdx].replace("\n", "")
        values.append(line_dict)
        #values.append(line.split(","))
    
    return values



def load_userdata(data_path: str) -> dict:
    users_data = load_data(data_path)
    userdata = {}


    for data in users_data:
        print(data)
        userdata[int(data["id"])] = {
            "username": data["username"],
            "password": data["password"],
            "email": data["email"],
            "library": data["library"]
        }

    return userdata

def load_gamedata(data_path: str, debug=True) -> dict:
    games_data = load_data(data_path)
    gamedata = {}

    for data in games_data:
        if debug:
            print(f"Parsing data: {data}\nCurrent gamedata: {gamedata}")

        gamedata[int(data["id"])] = {
            "name": data["name"],
            "description": data["description"],
            "price": data["price"]
        }
    
    return gamedata


def dict_to_csv(data_dict: dict, header: list[str]) -> str:
    lines = []
    csv_text = ""
    for keyIdx in range(len(header)):
        csv_text += header[keyIdx]
        if keyIdx < len(header) - 1:
            csv_text += ","
    
    csv_text += "\n"

    for main_key in data_dict:
        dict = data_dict[main_key]
        csv_line: str = str(main_key)
        for key in dict:
            csv_line += "," + str(dict[key])
        
        lines.append(csv_line)
    
    for line in lines:
        csv_text += line + "\n"
    
    return csv_text


#data = load_gamedata("data\gamedata.csv", False)
#print(dict_to_csv(data, ["id", "name", "description", "price"]))
