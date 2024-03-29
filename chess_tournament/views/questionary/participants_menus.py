"""Define chess participants related user interface."""

import questionary as q

from ..requests import Request, RequestAnswer, valid_request_or_exit
from .common import clear_screen_and_show_log, print_title


class ParticipantsMenus:
    """Participants related View’s mixin class."""

    @clear_screen_and_show_log
    def show_manage_participants_menu(self, total_participants: int) -> RequestAnswer:
        """Display a select menu to manage participants (add/delete/list participants and back)."""
        print_title("Participants menu")
        q.print(
            f"There {'is' if total_participants < 2 else 'are'} {total_participants} "
            f"participant{'s' if total_participants > 1 else ''} \r",
        )
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Add participant", value=Request.ADD_PARTICIPANT),
                q.Choice(title="Delete participant", value=Request.DELETE_PARTICIPANT),
                q.Separator(),
                q.Choice(title="List participants", value=Request.LIST_PARTICIPANTS),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT),
            ],
        )
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=answer)
