from dataclasses import dataclass, field
from pathlib import Path
from .chessdata.player import Player
from .chessdata.tournament import Tournament
from .chessdata.participant import Participant


@dataclass
class Model:

    data_path: Path | None
    players: dict[Player] = field(default_factory=dict)
    tournaments: list[Tournament] = field(default_factory=list)

    # public methods accessible by the controller and the load/backup system

    def add_players(self, *players_data):
        for player_data in players_data:
            self.players[player_data["identifier"]] = Player(**player_data)

    def add_tournaments(self, *tournaments_data):
        for tournament_data in tournaments_data:
            self.tournaments.append(Tournament(**tournament_data))

    def add_participants_to_tournament(self, tournament_t, *participants_data):
        for player_id in participants_data:
            self.tournaments[tournament_t].participants.append(Participant(self.players[player_id]))

    def start_round(self, tournament_t):
        self.tournaments[tournament_t].start_round()

    def get_round_matches(self, tournament_t):
        self.tournaments[tournament_t].get_round_matches()





