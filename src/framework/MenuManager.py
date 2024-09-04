from framework.PrintFramework import custom_print
from framework.PrintFramework import Colors

console_size = 50

def option_menu(options: list[dict], option_0: str="Quit", title="", subtitle=""):
    menu_lines = []
    centered_lines = []
    
    if title == "":
        title = "Navigate by typing one of the options:"
    if subtitle == "":
        subtitle = "Select one the options below:"

    if title != " ":
        menu_lines.append(f"{title}")
        centered_lines.append(len(centered_lines))
    if subtitle != " ":
        menu_lines.append(f"{subtitle}")
        centered_lines.append(len(centered_lines))
    
    possible_options = []

    for option in options:
        if option.get("condition"):
            if not option.get("condition")():
                continue
        
        possible_options.append(option)
    
    for menuIdx in range(len(possible_options)):
        menu_lines.append(f"[{menuIdx + 1}]-{possible_options[menuIdx]["name"]}")
    
    menu_lines.append(f"[0]-{option_0}")

    generate_menu_ui(menu_lines, console_size, centered_lines)

    input_char = -1
    while input_char < 0 or input_char > len(possible_options):    
        input_char: int = int(input())

        if input_char < 0 or input_char > len(possible_options):
            custom_print(f"\nInvalid option index\n", Colors.WARNING)

    if input_char == 0:
        return input_char

    if possible_options[input_char - 1].get("callable"):
        possible_options[input_char - 1]["callable"]()
    
    return input_char


def generate_menu_ui(text_lines: list[str], width: int=console_size, centered_lines: list[int] = [], top: bool=False, bottom:bool=False):    
    if top:
        print(f"+{"-" * width}+")

    for idx, line in enumerate(text_lines):
        if centered_lines.__contains__(idx):
            print(f"|{line.center(width)}|")
        
        else:
            print(f"|{line.ljust(width)}|")
    
    if bottom:
        print(f"+{"-" * width}+")