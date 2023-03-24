from dataclasses import dataclass, field
from pathlib import Path
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
                # create new player
                self.players[player_data["identifier"]] = Player(**player_data)
            else:
                raise AlreadyUsedID(player_data["identifier"])

    def get_player_str(self, identifier):
        return str(self.players[identifier])

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





