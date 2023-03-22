from ..requests import Request, RequestAnswer
from ..interface import IView


class View(IView):

    def __init__(self):
        print("------------------- Chess Tournament Manager ---------------------")

    def show_main_menu(self) -> RequestAnswer:
        print("1 : to add player")
        print("2 : to add tournament")
        print("3 : to add participants to tournament")
        print("4 : to show round matches")
        print("5: to register a match score")
        print("q : to quit")
        action = input()
        if action == "q":
            return Request.EXIT_APP
        if action == "1":
            return Request.LAUNCH_PLAYER_MENU
        if action == "2":
            return Request.LAUNCH_TOURNAMENT_MENU
        if action == "3":
            return Request.LAUNCH_PARTICIPANT_MENU
        if action == "4":
            return Request.GET_MATCHES_LIST
        if action == "5":
            return Request.REGISTER_MATCH_SCORE

    def show_player_registration(self) -> RequestAnswer:
        # to-do : add a system to check user input values
        last_name = input("Enter player last name: ")
        first_name = input("Enter player first name: ")
        identifier = input("Enter player ID: ")
        birth_date = input("Enter player birth's date (using format YYYY-MM-DD): ")
        player_data = {"id": identifier, "last_name": last_name, "first_name": first_name, "birth_date": birth_date}
        return Request.ADD_PLAYER, player_data
        # to-do : or EXIT if cancel

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
