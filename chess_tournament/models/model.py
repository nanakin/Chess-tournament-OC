import datetime
from dataclasses import dataclass, field
from pathlib import Path
from datetime import date
from .chessdata.player import Player
from .chessdata.tournament import Tournament
from .chessdata.participant import Participant
from .chessdata.match import Match
from .save_load_system import BackupManager, save_at_the_end
from pprint import pprint
import json


class AlreadyUsedID(Exception):
    def __init__(self, *args):
        super().__init__(args)
    def __str__(self):
        return "bla"


@dataclass
class Model(BackupManager):
    """The only external interface to manipulate chess data."""

    data_path: Path | None
    players: dict[Player] = field(default_factory=dict)
    tournaments: list[Tournament] = field(default_factory=list)
    status_filter = {
        "past": lambda tournament: tournament.end_date < datetime.date.today() or (tournament.end_date == datetime.date.today() and tournament.is_ended),
        "future": lambda tournament: tournament.begin_date > datetime.date.today() or (tournament.begin_date == datetime.date.today() and not tournament.total_started_rounds),
        "ongoing": lambda tournament: tournament.begin_date <= datetime.date.today() and tournament.total_started_rounds > 0,
        "all": lambda tournament: True
    }

    # public methods accessible by the controller and the load/backup system

    @save_at_the_end(players_file=True)
    def add_players(self, *players_data):
        for player_data in players_data:
            if player_data["identifier"] not in self.players:
                # formatting (to move to Player init method ?)
                player_data["last_name"] = player_data["last_name"].upper()
                player_data["first_name"] = player_data["first_name"].capitalize()
                player_data["identifier"] = player_data["identifier"].upper()
                if isinstance(player_data["birth_date"], str):
                    player_data["birth_date"] = date.fromisoformat(player_data["birth_date"])
                # create new player
                self.players[player_data["identifier"]] = Player(**player_data)
            else:
                raise AlreadyUsedID(player_data["identifier"])

    @save_at_the_end(players_file=True)
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

    def get_tournaments_states_statistics(self):
        statistics = {}
        for filter_name, func_status_filter in self.status_filter.items():
            statistics[filter_name] = sum(1 for tournament in self.tournaments
                                          if func_status_filter(tournament))
        return statistics

    def get_ordered_tournaments_str(self):
        sorted_tournaments = sorted(self.tournaments)
        return [str(tournament) for tournament in sorted_tournaments]

    def get_total_tournaments(self):
        return len(self.tournaments)

    def get_tournaments_str(self, status="all"):
        return [(t_index, tournament.name, str(tournament)) for t_index, tournament in enumerate(self.tournaments)
                if self.status_filter[status](tournament)]

    def get_participants_id(self, tournament_t):
        return (participant.player.identifier for participant in self.tournaments[tournament_t].participants)

    def get_tournament_info(self, tournament_t):
        tournament = self.tournaments[tournament_t]
        return {"str": str(tournament),
                "name": tournament.name, "location": tournament.location, "begin_date": str(tournament.begin_date),
                "end_date": str(tournament.end_date), "total_rounds": tournament.total_rounds,
                "total_started_rounds": tournament.total_started_rounds,
                "total_finished_matches": sum(1 for match in tournament.current_round.matches if match.is_ended) if tournament.total_started_rounds > 0 else 0,
                "total_matches": len(tournament.current_round.matches) if tournament.total_started_rounds > 0 else 0,
                "total_finished_rounds": tournament.total_finished_rounds,
                "total_participants": len(tournament.participants)}

    @save_at_the_end(tournaments_file=True)
    def add_tournaments(self, *tournaments_data):
        for tournament_data in tournaments_data:
            tournament_data["name"] = tournament_data["name"].strip()
            tournament_data["location"] = tournament_data["location"].capitalize()
            if isinstance(tournament_data["begin_date"], str):
                tournament_data["begin_date"] = date.fromisoformat(tournament_data["begin_date"])
            if isinstance(tournament_data["end_date"], str):
                tournament_data["end_date"] = date.fromisoformat(tournament_data["end_date"])
            # to-do: verify begin_date < end_date
            self.tournaments.append(Tournament(**tournament_data))

    @save_at_the_end(tournaments_file=True)
    def add_participants_to_tournament(self, tournament_t, *participants_data):
        for player_id in participants_data:
            self.tournaments[tournament_t].participants.append(Participant(self.players[player_id]))

    @save_at_the_end(tournaments_file=True)
    def register_score(self, tournament_t, match_m, first_player_result_str):
        round = self.tournaments[tournament_t].current_round
        first_result = Match.Points[first_player_result_str]
        pair_result = Match.get_pairs_score_from_first(first_result)
        round.matches[match_m].register_score(pair_result)
        are_all_matches_ended = all([True for match in round.matches
                                     if match.participants_scores is not None])
        if are_all_matches_ended:
            round.end_round()

    @save_at_the_end(tournaments_file=True)
    def start_round(self, tournament_t):
        self.tournaments[tournament_t].start_round()

    def get_rounds(self, tournament_t):
        return self.tournaments[tournament_t].rounds

    @save_at_the_end(tournaments_file=True)
    def get_round_matches(self, tournament_t, round_r=None):
        if round_r is None:
            round_r = max(0, len(self.tournaments[tournament_t].rounds) - 1)
        if round_r == len(self.tournaments[tournament_t].rounds):
            self.tournaments[tournament_t].set_next_round()
        return self.tournaments[tournament_t].get_round_matches(round_r)
