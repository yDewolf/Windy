from framework.PrintFramework import custom_print
from framework.PrintFramework import Colors

def option_menu(options: list[dict], option_0: str="Quit"):
    print(f"Navigate by typing one of the options: ")
    possible_options = []

    for option in options:
        if option.get("condition"):
            if not option.get("condition")():
                continue
        
        possible_options.append(option)
    
    for menuIdx in range(len(possible_options)):
        print(f"{menuIdx + 1}-{possible_options[menuIdx]["name"]}")
    
    print(f"0-{option_0}\n")

    input_char = -1
    while input_char < 0 or input_char > len(possible_options):    
        input_char: int = int(input())

        if input_char < 0 or input_char > len(possible_options):
            custom_print(f"\nInvalid option index\n", Colors.WARNING)

    if input_char == 0:
        return -1

    possible_options[input_char - 1]["callable"]()