"""Define chess matches related user interface."""
import questionary as q

from ..requests import Request, RequestAnswer, valid_request_or_exit
from .common import clear_screen_and_show_log, print_title


class MatchesMenus:
    """Matches related View’s mixin class."""

    @clear_screen_and_show_log
    def select_match(self, matches_info) -> RequestAnswer:
        """Display a select menu with the round’s matches list."""
        print_title("Match selection menu")
        question = q.select("Which match ?", choices=matches_info)
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=(
            Request.SELECTED_MATCH, matches_info.index(answer) if answer else None))

    @clear_screen_and_show_log
    def enter_score(self, players) -> RequestAnswer:
        """Display a select menu to choose the participants score (WIN/LOSE/DRAW)."""
        print_title("Score registration menu")
        question = q.select(
            "Select the result of the match, for the first player",
            choices=[
                q.Choice(title=f"{players[0]}: WIN  - {players[1]}: LOSE ", value="WIN"),
                q.Choice(title=f"{players[0]}: LOSE - {players[1]}: WIN ", value="LOSE"),
                q.Choice(title="DRAW", value="DRAW"),
            ],
        )
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=(Request.ADD_MATCH_RESULT, answer))
