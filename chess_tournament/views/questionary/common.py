import os


def clear_screen_and_show_log(function):
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def wrapper(self, *args, **kwargs):
        clear()
        self.show_log()
        return function(self, *args, **kwargs)
    return wrapper
