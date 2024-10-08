import os

os.system('')

class Colors:
    HEADER = "\033[95m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

def custom_print(text: str, color: Colors, new_line=True):
    if not new_line:
        print(f"{color}{text}{Colors.ENDC}", sep=" ", end="")
        return

    print(f"{color}{text}{Colors.ENDC}")