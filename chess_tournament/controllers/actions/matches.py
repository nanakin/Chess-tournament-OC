from chess_tournament.controllers.states import State
from chess_tournament.views.requests import Request


class MatchesController:

    def show_register_match_score_menu(self):
        selected_tournament = self.context
        matches = self.model.get_round_matches(selected_tournament)
        matches_info = [f"{str(match.participants_pair[0].player)} vs {str(match.participants_pair[1].player)}"
                        for match in matches if
                        match.participants_scores is None]
        action, action_data = self.view.select_match(matches_info)
        if action == Request.SELECTED_MATCH:
            selected_match_index = action_data
            # to-do : review match selection because not optimized
            selected_match = [match for match in matches if match.participants_scores is None][selected_match_index]
            match_m = matches.index(selected_match)
            action, action_data = self.view.enter_score((
                str(selected_match.participants_pair[0].player), str(selected_match.participants_pair[1].player)))
            if action == Request.ADD_MATCH_RESULT:
                first_player_result = action_data
                self.model.register_score(selected_tournament, match_m, first_player_result)
                self.view.log(True, "score saved")
                self.status = State.MANAGE_TOURNAMENT_MENU
        else:
            self.status = State.MANAGE_TOURNAMENT_MENU
