import datetime
from enum import Enum
from chess_tournament.views.requests import Request
from chess_tournament.models.model import Model, AlreadyUsedID

State = Enum("State", [
    "MAIN_MENU",
    "MANAGE_PLAYER_MENU",
    "ADD_PLAYER_MENU",
    "EDIT_PLAYER_MENU",
    "LIST_PLAYERS_MENU",
    "MANAGE_TOURNAMENTS_MENU",
    "ADD_TOURNAMENT_MENU",
    "REGISTER_MATCH_SCORE_MENU",
    "ADD_PARTICIPANT_MENU",
    "DELETE_PARTICIPANT_MENU",
    "MANAGE_PARTICIPANTS_MENU",
    "MANAGE_TOURNAMENT_MENU",
    "MANAGE_UNREADY_TOURNAMENT_MENU",
    "SELECT_TOURNAMENT_MENU",
    "QUIT"])

class Controller:

    def __init__(self, view, data_path):
        # view
        self.view = view
        # model
        self.model = Model(data_path)

        self.status = State.MAIN_MENU
        self.context = None

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



    def run(self):
        def show_main_menu():
            action = self.view.show_main_menu()
            if action == Request.EXIT_APP:
                self.status = State.QUIT
            elif action == Request.SAVE:
                pass
            elif action == Request.MANAGE_PLAYER:
                self.status = State.MANAGE_PLAYER_MENU
            elif action == Request.MANAGE_TOURNAMENT:
                self.status = State.MANAGE_TOURNAMENTS_MENU
            else:
                self.status = State.QUIT

        def show_manage_player_menu():
            action = self.view.show_manage_player_menu()
            if action == Request.MAIN_MENU:
                self.status = State.MAIN_MENU
            elif action == Request.ADD_PLAYER:
                self.status = State.ADD_PLAYER_MENU
            elif action == Request.EDIT_PLAYER:
                self.status = State.EDIT_PLAYER_MENU
            elif action == Request.LIST_PLAYERS:
                self.status = State.LIST_PLAYERS_MENU
            else:
                self.status = State.MAIN_MENU

        def show_edit_player_menu():
            players_id = self.model.get_players_id()
            action, action_data = self.view.show_player_selection(players_id)
            if action == Request.SELECTED_PLAYER:
                selected_id = action_data
                # maybe move message to the view
                message_to_confirm = f"You are about to edit:\n{self.model.get_player_str(selected_id)}\nDo you confirm?"
                action, action_data = self.view.show_confirmation(message_to_confirm)
                if action == Request.CONFIRM:
                    confirm_status = action_data
                    if confirm_status:
                        attributes_info = self.model.get_player_attributes(selected_id)
                        action, action_data = self.view.show_edit_player_menu(attributes_info)
                        if action == Request.REGISTER_PLAYER_DATA:
                            player_data = action_data
                            self.model.edit_player_attributes(player_data)
                            self.view.show_status(True, self.model.get_player_str(player_data["identifier"]))
                            self.status = State.MANAGE_PLAYER_MENU
                        else:
                            self.status = State.MANAGE_PLAYER_MENU
                    else:
                        self.status = State.MANAGE_PLAYER_MENU
                else:
                    self.status = State.MANAGE_PLAYER_MENU
            else:
                self.status = State.MANAGE_PLAYER_MENU

        def show_add_player_menu():
            action, action_data = self.view.show_player_registration()
            if action == Request.REGISTER_PLAYER_DATA:
                try:
                    self.model.add_players(action_data)
                    self.view.show_status(True, self.model.get_player_str(action_data["identifier"]))
                except AlreadyUsedID as err:
                    self.view.show_status(False)
            self.status = State.MANAGE_PLAYER_MENU

        def show_list_players_menu():
            total_players = self.model.get_total_players()
            action = self.view.show_list_players_menu(total_players)
            if action not in (Request.PRINT_PLAYERS, Request.EXPORT_PLAYERS):
                self.status = State.MANAGE_PLAYER
            players_info = self.model.get_ordered_players_str()
            if action == Request.PRINT_PLAYERS:
                self.view.print_players(players_info)
            else:
                pass  # to-do
            self.status = State.MANAGE_PLAYER_MENU

        def show_tournament_registration():
            action, action_data = self.view.show_tournament_registration()
            if action == Request.REGISTER_TOURNAMENT_DATA:
                tournament_data = action_data
                try:
                    self.model.add_tournaments(tournament_data)
                    self.view.show_status(True, "correctly added")  # to-do: change message
                except AlreadyUsedID as err:
                    self.view.show_status(False)
            self.status = State.MANAGE_TOURNAMENTS_MENU

        def show_select_tournament_menu():
            # improvement : use round info to know if a tournament really ended
            statistics = {
                "all": len(self.model.tournaments),
                "ongoing": sum(1 for tournament in self.model.tournaments if
                               tournament.end_date <= datetime.date.today() >= tournament.begin_date),
                "future": sum(
                    1 for tournament in self.model.tournaments if tournament.begin_date > datetime.date.today()),
                "past": sum(1 for tournament in self.model.tournaments if tournament.end_date < datetime.date.today())
            }
            action = self.view.how_to_choose_tournament(statistics)
            if action == Request.FIND_TOURNAMENT_BY_NAME:
                tournaments_info = self.model.get_tournaments_str()
                action, action_data = self.view.choose_tournament_by_name(tournaments_info)
                if action == Request.SELECTED_TOURNAMENT:
                    selected_tournament = action_data
                    self.context = selected_tournament
                    self.status = State.MANAGE_TOURNAMENT_MENU
            else:
                self.status = State.MANAGE_TOURNAMENTS_MENU

        def show_manage_participants_menu():
            total_participants = len(list(self.model.get_participants_id(self.context)))  # to-do : change method
            action = self.view.show_manage_participants_menu(total_participants)
            if action == Request.ADD_PARTICIPANT:
                self.status = State.ADD_PARTICIPANT_MENU
            elif action == Request.DELETE_PARTICIPANT:
                self.status = State.DELETE_PARTICIPANT_MENU
            else:
                self.status = State.MANAGE_TOURNAMENT_MENU

        def show_add_participant_menu():
            selected_tournament = self.context
            players_id = [player_id for player_id in self.model.get_players_id()
                          if player_id not in self.model.get_participants_id(selected_tournament)]
            # to-do : verify if the list is empty
            if not players_id:
                self.view.show_status(False, "No available players to add")
                self.status = State.MANAGE_PARTICIPANTS_MENU
                return
            action, action_data = self.view.show_player_selection(players_id)
            if action == Request.SELECTED_PLAYER:
                selected_id = action_data
                # action, action_data = self.view.show_participant_registration(players)
                self.model.add_participants_to_tournament(selected_tournament, selected_id)
                self.view.show_status(True, f"participant added")
            self.status = State.MANAGE_PARTICIPANTS_MENU

        def show_register_match_score_menu():
            selected_tournament = self.context
            matches = self.model.get_round_matches(selected_tournament)
            matches_info = [f"{str(match.participants_pair[0].player)} vs {str(match.participants_pair[0].player)}"
                            for match in matches if
                            match.participants_scores is None]
            action, action_data = self.view.select_match(matches_info)
            if action == Request.SELECTED_MATCH:
                match_m = action_data
                action, action_data = self.view.enter_score(None)
                if action == Request.ADD_MATCH_RESULT:
                    first_player_result = action_data
                    self.model.register_score(selected_tournament, match_m, first_player_result)
                    self.view.show_status(True, "score saved")
                    self.status = State.MANAGE_TOURNAMENT_MENU
            else:
                self.status = State.MANAGE_TOURNAMENT_MENU

        def show_manage_unready_tournament_menu():
            selected_tournament = self.context
            tournament_info = self.model.get_tournament_info(selected_tournament)
            action = self.view.show_manage_unready_tournament_menu(tournament_info)
            if action == Request.MANAGE_PARTICIPANTS:
                self.status = State.MANAGE_PARTICIPANTS_MENU
            elif action == Request.GET_MATCHES_LIST:
                matches_info = [(match.participants_pair[0].player.identifier,
                                 match.participants_pair[1].player.identifier)
                                for match in self.model.get_round_matches(selected_tournament)]
                self.view.show_matches(matches_info)
                self.status = State.MANAGE_TOURNAMENT_MENU
            else:
                self.status = State.MAIN_MENU

        def show_manage_tournament_menu():
            # main menu (if not started) : manage participants or start tournament
            # main menu (if started) : same as this one but without participants
            selected_tournament = self.context
            tournament_info = self.model.get_tournament_info(selected_tournament)
            if not self.model.tournaments[selected_tournament].rounds:
                self.status = State.MANAGE_UNREADY_TOURNAMENT_MENU
                return
            action = self.view.show_manage_tournament_menu(tournament_info)

            # ------------- to move ------------------------
            if action == Request.START_ROUND:
                self.model.start_round(selected_tournament)
                self.view.show_status(True, f"round started {self.model.tournaments[selected_tournament].rounds}")
                self.status = State.MANAGE_TOURNAMENT_MENU
            if action == Request.GET_MATCHES_LIST:
                round_r = self.model.get_rounds(selected_tournament)[-1]
                matches_info = [(match.participants_pair[0].player.identifier,
                                 match.participants_pair[1].player.identifier)
                                for match in self.model.get_round_matches(selected_tournament, round_r)]
                self.view.show_matches(matches_info)
            if action == Request.REGISTER_MATCH_SCORE:
                self.status = State.REGISTER_MATCH_SCORE_MENU
            if action == Request.MANAGE_TOURNAMENT:
                self.status = State.MANAGE_TOURNAMENTS_MENU

        def show_manage_tournaments_menu():
            action = self.view.show_manage_tournaments_menu()
            if action == Request.ADD_TOURNAMENT:
                self.status = State.ADD_TOURNAMENT_MENU
            elif action == Request.EDIT_TOURNAMENT:
                if self.context is not None:
                    selected_tournament = self.context
                    tournament_info = self.model.get_tournament_info(selected_tournament)["str"]
                    action = self.view.keep_or_change_tournament(tournament_info)
                    if action == Request.KEEP_SELECTED_TOURNAMENT:
                        self.status = State.MANAGE_TOURNAMENT_MENU
                    elif action == Request.CHANGE_SELECTED_TOURNAMENT:
                        self.context = None
                        self.status = State.SELECT_TOURNAMENT_MENU
                else:
                    self.status = State.SELECT_TOURNAMENT_MENU
            elif action == Request.LIST_TOURNAMENTS:
                pass  # to-do
            else:
                self.status = State.MAIN_MENU

        while self.status != State.QUIT:
            if self.status == State.MAIN_MENU:
                show_main_menu()

            if self.status == State.MANAGE_PLAYER_MENU:
                show_manage_player_menu()

            if self.status == State.EDIT_PLAYER_MENU:
                show_edit_player_menu()

            if self.status == State.ADD_PLAYER_MENU:
                show_add_player_menu()

            if self.status == State.LIST_PLAYERS_MENU:
                show_list_players_menu()

            if self.status == State.MANAGE_TOURNAMENTS_MENU:
                show_manage_tournaments_menu()

            if self.status == State.MANAGE_TOURNAMENT_MENU:
                show_manage_tournament_menu()

            if self.status == State.MANAGE_UNREADY_TOURNAMENT_MENU:
                show_manage_unready_tournament_menu()

            if self.status == State.ADD_TOURNAMENT_MENU:
                show_tournament_registration()

            if self.status == State.SELECT_TOURNAMENT_MENU:
                show_select_tournament_menu()

            if self.status == State.MANAGE_PARTICIPANTS_MENU:
                show_manage_participants_menu()

            if self.status == State.ADD_PARTICIPANT_MENU:
                show_add_participant_menu()

            if self.status == State.DELETE_PARTICIPANT_MENU:
                show_delete_participant_menu()

            if self.status == State.REGISTER_MATCH_SCORE_MENU:
                show_register_match_score_menu()
