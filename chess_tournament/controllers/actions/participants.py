"""Define participants related Controller’s behaviours."""

from chess_tournament.views.requests import Request

from ..helpers import ConjugatedWord
from ..states import State
from .common import CommonController


class ParticipantsController(CommonController):
    """Participants related Controller’s mixin class."""

    conjugated_participant = ConjugatedWord(singular="participant", plural="participants")


    def show_manage_participants_menu(self):
        """Show the main participants menu and redirect the user’s request to the main state manager system."""
        total_participants = len(list(self.model.get_participants_id(self.context)))  # to-do : change method
        action = self.view.show_manage_participants_menu(total_participants)
        if action == Request.ADD_PARTICIPANT:
            self.status = State.ADD_PARTICIPANT_MENU
        elif action == Request.DELETE_PARTICIPANT:
            self.status = State.DELETE_PARTICIPANT_MENU
        elif action == Request.LIST_PARTICIPANTS:
            self.status = State.LIST_PARTICIPANTS_MENU
        else:
            self.status = State.MANAGE_TOURNAMENT_MENU

    def show_add_participant_menu(self):
        """Show the tournament participant registration menu, register the player, then back to the previous state."""
        selected_tournament = self.context
        players_id = [
            player_id
            for player_id in self.model.get_players_id()
            if player_id not in self.model.get_participants_id(selected_tournament)
        ]
        if not players_id:
            self.view.log(False, "No available players to add")
            self.status = State.MANAGE_PARTICIPANTS_MENU
            return
        action, action_data = self.view.show_player_selection(players_id)
        if action == Request.SELECTED_PLAYER:
            selected_id = action_data
            participant_to_log, tournament_to_log = self.model.add_participants_to_tournament(
                selected_tournament, selected_id
            )
            self.view.log(True, f"Participant: {participant_to_log} >>> added to {tournament_to_log}")
        self.status = State.MANAGE_PARTICIPANTS_MENU

    def show_delete_participant_menu(self):
        """Show the tournament participant deletion menu, delete the player, then back to the previous state."""
        selected_tournament = self.context
        participants_id = list(self.model.get_participants_id(selected_tournament))
        if not participants_id:
            self.view.log(False, "No participant to delete")
        else:
            action, action_data = self.view.show_player_selection(participants_id)
            if action == Request.SELECTED_PLAYER:
                selected_id = action_data
                participant_to_log, tournament_to_log = self.model.delete_participants_from_tournament(
                    selected_tournament, selected_id
                )
                self.view.log(True, f"Participant: {participant_to_log} >>> deleted from {tournament_to_log}")
        self.status = State.MANAGE_PARTICIPANTS_MENU

    def show_list_participants_menu(self):
        """Show the participants report list of the current tournament."""
        selected_tournament = self.context
        tournament_is_started = self.model.get_tournament_info(selected_tournament)["total_started_rounds"] > 0
        self.report(
            total=self.model.get_total_participants(selected_tournament),
            data_info=self.model.get_ordered_participants_str(selected_tournament),
            conjugated_name=self.conjugated_participant,
            back_state=State.MANAGE_TOURNAMENT_MENU if tournament_is_started else State.MANAGE_PARTICIPANTS_MENU,
        )
