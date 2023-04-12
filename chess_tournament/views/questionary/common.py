"""Define common functions used by the questionary menus classes."""
import os
import questionary as q

DEFAULT_COLUMNS = 80  # used as reference to center text on the terminal


def clear_screen_and_show_log(function):
    """Decorator that clear screen, display logs and then execute the given function."""

    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def wrapper(self, *args, **kwargs):
        clear()
        self.show_log()
        return function(self, *args, **kwargs)

    return wrapper


def print_title(title):
    """Print a centered title."""
    title = f" {title} "
    q.print(title.center(DEFAULT_COLUMNS, "="), style="bold")


def print_list_title(title):
    """Print a centered list title."""
    title = f" {title} "
    q.print(title.center(DEFAULT_COLUMNS, "+"), style="bold")


def print_important_info(info):
    """Print important information."""
    info = f">>> {info} <<<"
    q.print(info)
