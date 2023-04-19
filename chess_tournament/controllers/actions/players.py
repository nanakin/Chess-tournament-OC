"""Define players related Controller’s behaviours."""

from chess_tournament.models.model import AlreadyUsedID
from chess_tournament.views.requests import Request

from ..helpers import ConjugatedWord
from ..states import State
from .common import CommonController


class PlayersController(CommonController):
    """Players related Controller’s mixin class."""

    conjugated_player = ConjugatedWord(singular="player", plural="players")

    def show_manage_player_menu(self) -> None:
        """Show the main players menu and redirect the user’s request to the main state manager system."""
        request_to_status = {
            Request.MAIN_MENU: State.MAIN_MENU,
            Request.ADD_PLAYER: State.ADD_PLAYER_MENU,
            Request.EDIT_PLAYER: State.EDIT_PLAYER_MENU,
            Request.LIST_PLAYERS: State.LIST_PLAYERS_MENU}

        request, _ = self.view.show_manage_player_menu()
        if request in request_to_status:
            self.status = request_to_status[request]
        else:
            self.status = State.MAIN_MENU

    def show_edit_player_menu(self) -> None:
        """Show the player edition menu, modify the player, then back to the previous state."""
        players_id = self.model.get_players_id()
        request, request_data = self.view.show_player_selection(players_id)
        if request == Request.SELECTED_PLAYER:
            selected_id = request_data
            # maybe move message to the view
            message_to_confirm = f"You are about to edit:\n{self.model.get_player_str(selected_id)}\nDo you confirm?"
            request, request_data = self.view.show_confirmation(message_to_confirm)
            if request == Request.CONFIRM:
                confirm_status = request_data
                if confirm_status:
                    attributes_info = self.model.get_player_attributes(selected_id)
                    request, request_data = self.view.show_edit_player_menu(attributes_info)
                    if request == Request.REGISTER_PLAYER_DATA:
                        player_data = request_data
                        player_to_log = self.model.edit_player_attributes(player_data)
                        self.view.log(True, f"Player: {player_to_log} >>> edited")
                        self.status = State.MANAGE_PLAYER_MENU
                        return
        self.status = State.MANAGE_PLAYER_MENU

    def show_add_player_menu(self) -> None:
        """Show the player registration menu, register the player, then back to the previous state."""
        request, request_data = self.view.show_player_registration()
        if request == Request.REGISTER_PLAYER_DATA:
            try:
                player_to_log = self.model.add_players(request_data)
                self.view.log(True, f"Player: {player_to_log} >>> created")
            except AlreadyUsedID as err:
                self.view.log(False, f"A player with ID:{err.args[0]} already exists")
        self.status = State.MANAGE_PLAYER_MENU

    def show_list_players_menu(self) -> None:
        """Show the players report list."""
        self.report(
            total=self.model.get_total_players(),
            data_info=self.model.get_ordered_players_str(),
            conjugated_name=PlayersController.conjugated_player,
            back_state=State.MANAGE_PLAYER_MENU,
        )
