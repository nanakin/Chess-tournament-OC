import datetime

from chess_tournament.views.requests import Request
from chess_tournament.models.model import Model


class Controller:

    def __init__(self, view, data_path):
        # view
        self.view = view
        # model
        self.model = Model(data_path)

        self.add_default_entries()  # temporary

    # temporary
    def add_default_entries(self):
        players_data = [
            {"identifier": "AB12345",
             "first_name": "Marie",
             "last_name": "Dupont",
             "birth_date": datetime.date.fromisoformat("1988-10-21")},
            {"identifier": "AB12346",
             "first_name": "Thomas",
             "last_name": "Marito",
             "birth_date": datetime.date.fromisoformat("1980-10-21")},
            {"identifier": "AA12345",
             "first_name": "Joan",
             "last_name": "Xiao",
             "birth_date": datetime.date.fromisoformat("1988-11-21")},
            {"identifier": "EB12345",
             "first_name": "Zak",
             "last_name": "Fara",
             "birth_date": datetime.date.fromisoformat("1928-10-11")},
            {"identifier": "AB42345",
             "first_name": "Pierre",
             "last_name": "Lacalu",
             "birth_date": datetime.date.fromisoformat("2000-01-21")},
            {"identifier": "AB12395",
             "first_name": "Julie",
             "last_name": "De la fontaine",
             "birth_date": datetime.date.fromisoformat("2010-10-01")},
        ]
        self.model.add_players(*players_data)
        print(self.model.players)
        tournaments_data = [
            {
                "name": "World Cup",
                "location": "Paris",
                "begin_date": datetime.date.fromisoformat("2010-10-01"),
                "end_date": datetime.date.fromisoformat("2010-10-31"),
                "total_rounds": 4,
            },
            {
                "name": "Coupe amateurs",
                "location": "Bordeaux",
                "begin_date": datetime.date.fromisoformat("2023-05-01"),
                "end_date": datetime.date.fromisoformat("2023-05-28"),
                "total_rounds": 4,
            }
        ]
        self.model.add_tournaments(*tournaments_data)
        self.model.add_participants_to_tournament(1, "AB42345", "EB12345", "AA12345", "AB12395")
        print(self.model.tournaments)

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

            if action == Request.GET_MATCHES_LIST:
                tournaments_info = [(t, tournament.name) for t, tournament in enumerate(self.model.tournaments)]
                action, action_data = self.view.choose_tournament(tournaments_info)
                tournament_t = action_data
                round_info = [(r, round.name) for r, round in enumerate(self.model.get_rounds(tournament_t))]
                action, action_data = self.view.choose_round(round_info)
                round_r = action_data
                matches_info = [(match[0].player.identifier, match[1].player.identifier)
                                for match in self.model.get_round_matches(tournament_t, round_r)]
                self.view.show_matches(matches_info)

            if action == Request.REGISTER_MATCH_SCORE:
                tournaments_info = [(t, tournament.name) for t, tournament in enumerate(self.model.tournaments)]
                action, action_data = self.view.choose_tournament(tournaments_info)
                if action == Request.EXIT_LOCAL_MENU:
                    pass
                elif action == Request.CHOSEN_TOURNAMENT:
                    tournament_t = action_data
                    matches = self.model.get_round_matches(tournament_t)
                    matches_info = [(m, match) for m, match in enumerate(matches) if match.participants_scores is None]
                    action, action_data = self.view.choose_match(matches_info)
                    if action == Request.CHOSEN_MATCH:
                        match_m = action_data
                        action, action_data = self.view.enter_score(None)
                        if action == Request.ADD_MATCH_RESULT:
                            first_player_result = action_data
                            self.model.register_score(tournament_t, match_m, first_player_result)

