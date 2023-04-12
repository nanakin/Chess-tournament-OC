from chess_tournament.controllers.states import State
from chess_tournament.views.requests import Request
from chess_tournament.models.model import AlreadyUsedID
from ..helpers import write_list_in_file, ConjugatedWord


class PlayerController:
    conjugated_player = ConjugatedWord(singular="player", plural="players")

    def show_manage_player_menu(self):
        action = self.view.show_manage_player_menu()
        if action == Request.MAIN_MENU:
            self.status = State.MAIN_MENU
        elif action == Request.ADD_PLAYER:
            self.status = State.ADD_PLAYER_MENU
        elif action == Request.EDIT_PLAYER:
            self.status = State.EDIT_PLAYER_MENU
        elif action == Request.LIST_PLAYERS:
            self.status = State.LIST_PLAYERS_MENU
        else:
            self.status = State.MAIN_MENU

    def show_edit_player_menu(self):
        players_id = self.model.get_players_id()
        action, action_data = self.view.show_player_selection(players_id)
        if action == Request.SELECTED_PLAYER:
            selected_id = action_data
            # maybe move message to the view
            message_to_confirm = f"You are about to edit:\n{self.model.get_player_str(selected_id)}\nDo you confirm?"
            action, action_data = self.view.show_confirmation(message_to_confirm)
            if action == Request.CONFIRM:
                confirm_status = action_data
                if confirm_status:
                    attributes_info = self.model.get_player_attributes(selected_id)
                    action, action_data = self.view.show_edit_player_menu(attributes_info)
                    if action == Request.REGISTER_PLAYER_DATA:
                        player_data = action_data
                        player_to_log = self.model.edit_player_attributes(player_data)
                        self.view.log(True, f"Player: {player_to_log} >>> edited")
                        self.status = State.MANAGE_PLAYER_MENU
                    else:
                        self.status = State.MANAGE_PLAYER_MENU
                else:
                    self.status = State.MANAGE_PLAYER_MENU
            else:
                self.status = State.MANAGE_PLAYER_MENU
        else:
            self.status = State.MANAGE_PLAYER_MENU

    def show_add_player_menu(self):
        action, action_data = self.view.show_player_registration()
        if action == Request.REGISTER_PLAYER_DATA:
            try:
                player_to_log = self.model.add_players(action_data)
                self.view.log(True, f"Player: {player_to_log} >>> created")
            except AlreadyUsedID as err:
                self.view.log(False)
        self.status = State.MANAGE_PLAYER_MENU

    def show_list_players_menu(self):
        self.report(
            total=self.model.get_total_players(),
            data_info=self.model.get_ordered_players_str(),
            conjugated_name=PlayerController.conjugated_player,
            back_state=State.MANAGE_PLAYER_MENU,
        )
