from framework.PrintFramework import custom_print
from framework.PrintFramework import Colors

#from PrintFramework import custom_print
# from PrintFramework import Colors

console_size = 50
border = ""


# "Novo sistema de menus"
# Provavelmente ele seria muito melhor de organizar
# e muito falharia muito menos, porém, devido ao tempo
# e um pouco de preguiça de refazer todos os menus...
# Eu decidi não usar ele

# Forms:
# - Can have a title
# - Receives the input type (int, float, str)
# - Receives a range of possible options (list[str], list[int])
# - Receives a callable
# - Returns the inputted value to the callable

class Form:
    title: str
    options: list[str]
    form_callable: callable

    def __init__(self, title: str, options: list[str], form_callable) -> None:
        self.title = title
        self.options = options
        self.form_callable = form_callable
    
    def run(self):
        form_lines: list[str] = []
        centered_lines: list[int] = []
        if self.title != "":
            form_lines.append(self.title)
            centered_lines.append(len(centered_lines))

        for idx, option in enumerate(self.options):
            form_lines.append(f"[{idx}]-{option}")

        generate_menu_ui(form_lines, console_size, centered_lines)

        inputted = -1
        while inputted < 0 or inputted > len(self.options):
            inputted = int(input())
            if inputted < 0 or inputted > len(self.options):
                custom_print("Invalid option!", Colors.WARNING)

        self.form_callable(inputted)

# Class Menu:
# The menu class will be generated in this order:
# 1. Title
# 2. Subtitle
# 3. All text
# 4. All forms

class Menu:
    title: str
    subtitle: str
    text: list[str]
    forms: list

    def __init__(self, title: str, subtitle: str, text: list[str], forms: list[Form]) -> None:
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.forms = forms

    def create(self):
        menu_text: list[str] = []
        centered_lines = []
        if self.title != "":
            menu_text.append(self.title)
            centered_lines.append(len(centered_lines))
        if self.subtitle != "":
            menu_text.append(self.subtitle)
            centered_lines.append(len(centered_lines))
        
        generate_menu_ui(menu_text, console_size, centered_lines)

        for form in self.forms:
            form.run()



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


def generate_menu_ui(text_lines: list[str], width: int=console_size, centered_lines: list[int] = [], top: bool=False, bottom:bool=False, line_colors: list[Colors] = []):    
    if top:
        print(f"+{"-" * width}+")

    for idx, line in enumerate(text_lines):
        adjusted_line = line
        
        if centered_lines.__contains__(idx):
            adjusted_line = line.center(width)
        
        else:
            adjusted_line = line.ljust(width)
        
        if line_colors.__contains__(idx):
            custom_print(f"{border}{line_colors[idx].value}{adjusted_line}{border}", Colors.ENDC)
        else:
            print(f"{border}{adjusted_line}{border}")
    
    if bottom:
        print(f"+{"-" * width}+")

def generate_menu_w_param(lines: list[dict], width: int = console_size, top: bool = False, bottom: bool = False):
    if top:
        print(f"+{"-" * width}+")
    
    for idx, line_dict in enumerate(lines):
        adjusted_line = line_dict["text"]
        if line_dict.get("adjust") == "c":
            adjusted_line = adjusted_line.center(width)
        elif line_dict.get("adjust") == "r":
            adjusted_line = adjusted_line.rjust(width)
        
        print(border, end="")
        if line_dict.get("color"):
            custom_print(f"{adjusted_line}{border}", line_dict["color"], False)
            print()
        else:
            print(f"{adjusted_line}{border}")
    
    if bottom:
        print(f"+{"-" * width}+")