import os
import questionary as q

def clear_screen_and_show_log(function):
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def wrapper(self, *args, **kwargs):
        clear()
        self.show_log()
        return function(self, *args, **kwargs)
    return wrapper


def print_title(title):
    title = f" {title} "
    q.print(title.center(80, "="), style="bold")


def print_list_title(title):
    title = f" {title} "
    q.print(title.center(80, "+"), style="bold")

