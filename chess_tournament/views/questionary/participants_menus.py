import questionary as q
from ..requests import Request, RequestAnswer
from .common import clear_screen_and_show_log, print_title


class ParticipantsMenus:
    @clear_screen_and_show_log
    def show_manage_participants_menu(self, total_participants):
        print_title("Participants menu")
        print(
            f"There {'is' if total_participants < 2 else 'are'} {total_participants} participant{'s' if total_participants > 1 else ''}"
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
        if not answer:
            return Request.MANAGE_TOURNAMENT
        return answer
