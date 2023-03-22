import datetime

from chess_tournament.views.requests import Request
from chess_tournament.models.model import Model


class Controller:

    def __init__(self, view, data_path):
        # view
        self.view = view
        # model
        self.model = Model(data_path)

    def run(self):
        running = True
        while running:
            action = self.view.show_main_menu()

            if action == Request.EXIT_APP:
                running = False

            if action == Request.LAUNCH_PLAYER_MENU:
                action, action_data = self.view.show_player_registration()
                if action == Request.EXIT_LOCAL_MENU:
                    break
                if action == Request.ADD_PLAYER:
                    self.model.add_players(action_data)

            if action == Request.LAUNCH_TOURNAMENT_MENU:
                action, action_data = self.view.show_tournament_registration()
                if action == Request.EXIT_LOCAL_MENU:
                    break
                if action == Request.EXIT_LOCAL_MENU:
                    self.model.add_tournaments(action_data)

            if action == Request.LAUNCH_PARTICIPANT_MENU:
                tournaments_info = [(t, tournament.name) for t, tournament in enumerate(self.model.tournaments)
                                    if tournament.end_date >= datetime.date.today()]
                action, action_data = self.view.show_participant_registration(tournaments_info)
                if action == Request.ADD_PARTICIPANT:
                    self.model.add_participants_to_tournament(action_data)
