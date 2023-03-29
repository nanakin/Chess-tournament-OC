import questionary as q
from ..requests import Request, RequestAnswer
from ..validators import *
from .common import clear_screen_and_show_log

class TournamentsMenus:

    @clear_screen_and_show_log
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

    @clear_screen_and_show_log
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

    @clear_screen_and_show_log
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

    @clear_screen_and_show_log
    def keep_or_change_tournament(self, last_edited_tournament):
        question = q.select(
            "What do you want to do ?",
            choices=[
                q.Choice(title=f"Keep editing {last_edited_tournament}", value=Request.KEEP_SELECTED_TOURNAMENT),
                q.Choice(title="Select a new one", value=Request.CHANGE_SELECTED_TOURNAMENT),
                q.Separator(),
                q.Choice(title="Back", value=Request.MANAGE_TOURNAMENT)])
        return question.ask()

    @clear_screen_and_show_log
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

    @clear_screen_and_show_log
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

    @clear_screen_and_show_log
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