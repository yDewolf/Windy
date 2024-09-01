import utils.FileUtils as FileUtils


# Probably a not good way to read .cfg files
def read_cfg_file(file_path: str) -> dict:
    cfg_dict: dict = {}
    file = open(file_path, "r")
    for line in file:
        if line.startswith("[") and line.endswith("]"):
            continue 
        
        values = line.split("=")
        if len(values) > 1:
            param = values[0]
            value = values[1].replace("\n", "")
            cfg_dict[param] = FileUtils.parse_string(value)

    return cfg_dict

def write_cfg_file(file_path: str, cfg_dict: dict):
    file = open(file_path, "w")

    text = ""
    for key in cfg_dict:
        value = cfg_dict[key]
        line = str(key) + "=" + FileUtils.convert_to_str(value)
        text += line + "\n"

    file.write(text)
    file.close()

#dictionary = read_cfg_file("config/session_config.cfg")
#write_cfg_file("config/session_config.cfg", dictionary)