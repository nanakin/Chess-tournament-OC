"""Define matches related Controller’s behaviours."""

from chess_tournament.controllers.states import State
from chess_tournament.views.requests import Request
from chess_tournament.controllers.actions.common import CommonController
from ..helpers import ConjugatedWord


class MatchesController(CommonController):
    """Matches related Controller’s mixin class."""

    conjugated_match = ConjugatedWord(singular="match", plural="matches")

    def show_register_match_score_menu(self):
        """Show the score registration menu, register the score, then back to the tournament menu."""
        selected_tournament = self.context
        matches = self.model._get_round_matches(selected_tournament)
        matches_info = [
            f"{str(match.participants_pair[0].player)} vs {str(match.participants_pair[1].player)}"
            for match in matches
            if match.participants_scores is None
        ]
        action, action_data = self.view.select_match(matches_info)
        if action == Request.SELECTED_MATCH:
            selected_match_index = action_data
            # to-do : review match selection because not optimized
            selected_match = [match for match in matches if match.participants_scores is None][selected_match_index]
            match_m = matches.index(selected_match)
            action, action_data = self.view.enter_score(
                (
                    str(selected_match.participants_pair[0].player),
                    str(selected_match.participants_pair[1].player),
                )
            )
            if action == Request.ADD_MATCH_RESULT:
                first_player_result = action_data
                scores_to_log = self.model.register_score(selected_tournament, match_m, first_player_result)
                self.view.log(True, f"Scores: {scores_to_log}\n>>> registered")
                self.status = State.MANAGE_TOURNAMENT_MENU
            else:
                pass  # to review
        else:
            self.status = State.MANAGE_TOURNAMENT_MENU

    def show_list_matches_menu(self):
        """Show the matches report list of the current round (of the current tournament)."""
        selected_tournament = self.context
        self.report(
            total=self.model.get_total_matches(selected_tournament),
            data_info=self.model.get_matches_str(selected_tournament),
            conjugated_name=self.conjugated_match,
            back_state=State.MANAGE_TOURNAMENT_MENU,
        )

    def show_list_all_rounds_menu(self):
        """Show the matches report list of all generated rounds (of the current tournament)."""
        selected_tournament = self.context
        self.report(
            total=self.model.get_total_all_matches(selected_tournament),
            data_info=self.model.get_all_matches_str(selected_tournament),
            conjugated_name=self.conjugated_match,
            back_state=State.MANAGE_TOURNAMENT_MENU,
        )
