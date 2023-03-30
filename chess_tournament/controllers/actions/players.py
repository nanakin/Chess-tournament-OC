from chess_tournament.controllers.states import State
from chess_tournament.views.requests import Request
from chess_tournament.models.model import AlreadyUsedID


class PlayerController:

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
                        self.model.edit_player_attributes(player_data)
                        self.view.log(True, self.model.get_player_str(player_data["identifier"]))
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
                self.model.add_players(action_data)
                self.view.log(True, self.model.get_player_str(action_data["identifier"]))
            except AlreadyUsedID as err:
                self.view.log(False)
        self.status = State.MANAGE_PLAYER_MENU

    def show_list_players_menu(self):
        total_players = self.model.get_total_players()
        action = self.view.show_list_players_menu(total_players)
        if action not in (Request.PRINT_PLAYERS, Request.EXPORT_PLAYERS):
            self.status = State.MANAGE_PLAYER
            return
        players_info = self.model.get_ordered_players_str()
        if action == Request.PRINT_PLAYERS:
            self.view.print_players(players_info)
        else:
            pass  # to-do
        self.status = State.MANAGE_PLAYER_MENU
