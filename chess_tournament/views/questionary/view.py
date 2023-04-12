"""Define the questionary main view class."""

from ..requests import Request, RequestAnswer
from ..interface import IView
from .players_menus import PlayerMenus
from .matches_menus import MatchesMenus
from .tournaments_menus import TournamentsMenus
from .participants_menus import ParticipantsMenus
from .common import clear_screen_and_show_log, print_title, print_list_title
import questionary as q


class View(PlayerMenus, MatchesMenus, TournamentsMenus, ParticipantsMenus, IView):
    """Main questionary view class (which inherits from specialized ones)."""

    def __init__(self):
        """Initialize the view."""
        self.logged = []
        q.print("------------------ ♔ Chess Tournament Manager ♔ --------------------")

    def log(self, ok_status, to_print=None):
        """Add a log to the log queue."""
        self.logged.append((ok_status, to_print))

    def show_log(self):
        """Display logs and purge the queue."""
        if self.logged:
            q.print("-- status " + "-" * 70)
        for log in self.logged:
            ok_status, to_print = log
            if ok_status:
                q.print(f"✅: {to_print}")
            else:
                q.print(f"❌: {to_print}")
        q.print("")
        self.logged = []

    def show_confirmation(self, to_confirm):
        """Display a yes/no question."""
        return Request.CONFIRM, q.confirm(to_confirm).ask()

    def ask_saving_path(self):
        """Display an autocomplete path question."""
        answer = q.path("Where do you want to save the list ?").ask()
        if not answer:
            return Request.EXIT_LOCAL_MENU
        return Request.SELECTED_PATH, answer

    @clear_screen_and_show_log
    def show_main_menu(self) -> RequestAnswer:
        """Display the main select menu."""
        print_title("Main menu")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Manage players", value=Request.MANAGE_PLAYER),
                q.Choice(title="Manage tournaments", value=Request.MANAGE_TOURNAMENT),
                q.Separator(),
                q.Choice(title="Exit", value=Request.EXIT_APP),
            ],
        )
        return question.ask()

    @clear_screen_and_show_log
    def show_list_menu(self, total, data_name):
        """Display a select menu : print or export."""
        print_title(f"{data_name.capitalize()} list menu")
        q.print(f">> Total {total} {data_name}")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Print list", value=Request.PRINT),
                q.Choice(title="Export list", value=Request.EXPORT),
                q.Separator(),
                q.Choice(title="Back", value=Request.EXIT_LOCAL_MENU),
            ],
        )
        return question.ask()

    @clear_screen_and_show_log
    def print_list(self, data_name, info_list):
        """Display the given list then suggest to export it."""
        print_list_title(f"{data_name.capitalize()} list")
        for info in info_list:
            q.print(info)
        back_choice = q.Choice(title="Back", value=Request.EXIT_LOCAL_MENU)
        question = q.select(
            "",
            choices=[
                back_choice,
                q.Choice(title="Export this list", value=Request.EXPORT),
            ],
            default=back_choice,
        )
        answer = question.ask()
        if not answer:
            return Request.EXIT_LOCAL_MENU
        return answer
