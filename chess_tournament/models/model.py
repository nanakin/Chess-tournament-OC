from dataclasses import dataclass, field
from pathlib import Path
from .chessdata.player import Player
from .chessdata.tournament import Tournament


@dataclass
class Model:

    data_path: Path | None
    players: list[Player] = field(default_factory=list)
    tournaments: list[Tournament] = field(default_factory=list)

    # public methods accessible by the controller
    def add_players(self, *players_data):
        for player_data in players_data:
            self.players.append(Player(**player_data))

    def add_tournaments(self, *tournaments_data):
        for tournament_data in tournaments_data:
            self.tournaments.append(Tournament(**tournament_data))

    def start_round(self, current_tournament):
        self.tournaments[current_tournament].start_round()

    def get_round_matches(self, current_tournament):
        self.tournaments[current_tournament].get_round_matches()





