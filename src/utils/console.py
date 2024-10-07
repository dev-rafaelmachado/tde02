import os

CLEAR_COMMAND = "cls" if os.name == "nt" else "clear"


def clear_screen():
    """Limpa o console."""
    os.system(CLEAR_COMMAND)
