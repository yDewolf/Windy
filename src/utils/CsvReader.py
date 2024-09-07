import utils.FileUtils as FileUtils
#import FileUtils

default_backup_path: str = "data/backup/"

# Saves the currently loaded data, overwriting the previous file and creating a backup of the previous .csv
def overwrite_data(data: dict, data_path: str, backup: bool=True, backup_path: str=default_backup_path):
    if backup:
        FileUtils.backup_file(data_path, backup_path)

    csv_text = ""
    with open(data_path, "r") as file:
        header = file.readline().replace("\n", "").split(",")

        csv_text = dict_to_csv(data, header)

    with open(data_path, "w") as file:
        file.write(csv_text)

# Adds to the last line or to a new line (new_line) the values in a dictionary (data)
# Can backup or not the .csv file
def append_data(data: dict, data_path: str, new_line=True, backup: bool=True, backup_path: str=default_backup_path):
    with open(data_path, "a+") as file:
        if backup:
            FileUtils.backup_file(data_path, backup_path)
    
        csv_text = simple_dict_to_csv(data)
        if new_line:
            file.write("\n")
        
        file.write(csv_text)
        #file.close()


# Loads a .csv file
def load_csv(csv_path: str, columns: list[str]=[], use_main_key=False):
    file = open(csv_path, 'r')
    header = file.readline().replace("\n", "").split(",")


    target_columns = []
    for header_keyIdx in range(len(header)):
        if len(columns) > 0:
            if columns.__contains__(header[header_keyIdx]):
                target_columns.append(header_keyIdx)
        else:
            target_columns.append(header_keyIdx)


    values = {}
    main_keyIdx = 0
    if use_main_key:
        if len(target_columns) > 1 and len(columns) > 0:
            main_keyIdx = header.index(columns[0])
    
    else:
        values = []

    # Append line values to a dictionary using the header as keys
    for line in file:
        if line == "\n":
            continue
        
        line_dict = {}
        line_values = line.split(",")

        for valueIdx in target_columns:
            if use_main_key and valueIdx == main_keyIdx:
                continue
            
            value = FileUtils.parse_string(line_values[valueIdx].replace("\n", ""))

            line_dict[header[valueIdx]] = value
        
        if use_main_key:
            values[FileUtils.parse_string(line_values[target_columns[main_keyIdx]])] = line_dict
        else:
            values.append(line_dict)


    file.close()

    return values

def get_csv_columns(csv_path: str, columns: list[str]):
    file = open(csv_path, 'r')
    header = file.readline().replace("\n", "").split(",")

    target_columns = []
    for header_keyIdx in range(len(header)):
        if columns.__contains__(header[header_keyIdx]):
            target_columns.append(header_keyIdx)
    
    
    values = {}
    for key in columns:
        values[key] = {}
    
    for line in file:
        if line == "\n":
            continue
            
        line = line.replace("\n", "")
        line_values = line.split(",")
        for valueIdx in target_columns:
            value = FileUtils.parse_string(line_values[valueIdx])
            
            values[header[valueIdx]][value] = 1
    
    file.close()
    return values
    


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
        csv_line: str = FileUtils.convert_to_str(main_key)
        for key in dict:
            value_text = FileUtils.convert_to_str(dict[key])
            
            csv_line += "," + value_text
        
        lines.append(csv_line)
    
    for idx, line in enumerate(lines):
        csv_text += line
        if idx < len(lines) - 1:
            csv_text += "\n"
    
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
        value = FileUtils.convert_to_str(data_dict[key])

        csv_text += value
        if keyIdx < len(keys) - 1:
            csv_text += ","
        
    return csv_text


