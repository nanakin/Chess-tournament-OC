from chess_tournament.controllers.states import State
from chess_tournament.views.requests import Request
import datetime


class TournamentsController:
    def show_tournament_registration(self):
        action, action_data = self.view.show_tournament_registration()
        if action == Request.REGISTER_TOURNAMENT_DATA:
            tournament_data = action_data
            try:
                self.model.add_tournaments(tournament_data)
                self.view.log(True, "correctly added")  # to-do: change message
            except AlreadyUsedID as err:
                self.view.log(False)
        self.status = State.MANAGE_TOURNAMENTS_MENU

    def show_select_tournament_menu(self):
        # improvement : use round info to know if a tournament really ended
        statistics = {
            "all": len(self.model.tournaments),
            "ongoing": sum(1 for tournament in self.model.tournaments if
                           tournament.end_date <= datetime.date.today() >= tournament.begin_date),
            "future": sum(
                1 for tournament in self.model.tournaments if tournament.begin_date > datetime.date.today()),
            "past": sum(1 for tournament in self.model.tournaments if tournament.end_date < datetime.date.today())
        }
        action = self.view.how_to_choose_tournament(statistics)
        if action == Request.FIND_TOURNAMENT_BY_NAME:
            tournaments_info = self.model.get_tournaments_str()
            action, action_data = self.view.choose_tournament_by_name(tournaments_info)
            if action == Request.SELECTED_TOURNAMENT:
                selected_tournament = action_data
                self.context = selected_tournament
                self.status = State.MANAGE_TOURNAMENT_MENU
        else:
            self.status = State.MANAGE_TOURNAMENTS_MENU

    def show_manage_unready_tournament_menu(self):
        selected_tournament = self.context
        tournament_info = self.model.get_tournament_info(selected_tournament)
        action = self.view.show_manage_unready_tournament_menu(tournament_info)
        if action == Request.MANAGE_PARTICIPANTS:
            self.status = State.MANAGE_PARTICIPANTS_MENU
        elif action == Request.GET_MATCHES_LIST:
            matches_info = [(match.participants_pair[0].player.identifier,
                             match.participants_pair[1].player.identifier)
                            for match in self.model.get_round_matches(selected_tournament)]
            self.view.show_matches(matches_info)
            self.status = State.MANAGE_TOURNAMENT_MENU
        else:
            self.status = State.MAIN_MENU

    def show_manage_tournament_menu(self):
        # main menu (if not started) : manage participants or start tournament
        # main menu (if started) : same as this one but without participants
        selected_tournament = self.context
        tournament_info = self.model.get_tournament_info(selected_tournament)
        if not self.model.tournaments[selected_tournament].rounds:
            self.status = State.MANAGE_UNREADY_TOURNAMENT_MENU
            return
        action = self.view.show_manage_tournament_menu(tournament_info)

        # ------------- to move ------------------------
        if action == Request.START_ROUND:
            self.model.start_round(selected_tournament)
            self.view.log(True, f"round started {self.model.tournaments[selected_tournament].rounds}")
            self.status = State.MANAGE_TOURNAMENT_MENU
        if action == Request.GET_MATCHES_LIST:
            round_r = self.model.get_rounds(selected_tournament)[-1]
            matches_info = [(match.participants_pair[0].player.identifier,
                             match.participants_pair[1].player.identifier)
                            for match in self.model.get_round_matches(selected_tournament, round_r)]
            self.view.show_matches(matches_info)
        if action == Request.REGISTER_MATCH_SCORE:
            self.status = State.REGISTER_MATCH_SCORE_MENU
        if action == Request.MANAGE_TOURNAMENT:
            self.status = State.MANAGE_TOURNAMENTS_MENU

    def show_manage_tournaments_menu(self):
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
            pass  # to-do
        else:
            self.status = State.MAIN_MENU
