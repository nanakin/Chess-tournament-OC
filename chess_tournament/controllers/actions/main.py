from chess_tournament.controllers.states import State
from chess_tournament.views.requests import Request
from ..helpers import ConjugatedWord, write_list_in_file


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

    def report(self, total, data_info, conjugated_name: ConjugatedWord, back_state):
        action = self.view.show_list_menu(total, conjugated_name.conjugated_with_number(total))
        if action not in (Request.PRINT, Request.EXPORT):
            self.status = back_state
            return
        if action == Request.PRINT:
            action = self.view.print_list(data_name=conjugated_name.plural, info_list=data_info)
        if action == Request.EXPORT:
            action, action_data = self.view.ask_saving_path()
            if action == Request.SELECTED_PATH:
                filename = action_data
                status_ok, absolute_path = write_list_in_file(data_info, filename, conjugated_name.plural)
                if status_ok:
                    self.view.log(True, f"List correctly saved in {absolute_path}.")
                else:
                    self.view.log(False, f"Cannot save data in {absolute_path}.")
        self.status = back_state
