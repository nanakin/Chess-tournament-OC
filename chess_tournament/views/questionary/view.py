from ..requests import Request, RequestAnswer
from ..interface import IView
from ..validators import *
from .players_menus import PlayerMenus
from .matches_menus import MatchesMenus
from .tournaments_menus import TournamentsMenus
from .participants_menus import ParticipantsMenus
import questionary as q
import os


class View(PlayerMenus, MatchesMenus, TournamentsMenus, ParticipantsMenus, IView):

    def __init__(self):
        q.print("------------------- Chess Tournament Manager ---------------------")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_confirmation(self, to_confirm):
        return Request.CONFIRM, q.confirm(to_confirm).ask()

    def show_status(self, ok_status, to_print=""):
        if ok_status:
            q.print(f"🟢 OK : {to_print}")
        else:
            q.print(f"🟥 FAIL {to_print}")

    def show_main_menu(self) -> RequestAnswer:
        q.print("==== Main Menu ===")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Manage players", value=Request.MANAGE_PLAYER),
                q.Choice(title="Manage tournaments", value=Request.MANAGE_TOURNAMENT),
                q.Separator(),
                "Save",
                q.Choice(title="Exit", value=Request.EXIT_APP)])
        return question.ask()
