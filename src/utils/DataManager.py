import datetime
default_backup_path: str = "data/backup/"

# Saves the currently loaded data, overwriting the previous file and creating a backup of the previous .csv
def overwrite_data(data: dict, data_path: str, backup: bool=True, backup_path: str=default_backup_path):
    if backup:
        backup_data(data_path, backup_path)

    file = open(data_path, "r")
    header = file.readline().replace("\n", "").split(",")

    csv_text = dict_to_csv(data, header)

    file.close()
    file = open(data_path, "w")

    file.write(csv_text)
    file.close()

# Adds to the last line or to a new line (new_line) the values in a dictionary (data)
# Can backup or not the .csv file
def append_data(data: dict, data_path: str, new_line=True, backup: bool=True, backup_path: str=default_backup_path):
    file = open(data_path, "a")
    if backup:
        backup_data(data_path, backup_path)
    
    csv_text = simple_dict_to_csv(data)
    if new_line:
        file.write("\n")
    
    file.write(csv_text)
    file.close()

# Duplicates the selected file to a new path
# Adds to the file name the date and time that the file was created
def backup_data(file_path: str, backup_path: str):
    file_name = file_path.split("/")[-1] # Get file name from the file path

    # Add file format + create a new file
    backup_file = open(backup_path + file_name.split(".")[0] + "_" + (datetime.datetime.now()).strftime("%d%m%Y_%H-%M-%S") + "." + file_name.split(".")[-1], "w")
    
    # Duplicate file content to the new file
    file = open(file_path, "r")
    file_text = file.read()
    backup_file.write(file_text)
    backup_file.close()

# Loads a .csv file
def load_csv(data_path: str) -> list[dict]:
    file = open(data_path, 'r')
    header = file.readline().replace("\n", "").split(",")

    values = []

    # Append line values to a dictionary using the header as keys
    for line in file:
        line_dict = {}
        line_values = line.split(",")

        for valueIdx in range(len(line_values)):
            value = str_convert(line_values[valueIdx].replace("\n", ""))
            line_dict[header[valueIdx]] = value
        
        values.append(line_dict)
    
    file.close()

    return values

def load_csv_columns(csv_path: str, columns: list[str], use_main_key=True):
    file = open(csv_path, 'r')
    header = file.readline().replace("\n", "").split(",")

    target_columns = []
    for header_keyIdx in range(len(header)):
        if columns.__contains__(header[header_keyIdx]):
            target_columns.append(header_keyIdx)

    main_keyIdx = header.index(columns[0])    

    values = []
    if use_main_key:
        values = {}

    # Append line values to a dictionary using the header as keys
    for line in file:
        line_dict = {}
        line_values = line.split(",")

        for valueIdx in target_columns:
            if use_main_key and valueIdx == main_keyIdx:
                continue
            
            value = str_convert(line_values[valueIdx].replace("\n", ""))

            line_dict[header[valueIdx]] = value
        
        if use_main_key:
            values[str_convert(line_values[target_columns[main_keyIdx]])] = line_dict
        else:
            values.append(line_dict)


    file.close()

    return values


def str_convert(value: str):
    if value.startswith("[") and value.endswith("]"):
        value_list = list(value.replace(";", ",").replace("]", "").replace("[", ""))
        converted = []
        for val in value_list:
            converted.append(str_convert(val))

        return converted
    
    elif value.startswith("'") and value.endswith("'"):
        return str(value.replace("'", ""))

    # Value is a valid number
    elif value.count(".") != 0: #int(value) != 0 or value == "0":
        return float(value)

    return int(value)
    
def convert_to_str(value):
    if type(value) == str:
        return "'" + value + "'"

    elif type(value) == list:
        return str(value).replace(",", ";")

    return str(value)

# Reads a dictionary and returns a csv text
# This function is mainly used on dicts that has dicts inside of it. Ex:
# data_dict = {
#   1: {
#       "some_key": "some_value"
#   }
# }
# The keys on data_dict are the main keys
# The keys on the data_dict[main_key] are other keys
# The main key will always the first key on the csv line
def dict_to_csv(data_dict: dict, header: list[str]=[]) -> str:
    lines = []
    csv_text = ""
    # Append header to the csv text
    if len(header) != 0:
        for keyIdx in range(len(header)):
            csv_text += header[keyIdx]
            if keyIdx < len(header) - 1:
                csv_text += ","
        
        csv_text += "\n"

    for main_key in data_dict:
        dict = data_dict[main_key]
        csv_line: str = convert_to_str(main_key)
        for key in dict:
            value_text = convert_to_str(dict[key])
            
            csv_line += "," + value_text
        
        lines.append(csv_line)
    
    for line in lines:
        csv_text += line + "\n"
    
    return csv_text


# Reads a dictionary and returns a csv line
# This function is used when you are reading only one dict. A dict that doesn't have main keys. Ex:
# data_dict = {
#   "key": value
#}
def simple_dict_to_csv(data_dict: dict) -> str:
    csv_text = ""
    keys = []
    for key in data_dict:
        keys.append(key)


    for keyIdx in range(len(keys)):
        key = keys[keyIdx]
        value = convert_to_str(data_dict[key])

        csv_text += value
        if keyIdx < len(keys) - 1:
            csv_text += ","
        
    return csv_text
