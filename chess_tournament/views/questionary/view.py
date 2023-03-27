import questionary
import re
from ..requests import Request, RequestAnswer
from ..interface import IView
from datetime import date
import questionary as q


def non_empty_alphabet_validator(user_str):
    return re.match(r"^\w+((-|\s)(\w)+)*$", user_str) is not None


def date_validator(user_date_str):
    try:
        date.fromisoformat(user_date_str)
        return True
    except ValueError:
        return False

def past_date_validator(user_date_str):
    try:
        user_date = date.fromisoformat(user_date_str)
        return user_date < date.today()
    except ValueError:
        return False


def national_identifier_validator(user_id_str):
    return re.match(r"^[A-Za-z]{2}[0-9]{5}$", user_id_str) is not None


class View(IView):

    def __init__(self):
        q.print("------------------- Chess Tournament Manager ---------------------")

    def show_main_menu(self) -> RequestAnswer:
        q.print("==== Main Menu ===")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Manage players", value=Request.MANAGE_PLAYER),
                q.Choice(title="Manage tournaments", value=Request.MANAGE_TOURNAMENT),
                q.Separator(),
                "Save",
                q.Choice(title="Exit", value=Request.EXIT_APP)])
        return question.ask()


    def show_manage_player_menu(self) -> RequestAnswer:
        q.print("==== Player Menu ===")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Add player", value=Request.ADD_PLAYER),
                q.Choice(title="Edit player", value=Request.EDIT_PLAYER),
                q.Choice(title="List players", value=Request.LIST_PLAYERS),
                q.Separator(),
                "Save",
                q.Choice(title="Back", value=Request.MAIN_MENU)])
        return question.ask()

    def show_list_players_menu(self, total_players):
        q.print(f"Total {total_players} players")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Print list", value=Request.PRINT_PLAYERS),
                q.Choice(title="Export list", value=Request.EXPORT_PLAYERS),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_PLAYER)])
        return question.ask()

    def print_players(self, players_info):
        for player_info in players_info:
            q.print(player_info)

    def show_player_selection(self, players_id):
        question = q.autocomplete(
            "Enter the player ID :",
            choices=players_id, validate=lambda x: x in players_id)
        return Request.SELECTED_PLAYER, question.ask()

    def show_confirmation(self, to_confirm):
        return Request.CONFIRM, q.confirm(to_confirm).ask()

    def show_player_registration(self) -> RequestAnswer:
        add_player_questions = [
            {
                "type": "text", "name": "first_name", "qmark": ">",
                "message": "Enter player's first name :",
                "validate": non_empty_alphabet_validator
            },
            {
                "type": "text", "name": "last_name", "qmark": ">",
                "message": "Enter player's last name :",
                "validate": non_empty_alphabet_validator
             },
            {
                "type": "text", "name": "birth_date", "qmark": ">",
                "message": "Enter player's date of birth (YYYY-MM-DD):",
                "validate": past_date_validator,
            },
            {"type": "text", "name": "identifier", "qmark": ">",
             "message": "Enter player's national identifier :",
             "validate": national_identifier_validator}
        ]
        raw_player_data = q.prompt(add_player_questions)
        if not raw_player_data:  # ctrl-c
            return Request.MANAGE_PLAYER, None
        else:
            return Request.REGISTER_PLAYER_DATA, raw_player_data

    def show_edit_player_menu(self, player_info):
        what_to_edit = q.select("What to edit ?", choices=[
            q.Choice(title="First name", value="first_name"),
            q.Choice(title="Last name", value="last_name"),
            q.Choice(title="Birth date", value="birth_date"),
            q.Choice(title="Cancel")
        ])
        answer = what_to_edit.ask()
        if answer == "first_name":
            player_info["first_name"] = q.text("Enter player's new first name: ", validate=non_empty_alphabet_validator).ask()
        elif answer == "last_name":
            player_info["last_name"] = q.text("Enter player's new last name: ", validate=non_empty_alphabet_validator).ask()
        elif answer == "birth_date":
            player_info["birth_date"] = q.text("Enter player's new birth date: ", validate=past_date_validator).ask()
        else:
            return Request.MANAGE_PLAYER, None
        return Request.REGISTER_PLAYER_DATA, player_info

    def show_status(self, ok_status, to_print=""):
        if ok_status:
            q.print(f"🟢 OK : {to_print}")
        else:
            q.print(f"🟥 FAIL {to_print}")

    def show_manage_tournaments_menu(self):
        q.print("==== Tournament Menu ===")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Register a new tournament", value=Request.ADD_TOURNAMENT),
                q.Choice(title="Manage existing tournament", value=Request.EDIT_TOURNAMENT),
                q.Choice(title="List tournaments", value=Request.LIST_TOURNAMENTS),
                q.Separator(),
                "Save",
                q.Choice(title="Back", value=Request.MAIN_MENU)])
        return question.ask()

    def show_tournament_registration(self) -> RequestAnswer:
        add_tournament_questions = [
            {
                "type": "text", "name": "name", "qmark": ">",
                "message": "Enter Tournament name :",
                "validate": lambda x: len(x.strip()) > 0
            },
            {
                "type": "text", "name": "location", "qmark": ">",
                "message": "Enter location :",
                "validate": non_empty_alphabet_validator
            },
            {
                "type": "text", "name": "begin_date", "qmark": ">",
                "message": "Enter begin date (YYYY-MM-DD):",
                "validate": date_validator,
            },
            {
                "type": "text", "name": "end_date", "qmark": ">",
                "message": "Enter end date (YYYY-MM-DD):",
                "validate": date_validator,
            },
            {"type": "text", "name": "total_rounds", "qmark": ">",
             "message": "Total number of rounds :",
             "validate": lambda x: x.isnumeric(),
             "default": "4"}
        ]
        raw_tournament_data = q.prompt(add_tournament_questions)
        if not raw_tournament_data:  # ctrl-c
            return Request.MANAGE_TOURNAMENT, None
        else:
            return Request.REGISTER_TOURNAMENT_DATA, raw_tournament_data

    def show_participant_registration(self, tournaments_info) -> RequestAnswer:
        # tournaments_info = list[tuple[index, name]]
        # to-do : add a system to check user input values
        print("Select a tournament:")
        for n, tournament_info in enumerate(tournaments_info):
            print(f"{n}: {tournament_info[1]}")
        tournament_t = tournaments_info[int(input()) - 1][0]
        player_id = input("Enter player ID: ")
        add_participant_data = {"player_id": player_id, "tournament_t": tournament_t}
        return Request.ADD_PARTICIPANT, add_participant_data
        # to-do or EXIT if cancel

    def show_matches(self, matches):
        print("List of matches :")
        for match in matches:
            print(match)

    def how_to_choose_tournament(self, statistics) -> RequestAnswer:
        question = q.select(
            "Which tournament do you want to manage ?",
            choices=[
                q.Choice(title="Find by name", value=Request.FIND_TOURNAMENT_BY_NAME),
                q.Choice(title=f"Find from list of ongoing tournaments ({statistics['ongoing']})", value=Request.FIND_TOURNAMENT_BY_LIST_ONGOING),
                q.Choice(title=f"Find from list of future tournaments ({statistics['future']})", value=Request.FIND_TOURNAMENT_BY_LIST_FUTURE),
                q.Choice(title=f"Find from list of past tournaments ({statistics['past']})", value=Request.FIND_TOURNAMENT_BY_LIST_PAST),
                q.Choice(title=f"Find from list of all tournaments ({statistics['all']})", value=Request.FIND_TOURNAMENT_BY_LIST_ALL),
                q.Separator(),
                "Save",
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        return question.ask()

    def choose_tournament_by_name(self, tournaments_info):
        tournaments_meta = {f"{t}- {tournament_info[0]}": tournament_info[1] for t, tournament_info in enumerate(tournaments_info)}
        question = q.autocomplete(
            "Enter the tournament name :",
            choices=list(tournaments_meta.keys()), meta_information=tournaments_meta, validate=lambda x: x in list(tournaments_meta.keys()))
        answer = question.ask()
        if answer is None:
            return Request.EDIT_TOURNAMENT, None
        else:
            selected_tournament = int(answer.partition("-")[0])
            return Request.SELECTED_TOURNAMENT, selected_tournament

    def show_manage_tournament_menu(self, tournament_info):
        print(f"selected tournament : {tournament_info['str']}")
        #print(f'{tournament_info["name"]=}, {tournament_info["location"]=}, {tournament_info["begin_date"]=},'
        #      f'{tournament_info["end_date"]=}, {tournament_info["total_rounds"]=}, {tournament_info["total_started_rounds"]=},'
        #      f'{tournament_info["total_finished_matches"]=}, {tournament_info["total_matches"]=}',
        #      f'{tournament_info["total_finished_rounds"]=}, {tournament_info["total_participants"]=}')

        choice_manage_participant = q.Choice(title="Manage participants", value=Request.MANAGE_PARTICIPANTS)
        choice_list_matches = q.Choice(title="List matches of the current round", value=Request.LIST_MATCHES)

        if tournament_info["total_started_rounds"] > 0:
            choice_manage_participant.disabled = "Tournament already started"
        if tournament_info["total_finished_matches"] == tournament_info["total_matches"]:
            choice_register_or_start_round = q.Choice(title="Start new round", value=Request.LIST_TOURNAMENTS)
            if tournament_info["total_finished_rounds"] == tournament_info["total_rounds"]:
                choice_register_or_start_round.disabled = "All rounds ended"
        else:
            choice_register_or_start_round = q.Choice(title="Register a match score", value=Request.LIST_TOURNAMENTS)

        question = q.select(
            "What do you want to do ?",
            choices=[
                choice_manage_participant,
                q.Choice(title="List matches of the current round", value=Request.LIST_MATCHES),
                choice_register_or_start_round,
                q.Separator(),
                q.Choice(title="Summary report of all rounds and scores", value=Request.LIST_ROUNDS_SCORES),
                q.Separator(),
                "Save",
                q.Choice(title="Back", value=Request.MAIN_MENU)])
        return question.ask()

    def choose_match(self, matches_info) -> RequestAnswer:
        print("Select the match: ")
        for m, match_info in enumerate(matches_info):
            print(match_info)
        match_m = int(input())
        return Request.CHOSEN_MATCH, match_m

    def choose_round(self, rounds):
        print("Select a round: ")
        for r, round in enumerate(rounds):
            print(r, round)
        round_r = int(input())
        return Request.CHOSEN_ROUND, round_r

    def enter_score(self, match_info) -> RequestAnswer:
        print(match_info)
        print("Enter the first player result : WIN, LOSE, or DRAW")
        first_score = input()
        return Request.ADD_MATCH_RESULT, first_score