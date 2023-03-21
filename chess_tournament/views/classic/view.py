from ..requests import Request, RequestAnswer
from ..interface import IView


class View(IView):

    def __init__(self):
        print("------------------- Chess Tournament Manager ---------------------")

    def show_main_menu(self) -> RequestAnswer:
        print("1 : to add player")
        print("2 : to add tournament")
        print("q : to quit")
        action = input()
        if action == "q":
            return Request.EXIT_APP
        if action == "1":
            return Request.LAUNCH_PLAYER_MENU
        if action == "2":
            return Request.LAUNCH_TOURNAMENT_MENU

    def show_player_registration(self) -> RequestAnswer:
        # to-do : add a system to check user input values
        last_name = input("Enter player last name: ")
        first_name = input("Enter player first name: ")
        identifier = input("Enter player ID: ")
        birth_date = input("Enter player birth's date (using format YYYY/MM/DD): ")
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
