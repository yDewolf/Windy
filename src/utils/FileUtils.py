import datetime

def parse_string(value: str):
    if value.startswith("[") and value.endswith("]"):
        value_list = (value.replace("]", "").replace("[", "")).split(";")
        converted = []
        if value_list != ['']:
            for val in value_list:
                converted.append(parse_string(val))

        return converted
    
    elif value.startswith("'") and value.endswith("'"):
        return str(value.replace("'", ""))

    # Value is a valid number
    elif value.count(".") != 0:
        return float(value)

    elif str(value).lower() == "false":
        return False
    elif str(value).lower() == "true":
        return True

    return int(value)
    
def convert_to_str(value):
    if type(value) == str:
        return "'" + value + "'"

    elif type(value) == list:
        return str(value).replace(",", ";")

    return str(value)

# Duplicates the selected file to a new path
# Adds to the file name the date and time that the file was created
def backup_file(file_path: str, backup_path: str):
    file_name = file_path.split("/")[-1] # Get file name from the file path

    # Add file format + create a new file
    backup_file = open(backup_path + file_name.split(".")[0] + "_" + (datetime.datetime.now()).strftime("%d%m%Y_%H-%M-%S") + "." + file_name.split(".")[-1], "w")
    
    # Duplicate file content to the new file
    file = open(file_path, "r")
    file_text = file.read()
    backup_file.write(file_text)
    backup_file.close()