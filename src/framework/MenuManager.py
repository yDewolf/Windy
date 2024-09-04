from framework.PrintFramework import custom_print
from framework.PrintFramework import Colors

console_size = 50

def option_menu(options: list[dict], option_0: str="Quit", title="", subtitle=""):
    if title == "":
        title = "Navigate by typing one of the options:"
    if subtitle == "":
        subtitle = "Select one the options below:"
    
    if title != " ":
        print(f"\n {title.center(console_size, " ")} ")
    if subtitle != " ":
        print(f" {subtitle.center(console_size, " ")} ")
    
    possible_options = []

    for option in options:
        if option.get("condition"):
            if not option.get("condition")():
                continue
        
        possible_options.append(option)
    
    for menuIdx in range(len(possible_options)):
        print(f"[{menuIdx + 1}]-{possible_options[menuIdx]["name"]}")
    
    print(f"[0]-{option_0}")

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
