"""Define tournaments related Controller’s behaviours."""

from chess_tournament.controllers.states import State
from chess_tournament.models.model import InconsistentDates
from chess_tournament.views.requests import Request

from ..helpers import ConjugatedWord
from .common import CommonController


class TournamentsController(CommonController):
    """Tournaments related Controller’s mixin class."""

    conjugated_tournament = ConjugatedWord(singular="tournament", plural="tournaments")

    def show_manage_tournaments_menu(self) -> None:
        """Show the main tournaments menu and redirect the user’s request to the main state manager system."""
        request, _ = self.view.show_manage_tournaments_menu()
        if request == Request.ADD_TOURNAMENT:
            self.status = State.ADD_TOURNAMENT_MENU
        elif request == Request.EDIT_TOURNAMENT:
            if self.context is not None:
                selected_tournament = self.context
                tournament_info = self.model.get_tournament_info(selected_tournament)["str"]
                request, _ = self.view.keep_or_change_tournament(tournament_info)
                if request == Request.KEEP_SELECTED_TOURNAMENT:
                    self.status = State.MANAGE_TOURNAMENT_MENU
                elif request == Request.CHANGE_SELECTED_TOURNAMENT:
                    self.context = None
                    self.status = State.SELECT_TOURNAMENT_MENU
            else:
                self.status = State.SELECT_TOURNAMENT_MENU
        elif request == Request.LIST_TOURNAMENTS:
            self.status = State.LIST_TOURNAMENTS_MENU
        else:
            self.status = State.MAIN_MENU

    def show_tournament_registration(self) -> None:
        """Show the tournament registration menu, register the tournament, then back to the previous state."""
        request, request_data = self.view.show_tournament_registration()
        if request == Request.REGISTER_TOURNAMENT_DATA:
            tournament_data = request_data
            try:
                tournament_to_log = self.model.add_tournaments(tournament_data)
            except InconsistentDates as err:
                self.view.log(False, err.args[0] + " >>> not created")
            else:
                self.view.log(True, f"Tournament: {tournament_to_log} >>> created")
        self.status = State.MANAGE_TOURNAMENTS_MENU

    def show_select_tournament_menu(self) -> None:
        """Show methods to choose, then list tournament to select from, register selection in the context."""
        # improvement : use round info to know if a tournament really ended
        statistics = self.model.get_tournaments_states_statistics()
        request, _ = self.view.how_to_choose_tournament(statistics)
        if request in (
            Request.FIND_TOURNAMENT_BY_NAME,
            Request.FIND_TOURNAMENT_BY_LIST_ONGOING,
            Request.FIND_TOURNAMENT_BY_LIST_FUTURE,
            Request.FIND_TOURNAMENT_BY_LIST_PAST,
            Request.FIND_TOURNAMENT_BY_LIST_ALL,
        ):
            if request == Request.FIND_TOURNAMENT_BY_NAME:
                tournaments_info = self.model.get_tournaments_str()
                if tournaments_info:
                    request, request_data = self.view.choose_tournament_by_name(tournaments_info)
                else:
                    self.view.log(False, "Tournaments list is empty")
            else:
                if request == Request.FIND_TOURNAMENT_BY_LIST_ONGOING:
                    tournaments_info = self.model.get_tournaments_str("ongoing")
                elif request == Request.FIND_TOURNAMENT_BY_LIST_FUTURE:
                    tournaments_info = self.model.get_tournaments_str("future")
                elif request == Request.FIND_TOURNAMENT_BY_LIST_PAST:
                    tournaments_info = self.model.get_tournaments_str("past")
                elif request == Request.FIND_TOURNAMENT_BY_LIST_ALL:
                    tournaments_info = self.model.get_tournaments_str("all")
                if tournaments_info:
                    request, request_data = self.view.choose_tournament_by_list(tournaments_info)
                else:
                    self.view.log(False, "Tournaments list is empty")

            if request == Request.SELECTED_TOURNAMENT:
                selected_tournament = request_data
                self.context = selected_tournament
                self.status = State.MANAGE_TOURNAMENT_MENU
                return
        self.status = State.MANAGE_TOURNAMENTS_MENU

    def show_manage_unready_tournament_menu(self) -> None:
        """The selected tournament did not start: display "unready" menu, then deal with the user’s request."""
        selected_tournament = self.context
        tournament_info = self.model.get_tournament_info(selected_tournament)
        request, _ = self.view.show_manage_unready_tournament_menu(tournament_info)
        if request == Request.MANAGE_PARTICIPANTS:
            self.status = State.MANAGE_PARTICIPANTS_MENU
        elif request == Request.GENERATE_MATCHES:
            tournament_to_log, matches_to_log = self.model.start_tournament(selected_tournament)
            self.view.log(True, f"Tournament: {tournament_to_log} >>> started")
            self.view.log(True, f"{matches_to_log} matches >>> generated")
            self.status = State.MANAGE_TOURNAMENT_MENU
        else:
            self.status = State.MAIN_MENU

    def show_manage_tournament_menu(self) -> None:
        """The selected tournament started, display the normal tournament menu, then deal with the user’s request."""
        selected_tournament = self.context
        tournament_info = self.model.get_tournament_info(selected_tournament)
        if not self.model.tournaments[selected_tournament].rounds:
            self.status = State.MANAGE_UNREADY_TOURNAMENT_MENU
            return
        request, _ = self.view.show_manage_tournament_menu(tournament_info)

        request_to_status = {
            Request.START_ROUND: State.MANAGE_TOURNAMENT_MENU,
            Request.LIST_PARTICIPANTS: State.LIST_PARTICIPANTS_MENU,
            Request.LIST_MATCHES: State.LIST_MATCHES_MENU,
            Request.LIST_ROUNDS_SCORES: State.LIST_ALL_ROUNDS_MENU,
            Request.REGISTER_MATCH_SCORE: State.REGISTER_MATCH_SCORE_MENU,
        }

        if request in request_to_status:
            self.status = request_to_status[request]
            if request == Request.START_ROUND:
                self.model.start_round(selected_tournament)
        else:
            self.status = State.MANAGE_TOURNAMENTS_MENU

    def show_list_tournaments_menu(self) -> None:
        """Show the tournaments report list."""
        self.report(
            total=self.model.get_total_tournaments(),
            data_info=self.model.get_ordered_tournaments_str(),
            conjugated_name=self.conjugated_tournament,
            back_state=State.MANAGE_TOURNAMENTS_MENU,
        )
