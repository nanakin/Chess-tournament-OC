from chess_tournament.controllers.states import State
from chess_tournament.views.requests import Request


class MainMenuController:

    def show_main_menu(self):
        action = self.view.show_main_menu()
        if action == Request.EXIT_APP:
            self.status = State.QUIT
        elif action == Request.SAVE:
            pass
        elif action == Request.MANAGE_PLAYER:
            self.status = State.MANAGE_PLAYER_MENU
        elif action == Request.MANAGE_TOURNAMENT:
            self.status = State.MANAGE_TOURNAMENTS_MENU
        else:
            self.status = State.QUIT
