from ..requests import Request, RequestAnswer
from ..interface import IView
from ..validators import *
import questionary as q
import os


class View(IView):

    def __init__(self):
        q.print("------------------- Chess Tournament Manager ---------------------")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

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

    def show_manage_participants_menu(self, total_participants):
        print(f"There {'is' if total_participants < 2 else 'are'} {total_participants} participant{'s' if total_participants > 1 else ''}")
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title="Add participant", value=Request.ADD_PARTICIPANT),
                q.Choice(title="Delete participant", value=Request.DELETE_PARTICIPANT),
                q.Separator(),
                q.Choice(title="List participants", value=Request.LIST_PARTICIPANTS),
                q.Separator(),
                "Save",
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        answer = question.ask()
        if not answer:
            return Request.MANAGE_TOURNAMENT
        return answer


    def show_manage_unready_tournament_menu(self, tournament_info):
        choice_generate_matches = q.Choice(title=f"Generate pairs of the first round", value=Request.GET_MATCHES_LIST)
        if tournament_info["total_participants"] < 2:
            choice_generate_matches.disabled = "Not enough participants"
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title=f"Manage participants ({tournament_info['total_participants']})", value=Request.MANAGE_PARTICIPANTS),
                choice_generate_matches,
                q.Separator(),
                "Save",
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        answer = question.ask()
        if not answer:
            return Request.MANAGE_TOURNAMENT
        return answer

    def show_manage_tournament_menu(self, tournament_info):
        #print(f"selected tournament : {tournament_info['str']}")
        #print(f"{tournament_info['total_started_rounds']=}")
        #print(f"{tournament_info['total_matches']=}")
        #print(f'{tournament_info["name"]=}, {tournament_info["location"]=}, {tournament_info["begin_date"]=},'
        #      f'{tournament_info["end_date"]=}, {tournament_info["total_rounds"]=}, {tournament_info["total_started_rounds"]=},'
        #      f'{tournament_info["total_finished_matches"]=}, {tournament_info["total_matches"]=}',
        #      f'{tournament_info["total_finished_rounds"]=}, {tournament_info["total_participants"]=}')


        if tournament_info["total_matches"] == 0:
            choice_list_or_generate_matches = q.Choice(title="Generate matches", value=Request.GENERATE_MATCHES)
        else:
            choice_list_or_generate_matches = q.Choice(title="List matches of the current round", value=Request.LIST_MATCHES)

        if tournament_info["total_finished_matches"] == tournament_info["total_matches"]:
            choice_register_or_start_round = q.Choice(title="Start new round", value=Request.START_ROUND)
            if tournament_info["total_finished_rounds"] == tournament_info["total_rounds"]:
                choice_register_or_start_round.disabled = "All rounds ended"
        else:
            choice_register_or_start_round = q.Choice(title="Register a match score", value=Request.REGISTER_MATCH_SCORE)
        if tournament_info["total_participants"] < 2:
            choice_register_or_start_round.disabled = "Not enough participants"
            choice_list_or_generate_matches.disabled = "Not enough participants"

        question = q.select(
            "What do you want to do ?",
            choices=[
                choice_list_or_generate_matches,
                choice_register_or_start_round,
                q.Separator(),
                q.Choice(title="Summary report of all rounds and scores", value=Request.LIST_ROUNDS_SCORES),
                q.Separator(),
                "Save",
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        return question.ask()

    def keep_or_change_tournament(self, last_edited_tournament):
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title=f"Keep editing {last_edited_tournament}", value=Request.KEEP_SELECTED_TOURNAMENT),
                q.Choice(title="Select a new one", value=Request.CHANGE_SELECTED_TOURNAMENT),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        return question.ask()

    def select_match(self, matches_info) -> RequestAnswer:
        print(matches_info)
        question = q.select(
            "Which match ?",
            choices=matches_info)
             #   q.Separator(),
             #   q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        answer = question.ask()
        if answer:
            return Request.SELECTED_MATCH, matches_info.index(answer)
        else:
            return Request.MANAGE_TOURNAMENT, None

    def enter_score(self, match_info) -> RequestAnswer:
        # to-do : print the first player info or detail the 2 names in the choices
        question = q.select(
            "Select the result of the match, for the first player",
            choices=["WIN", "LOSE", "DRAW"])
        answer = question.ask()
        if answer:
            return Request.ADD_MATCH_RESULT, answer
        else:
            return Request.MANAGE_TOURNAMENT, None
