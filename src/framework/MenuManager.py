from framework.PrintFramework import custom_print
from framework.PrintFramework import Colors

def option_menu(options: list[dict], option_0: str="Quit"):
    print(f"Navigate by typing one of the options: ")

    for menuIdx in range(len(options)):
        if options[menuIdx].get("condition"):
            if not options[menuIdx].get("condition")():
                continue

        print(f"{menuIdx + 1}-{options[menuIdx]["name"]}")
    
    print(f"0-{option_0}\n")

    input_char = -1
    while input_char < 0 or input_char > len(options):    
        input_char: int = int(input())

        if input_char < 0 or input_char > len(options):
            custom_print(f"\nInvalid option index\n", Colors.WARNING)

    if input_char == 0:
        return -1

    options[input_char - 1]["callable"]()