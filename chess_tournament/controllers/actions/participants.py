from chess_tournament.controllers.states import State
from chess_tournament.views.requests import Request
from ..helpers import ConjugatedWord

class ParticipantsController:

    conjugated_participant = ConjugatedWord(singular="participant", plural="participants")

    def show_manage_participants_menu(self):
        total_participants = len(list(self.model.get_participants_id(self.context)))  # to-do : change method
        action = self.view.show_manage_participants_menu(total_participants)
        if action == Request.ADD_PARTICIPANT:
            self.status = State.ADD_PARTICIPANT_MENU
        elif action == Request.DELETE_PARTICIPANT:
            self.status = State.DELETE_PARTICIPANT_MENU
        else:
            self.status = State.MANAGE_TOURNAMENT_MENU

    def show_add_participant_menu(self):
        selected_tournament = self.context
        players_id = [player_id for player_id in self.model.get_players_id()
                      if player_id not in self.model.get_participants_id(selected_tournament)]
        # to-do : verify if the list is empty
        if not players_id:
            self.view.log(False, "No available players to add")
            self.status = State.MANAGE_PARTICIPANTS_MENU
            return
        action, action_data = self.view.show_player_selection(players_id)
        if action == Request.SELECTED_PLAYER:
            selected_id = action_data
            # action, action_data = self.view.show_participant_registration(players)
            self.model.add_participants_to_tournament(selected_tournament, selected_id)
            self.view.log(True, f"participant added")
        self.status = State.MANAGE_PARTICIPANTS_MENU

    def show_delete_participant_menu(self):
        pass

    def show_list_participants_menu(self):
        selected_tournament = self.context
        self.report(total=self.model.get_total_participants(selected_tournament),
                    data_info=self.model.get_ordered_participants_str(selected_tournament),
                    conjugated_name=self.conjugated_participant, back_state=State.MANAGE_TOURNAMENT_MENU)
