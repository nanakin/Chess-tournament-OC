"""Define tournaments related Controller’s behaviours."""

from chess_tournament.controllers.states import State
from chess_tournament.views.requests import Request
from ..helpers import ConjugatedWord
from chess_tournament.controllers.actions.common import CommonController


class TournamentsController(CommonController):
    """Tournaments related Controller’s mixin class."""

    conjugated_tournament = ConjugatedWord(singular="tournament", plural="tournaments")

    def show_manage_tournaments_menu(self):
        """Show the main tournaments menu and redirect the user’s request to the main state manager system."""
        action = self.view.show_manage_tournaments_menu()
        if action == Request.ADD_TOURNAMENT:
            self.status = State.ADD_TOURNAMENT_MENU
        elif action == Request.EDIT_TOURNAMENT:
            if self.context is not None:
                selected_tournament = self.context
                tournament_info = self.model.get_tournament_info(selected_tournament)["str"]
                action = self.view.keep_or_change_tournament(tournament_info)
                if action == Request.KEEP_SELECTED_TOURNAMENT:
                    self.status = State.MANAGE_TOURNAMENT_MENU
                elif action == Request.CHANGE_SELECTED_TOURNAMENT:
                    self.context = None
                    self.status = State.SELECT_TOURNAMENT_MENU
            else:
                self.status = State.SELECT_TOURNAMENT_MENU
        elif action == Request.LIST_TOURNAMENTS:
            self.status = State.LIST_TOURNAMENTS_MENU
        else:
            self.status = State.MAIN_MENU

    def show_tournament_registration(self):
        """Show the tournament registration menu, register the tournament, then back to the previous state."""
        action, action_data = self.view.show_tournament_registration()
        if action == Request.REGISTER_TOURNAMENT_DATA:
            tournament_data = action_data
            tournament_to_log = self.model.add_tournaments(tournament_data)
            self.view.log(True, f"Tournament: {tournament_to_log} >>> created")
        self.status = State.MANAGE_TOURNAMENTS_MENU

    def show_select_tournament_menu(self):
        """Show methods to choose, then list tournament to select from, register selection in the context."""
        # improvement : use round info to know if a tournament really ended
        statistics = self.model.get_tournaments_states_statistics()
        action = self.view.how_to_choose_tournament(statistics)
        if action in (
            Request.FIND_TOURNAMENT_BY_NAME,
            Request.FIND_TOURNAMENT_BY_LIST_ONGOING,
            Request.FIND_TOURNAMENT_BY_LIST_FUTURE,
            Request.FIND_TOURNAMENT_BY_LIST_PAST,
            Request.FIND_TOURNAMENT_BY_LIST_ALL,
        ):
            if action == Request.FIND_TOURNAMENT_BY_NAME:
                tournaments_info = self.model.get_tournaments_str()
                action, action_data = self.view.choose_tournament_by_name(tournaments_info)
            else:
                if action == Request.FIND_TOURNAMENT_BY_LIST_ONGOING:
                    tournaments_info = self.model.get_tournaments_str("ongoing")
                elif action == Request.FIND_TOURNAMENT_BY_LIST_FUTURE:
                    tournaments_info = self.model.get_tournaments_str("future")
                elif action == Request.FIND_TOURNAMENT_BY_LIST_PAST:
                    tournaments_info = self.model.get_tournaments_str("past")
                elif action == Request.FIND_TOURNAMENT_BY_LIST_ALL:
                    tournaments_info = self.model.get_tournaments_str("all")
                action, action_data = self.view.choose_tournament_by_list(tournaments_info)

            if action == Request.SELECTED_TOURNAMENT:
                selected_tournament = action_data
                self.context = selected_tournament
                self.status = State.MANAGE_TOURNAMENT_MENU
            else:
                self.status = State.MANAGE_TOURNAMENTS_MENU
        else:
            self.status = State.MANAGE_TOURNAMENTS_MENU

    def show_manage_unready_tournament_menu(self):
        """The selected tournament did not start: display "unready" menu, then deal with the user’s request."""
        selected_tournament = self.context
        tournament_info = self.model.get_tournament_info(selected_tournament)
        action = self.view.show_manage_unready_tournament_menu(tournament_info)
        if action == Request.MANAGE_PARTICIPANTS:
            self.status = State.MANAGE_PARTICIPANTS_MENU
        elif action == Request.GENERATE_MATCHES:
            tournament_to_log, matches_to_log = self.model.start_tournament(selected_tournament)
            self.view.log(True, f"Tournament: {tournament_to_log} >>> started")
            self.view.log(True, f"{matches_to_log} matches >>> generated")
            self.status = State.MANAGE_TOURNAMENT_MENU
        else:
            self.status = State.MAIN_MENU

    def show_manage_tournament_menu(self):
        """The selected tournament started, display the normal tournament menu, then deal with the user’s request."""
        selected_tournament = self.context
        tournament_info = self.model.get_tournament_info(selected_tournament)
        if not self.model.tournaments[selected_tournament].rounds:
            self.status = State.MANAGE_UNREADY_TOURNAMENT_MENU
            return
        action = self.view.show_manage_tournament_menu(tournament_info)

        # ------------- to move ------------------------
        if action == Request.START_ROUND:
            self.model.start_round(selected_tournament)
            # self.view.log(True, f"round started {self.model.tournaments[selected_tournament].rounds}")
            self.status = State.MANAGE_TOURNAMENT_MENU
        if action == Request.LIST_PARTICIPANTS:
            self.status = State.LIST_PARTICIPANTS_MENU
        if action == Request.LIST_MATCHES:
            self.status = State.LIST_MATCHES_MENU
        if action == Request.LIST_ROUNDS_SCORES:
            self.status = State.LIST_ALL_ROUNDS_MENU
            # rounds = self.model.get_rounds(selected_tournament)
            # matches_info = [(match.participants_pair[0].player.identifier,
            #                 match.participants_pair[1].player.identifier)
            #                for round_r in range(len(rounds))
            #                for match in self.model.get_round_matches(selected_tournament, round_r)]
            # self.view.show_matches(matches_info)
        if action == Request.REGISTER_MATCH_SCORE:
            self.status = State.REGISTER_MATCH_SCORE_MENU
        if action == Request.MANAGE_TOURNAMENT:
            self.status = State.MANAGE_TOURNAMENTS_MENU

    def show_list_tournaments_menu(self):
        """Show the tournaments report list."""
        self.report(
            total=self.model.get_total_tournaments(),
            data_info=self.model.get_ordered_tournaments_str(),
            conjugated_name=self.conjugated_tournament,
            back_state=State.MANAGE_TOURNAMENTS_MENU,
        )
