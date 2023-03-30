from ..requests import Request, RequestAnswer
from ..interface import IView
from .players_menus import PlayerMenus
from .matches_menus import MatchesMenus
from .tournaments_menus import TournamentsMenus
from .participants_menus import ParticipantsMenus
from .common import clear_screen_and_show_log, print_title
import questionary as q
import os


class View(PlayerMenus, MatchesMenus, TournamentsMenus, ParticipantsMenus, IView):

    def __init__(self):
        self.logged = []
        q.print("------------------- Chess Tournament Manager ---------------------")

    def log(self, ok_status, to_print=None):
        self.logged.append((ok_status, to_print))

    def show_log(self):
        if self.logged:
            q.print("-- status " + "-" * 70)
        for log in self.logged:
            ok_status, to_print = log
            if ok_status:
                q.print(f"🟢 OK : {to_print}")
            else:
                q.print(f"🟥 FAIL {to_print}")
        self.logged = []

    def show_confirmation(self, to_confirm):
        return Request.CONFIRM, q.confirm(to_confirm).ask()

    def ask_saving_path(self):
        answer = q.path("Where do you want to save the list ?").ask()
        if not answer:
            return Request.EXIT_LOCAL_MENU
        return Request.SELECTED_PATH, answer

    @clear_screen_and_show_log
    def show_main_menu(self) -> RequestAnswer:
        print_title("Main menu")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Manage players", value=Request.MANAGE_PLAYER),
                q.Choice(title="Manage tournaments", value=Request.MANAGE_TOURNAMENT),
                q.Separator(),
                "Save",
                q.Choice(title="Exit", value=Request.EXIT_APP)])
        return question.ask()
