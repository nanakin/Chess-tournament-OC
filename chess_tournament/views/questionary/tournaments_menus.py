"""Define chess tournaments related user interface."""

import questionary as q
from ..requests import Request, RequestAnswer, valid_request_or_exit
from ..validators import non_empty_alphabet_validator, date_validator
from .common import (
    clear_screen_and_show_log,
    print_title,
    print_important_info,
)


class TournamentsMenus:
    """Tournaments related View’s mixin class."""

    @clear_screen_and_show_log
    def show_manage_tournaments_menu(self):
        """Display a select menu to add/manage/list tournaments and back."""
        print_title("Tournaments menu")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Register a new tournament", value=Request.ADD_TOURNAMENT),
                q.Choice(title="Manage existing tournament", value=Request.EDIT_TOURNAMENT),
                q.Choice(title="List tournaments", value=Request.LIST_TOURNAMENTS),
                q.Separator(),
                q.Choice(title="Back", value=Request.MAIN_MENU),
            ],
        )
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=answer)

    @clear_screen_and_show_log
    def show_manage_unready_tournament_menu(self, tournament_info):
        """Display a select menu to manage participants or start the selected tournament."""
        print_title("Unready tournament menu")
        print_important_info(f"{tournament_info['str']}")
        choice_start_tournament = q.Choice(title="Start tournament", value=Request.GENERATE_MATCHES)
        if tournament_info["total_participants"] < 2:
            choice_start_tournament.disabled = "Not enough participants"
        elif tournament_info["total_participants"] % 2 == 1:
            choice_start_tournament.disabled = "Select an even number of participants"
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(
                    title=f"Manage participants ({tournament_info['total_participants']})",
                    value=Request.MANAGE_PARTICIPANTS,
                ),
                choice_start_tournament,
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT),
            ],
        )
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=answer)

    @clear_screen_and_show_log
    def show_manage_tournament_menu(self, tournament_info):
        """Display a select menu to manage rounds and scores of the selected tournament."""
        print_title("Tournament menu")
        print_important_info(f"{tournament_info['str']}")
        choices = []
        if tournament_info["total_finished_rounds"] < tournament_info["total_rounds"]:
            print_important_info(
                f"{tournament_info['current_round_name']} ({tournament_info['total_started_rounds']}" +
                f"/{tournament_info['total_rounds']})")
            if not tournament_info["is_current_round_started"]:
                choice_register_or_start_round = q.Choice(title="Start the round", value=Request.START_ROUND)
            else:
                choice_register_or_start_round = q.Choice(
                    title="Register a match score", value=Request.REGISTER_MATCH_SCORE
                )
            choices.extend(
                [
                    choice_register_or_start_round,
                    q.Separator(),
                    q.Choice(
                        title="List matches of the current round",
                        value=Request.LIST_MATCHES,
                    ),
                ]
            )
        else:
            print_important_info("Tournament Ended")
            q.print(f"Top {len(tournament_info['winners'])} players " +
                    f"({tournament_info['total_participants']} participants):")
            for position, participant in enumerate(tournament_info["winners"]):
                q.print(f"{position + 1}: {participant}")

        choices.extend(
            [
                q.Choice(
                    title="List all rounds matches (and scores)",
                    value=Request.LIST_ROUNDS_SCORES,
                ),
                q.Choice(title="List participants", value=Request.LIST_PARTICIPANTS),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT),
            ]
        )

        question = q.select("What do you want to do ?", choices=choices)
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=answer)

    @clear_screen_and_show_log
    def keep_or_change_tournament(self, last_edited_tournament):
        """Display a select menu to choose between keep editing the last selected tournament or change."""
        print_title("Tournament selection menu")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(
                    title=f"Keep editing {last_edited_tournament}",
                    value=Request.KEEP_SELECTED_TOURNAMENT,
                ),
                q.Choice(title="Select a new one", value=Request.CHANGE_SELECTED_TOURNAMENT),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT),
            ],
        )
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=answer)

    @clear_screen_and_show_log
    def show_tournament_registration(self) -> RequestAnswer:
        """Prompt 5 input questions (name, location, dates, rounds number) with user entries validation."""
        print_title("Tournament registration menu")
        add_tournament_questions = [
            {
                "type": "text",
                "name": "name",
                "qmark": ">",
                "message": "Enter Tournament name :",
                "validate": lambda x: len(x.strip()) > 0,
            },
            {
                "type": "text",
                "name": "location",
                "qmark": ">",
                "message": "Enter location :",
                "validate": non_empty_alphabet_validator,
            },
            {
                "type": "text",
                "name": "begin_date",
                "qmark": ">",
                "message": "Enter begin date (YYYY-MM-DD):",
                "validate": date_validator,
            },
            {
                "type": "text",
                "name": "end_date",
                "qmark": ">",
                "message": "Enter end date (YYYY-MM-DD):",
                "validate": date_validator,
            },
            {
                "type": "text",
                "name": "total_rounds",
                "qmark": ">",
                "message": "Total number of rounds :",
                "validate": lambda x: x.isnumeric(),
                "default": "4",
            },
        ]
        raw_tournament_data = q.prompt(add_tournament_questions)
        return valid_request_or_exit(check=raw_tournament_data,
                                     return_if_ok=(Request.REGISTER_TOURNAMENT_DATA, raw_tournament_data))

    @clear_screen_and_show_log
    def how_to_choose_tournament(self, statistics) -> RequestAnswer:
        """Display a select menu to choose the filter and the method to find an existing tournament."""
        print_title("Tournament selection method menu")
        question = q.select(
            "Which tournament do you want to manage ?",
            choices=[
                q.Choice(title="Find by name", value=Request.FIND_TOURNAMENT_BY_NAME),
                q.Choice(
                    title=f"Find from list of ongoing tournaments ({statistics['ongoing']})",
                    value=Request.FIND_TOURNAMENT_BY_LIST_ONGOING,
                ),
                q.Choice(
                    title=f"Find from list of future tournaments ({statistics['future']})",
                    value=Request.FIND_TOURNAMENT_BY_LIST_FUTURE,
                ),
                q.Choice(
                    title=f"Find from list of past tournaments ({statistics['past']})",
                    value=Request.FIND_TOURNAMENT_BY_LIST_PAST,
                ),
                q.Choice(
                    title=f"Find from list of all tournaments ({statistics['all']})",
                    value=Request.FIND_TOURNAMENT_BY_LIST_ALL,
                ),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT),
            ],
        )
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=answer)

    @clear_screen_and_show_log
    def choose_tournament_by_name(self, tournaments_info):
        """Display an autocomplete question for the tournament name."""
        print_title("Tournament selection menu")
        tournaments_meta = {
            f"{t_index}- {tournament_name}": tournament_str
            for t_index, tournament_name, tournament_str in tournaments_info
        }
        question = q.autocomplete(
            "Enter the tournament name :",
            choices=list(tournaments_meta.keys()),
            meta_information=tournaments_meta,
            validate=lambda x: x in list(tournaments_meta.keys()),
        )
        answer = question.ask()
        return valid_request_or_exit(check=answer,
                                     return_if_ok=(Request.SELECTED_TOURNAMENT, int(answer.partition("-")[0])))

    @clear_screen_and_show_log
    def choose_tournament_by_list(self, tournaments_info):
        """Display a select menu with a list of tournaments."""
        print_title("Tournament selection menu")
        choices = [q.Choice(title=tournament_name, value=t_index) for t_index, tournament_name, _ in tournaments_info]
        choices.extend([q.Separator(), q.Choice("Back")])
        question = q.select("Select a tournament: ", choices=choices)
        answer = question.ask()
        return valid_request_or_exit(check=answer, return_if_ok=(Request.SELECTED_TOURNAMENT, answer))
