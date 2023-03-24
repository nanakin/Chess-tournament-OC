import questionary
import re
from ..requests import Request, RequestAnswer
from ..interface import IView
from . import questions
from datetime import date
import questionary as q


def non_empty_alphabet_validator(user_str):
    return re.match(r"^\w+((-|\s)(\w)+)*$", user_str) is not None


def past_date_validator(user_date_str):
    try:
        user_date = date.fromisoformat(user_date_str)
        return user_date < date.today()
    except ValueError:
        return False


def national_identifier_validator(user_id_str):
    return re.match(r"^[A-Za-z]{2}[0-9]{4}$", user_id_str) is not None


class View(IView):

    def __init__(self):
        q.print("------------------- Chess Tournament Manager ---------------------")

    def show_main_menu(self) -> RequestAnswer:
        q.print("==== Main Menu ===")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Manage players", value=Request.LAUNCH_PLAYER_MENU),
                q.Choice(title="Manage tournaments", value=Request.LAUNCH_TOURNAMENT_MENU),
                q.Separator(),
                "Save",
                q.Choice(title="Exit", value=Request.EXIT_APP)])
        return question.ask()


    def show_player_menu(self) -> RequestAnswer:
        pass


    def show_player_registration(self) -> RequestAnswer:
        q.print(">>>> Add Player >>>>")
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
                "filter": lambda x: date.fromisoformat(x)
            },
            {"type": "text", "name": "identifier", "qmark": ">",
             "message": "Enter player's national identifier :",
             "validate": national_identifier_validator}
        ]
        player_data = q.prompt(add_player_questions)
        return Request.ADD_PLAYER, player_data

    def show_status(self, ok_status, to_print=""):
        if ok_status:
            q.print(f"OK {to_print}")
        else:
            q.print(f"FAIL {to_print}")

    def show_tournament_registration(self) -> RequestAnswer:
        # to-do : add a system to check user input values
        tournament_data = {
            "name": input("Enter Tournament name: "),
            "location": input("Enter location: "),
            "begin_date": input("Enter begin date (using format YYYY/MM/DD): "),
            "end_date": input("Enter end date (using format YYYY/MM/DD): "),
            "total_rounds": input("Total number of rounds (leave empty for default value: 4): ")}

        return Request.ADD_TOURNAMENT, tournament_data
        # to-do or EXIT if cancel

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

    def choose_tournament(self, tournaments_info) -> RequestAnswer:
        print("Select a tournament:")
        for n, tournament_info in enumerate(tournaments_info):
            print(f"{n}: {tournament_info[1]}")
        tournament_t = tournaments_info[int(input())][0]
        return Request.CHOSEN_TOURNAMENT, tournament_t

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