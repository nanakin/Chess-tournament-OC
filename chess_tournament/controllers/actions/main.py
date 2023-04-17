"""Define not chess specialized Controller’s behaviours."""

from ..states import State
from chess_tournament.views.requests import Request
from .common import CommonController


class MainMenuController(CommonController):
    """Not specialized Controller’s mixin class."""

    def show_main_menu(self):
        """Show the main menu and redirect the user’s request to the main state manager system."""
        request_to_status = {
            Request.MANAGE_PLAYER: State.MANAGE_PLAYER_MENU,
            Request.MANAGE_TOURNAMENT: State.MANAGE_TOURNAMENTS_MENU}

        request = self.view.show_main_menu()

        if request in request_to_status:
            self.status = request_to_status[request]
        else:
            self.status = State.QUIT

