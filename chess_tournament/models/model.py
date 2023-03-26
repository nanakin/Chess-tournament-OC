from dataclasses import dataclass, field
from pathlib import Path
from datetime import date
from .chessdata.player import Player
from .chessdata.tournament import Tournament
from .chessdata.participant import Participant
from .chessdata.match import Match
from pprint import pprint


class AlreadyUsedID(Exception):
    def __init__(self, *args):
        super().__init__(args)
    def __str__(self):
        return "bla"

@dataclass
class Model:
    """The only external interface to manipulate chess data."""

    data_path: Path | None
    players: dict[Player] = field(default_factory=dict)
    tournaments: list[Tournament] = field(default_factory=list)

    # public methods accessible by the controller and the load/backup system

    def add_players(self, *players_data):
        for player_data in players_data:
            if player_data["identifier"] not in self.players:
                # formatting (to move to Player init method ?)
                player_data["last_name"] = player_data["last_name"].upper()
                player_data["first_name"] = player_data["first_name"].capitalize()
                player_data["identifier"] = player_data["identifier"].upper()
                if player_data["birth_date"] is type(str):
                    player_data["birth_date"] = date.fromisoformat(player_data["birth_date"])
                # create new player
                self.players[player_data["identifier"]] = Player(**player_data)
            else:
                raise AlreadyUsedID(player_data["identifier"])

    def edit_player_attributes(self, player_data):
        player = self.players[player_data["identifier"]]
        player.first_name = player_data["first_name"].capitalize()
        player.last_name = player_data["last_name"].upper()
        player.birth_date = date.fromisoformat(player_data["birth_date"])

    def get_players_id(self):
        return self.players.keys()

    def get_player_str(self, identifier):
        return str(self.players[identifier])

    def get_player_attributes(self, identifier):
        # maybe implement to_dict method
        player = self.players[identifier]
        return {"identifier": player.identifier, "first_name": player.first_name,
                "last_name": player.last_name, "birth_date": str(player.birth_date)}

    def get_ordered_players_str(self):
        sorted_players = sorted(self.players.values())
        return [self.get_player_str(player.identifier) for player in sorted_players]

    def get_total_players(self):
        return len(self.players)

    def get_tournaments_str(self, filter=None):
        return [(tournament.name, str(tournament)) for tournament in self.tournaments]

    def get_tournament_info(self, tournament_t):
        tournament = self.tournaments[tournament_t]
        return {"name": tournament.name, "location": tournament.location, "begin_date": str(tournament.begin_date),
                "end_date": str(tournament.end_date), "total_rounds": tournament.total_rounds,
                "total_started_rounds": tournament.total_started_rounds,
                "total_finished_matches": sum(1 for match in tournament.current_round.matches if match.is_ended) if tournament.total_started_rounds > 0 else 0,
                "total_matches": len(tournament.current_round.matches) if tournament.total_started_rounds > 0 else 0,
                "total_finished_rounds": tournament.total_finished_rounds,
                "total_participants": len(tournament.participants)}

    def add_tournaments(self, *tournaments_data):
        for tournament_data in tournaments_data:
            self.tournaments.append(Tournament(**tournament_data))

    def add_participants_to_tournament(self, tournament_t, *participants_data):
        for player_id in participants_data:
            self.tournaments[tournament_t].participants.append(Participant(self.players[player_id]))

    def register_score(self, tournament_t, match_m, first_player_result_str):
        round = self.tournaments[tournament_t].current_round
        first_result = Match.Points[first_player_result_str]
        pair_result = Match.get_pairs_score_from_first(first_result)
        round.matches[match_m].register_score(pair_result)
        are_all_matches_ended = all([True for match in round.matches
                                     if match.participants_scores is not None])
        if are_all_matches_ended:
            round.end_round()

    def start_round(self, tournament_t):
        self.tournaments[tournament_t].start_round()

    def get_rounds(self, tournament_t):
        return self.tournaments[tournament_t].rounds

    def get_round_matches(self, tournament_t, round_r=None):
        if round_r is None:
            round_r = max(0, len(self.tournaments[tournament_t].rounds) - 1)
        if round_r == len(self.tournaments[tournament_t].rounds):
            self.tournaments[tournament_t].set_next_round()
        return self.tournaments[tournament_t].get_round_matches(round_r)
