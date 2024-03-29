"""Define all the model methods required by the controller."""

from collections.abc import KeysView
from datetime import date
from pathlib import Path
from typing import Any, Callable, Iterator, Optional

from .chessdata import Match, Participant, Player, Tournament
from .save_load_system import BackupManager, save_at_the_end

Log = str


class AlreadyUsedID(Exception):
    """Exception raised when an ID is already used."""


class InconsistentDates(Exception):
    """Exception raised when ending is anterior to starting."""


class Model(BackupManager):
    """Expose public methods to allow chess data manipulation from the controller.

    This class abstract the internal data structure to the controller."""

    status_filter: dict[str, Callable[[Tournament], bool]] = {
        "past": lambda tournament: tournament.end_date < date.today()
        or (tournament.end_date == date.today() and tournament.is_ended),
        "future": lambda tournament: tournament.begin_date > date.today()
        or (tournament.begin_date == date.today() and not tournament.total_started_rounds),
        "ongoing": lambda tournament: tournament.begin_date <= date.today()
        and tournament.is_started
        and not tournament.is_ended,
        "all": lambda tournament: True,
    }

    def __init__(self, data_path: Path) -> None:
        super().__init__(data_path)
        self.players = {}
        self.tournaments = []

    # -- players --------------------------------------------------------------

    @save_at_the_end(players_file=True)
    def add_players(self, *players_data: dict[str, Any]) -> Log:
        """Create new players and register them in the internal list."""
        # + cleaning user input and checking ID duplicates.
        for player_data in players_data:
            if player_data["identifier"].upper() not in self.players:
                # formatting
                player_data["last_name"] = player_data["last_name"].upper()
                player_data["first_name"] = player_data["first_name"].capitalize()
                player_data["identifier"] = player_data["identifier"].upper()
                if isinstance(player_data["birth_date"], str):
                    player_data["birth_date"] = date.fromisoformat(player_data["birth_date"])
                # create new player
                self.players[player_data["identifier"]] = Player(**player_data)
            else:
                raise AlreadyUsedID(player_data["identifier"])
        # Log only the last one (players are added 1 by 1 from the interface)
        return str(self.players[player_data["identifier"]])

    @save_at_the_end(players_file=True)
    def edit_player_attributes(self, player_data: dict[str, Any]) -> Log:
        """Edit existing player attributes."""
        player = self.players[player_data["identifier"]]
        player.first_name = player_data["first_name"].capitalize()
        player.last_name = player_data["last_name"].upper()
        player.birth_date = date.fromisoformat(player_data["birth_date"])
        return str(player)

    def get_players_id(self) -> KeysView:
        """Return list of players ID."""
        return self.players.keys()

    def get_player_str(self, identifier: str) -> str:
        """Return player description."""
        return str(self.players[identifier])

    def get_player_attributes(self, identifier: str) -> dict[str, Any]:
        """Return the players attributes as dictionary."""
        player = self.players[identifier]
        return player.encode()

    def get_ordered_players_str(self) -> list[str]:
        """Return ordered players descriptions."""
        sorted_players = sorted(self.players.values())
        return [self.get_player_str(player.identifier) for player in sorted_players]

    def get_total_players(self) -> int:
        """Return the total number of existing players."""
        return len(self.players)

    # -- participants ---------------------------------------------------------

    @save_at_the_end(tournaments_file=True)
    def add_participants_to_tournament(self, tournament_t: int, *participants_data: str) -> tuple[Log, Log]:
        """Create participants from players and link them to the given tournaments."""
        tournament = self.tournaments[tournament_t]
        for player_id in participants_data:
            participant = Participant(self.players[player_id])
            tournament.participants.append(participant)
        # Log only the last one (participants are added 1 by 1 from the interface)
        return str(participant.player), str(tournament)

    @save_at_the_end(tournaments_file=True)
    def delete_participants_from_tournament(self, tournament_t: int, *participants_data: str) -> tuple[Log, Log]:
        """Create participants from players and link them to the given tournaments."""
        tournament = self.tournaments[tournament_t]
        for player_id in participants_data:
            participant_to_log = str(self.players[player_id])
            for p_index, participant in enumerate(tournament.participants):
                if participant.player.identifier == player_id:
                    del tournament.participants[p_index]
                    break
        # Log only the last one (participants are deleted 1 by 1 from the interface)
        return participant_to_log, str(tournament)

    def get_total_participants(self, tournament_t: int) -> int:
        """Return the total number of participant from a given tournament."""
        return len(self.tournaments[tournament_t].participants)

    def get_ordered_participants_str(self, tournament_t: int) -> list[str]:
        """Return participants descriptions."""
        sorted_participants = sorted(
            self.tournaments[tournament_t].participants,
            key=lambda participant: participant.player,
        )
        return [str(participant) for participant in sorted_participants]

    def get_participants_id(self, tournament_t: int) -> Iterator[str]:
        """Return the participants ID from a given tournament."""
        return (participant.player.identifier for participant in self.tournaments[tournament_t].participants)

    def _get_winners(self, tournament_t: int) -> list[str]:
        """Return strings representation of tournaments winners."""
        tournament = self.tournaments[tournament_t]
        ordered_participants = sorted(tournament.participants)
        bests = []
        for i in range(len(ordered_participants)):
            bests.append(str(ordered_participants[i]))
            if i >= 2:
                # in case of tie, continue listing winners with the same score
                if (
                    len(ordered_participants) > i + 1
                    and ordered_participants[i].score == ordered_participants[i + 1].score
                ):
                    continue
                break
        return bests

    # -- matches --------------------------------------------------------------

    @save_at_the_end(tournaments_file=True)
    def register_score(self, tournament_t: int, match_m: int, first_player_result_str: str) -> Log:
        """Register participant score for a given match."""
        tournament = self.tournaments[tournament_t]
        round = tournament.current_round
        first_result = Match.Points[first_player_result_str]
        pair_result = Match.get_pairs_score_from_first(first_result)
        round.matches[match_m].register_score(pair_result)
        are_all_matches_ended = all([bool(match.participants_scores is not None) for match in round.matches])
        if are_all_matches_ended:
            round.end_round()
            if tournament.total_finished_rounds < tournament.total_rounds:
                tournament.set_next_round()
        return str(round.matches[match_m])

    @save_at_the_end(tournaments_file=True)
    def get_round_matches(self, tournament_t: int) -> tuple[Match, ...]:
        """Return matches of the given round."""
        round_r = self.tournaments[tournament_t].current_round_index
        if round_r == len(self.tournaments[tournament_t].rounds):
            self.tournaments[tournament_t].set_next_round()
        return self.tournaments[tournament_t].get_round_matches(round_r)

    def get_total_matches(self, tournament_t: int) -> int:
        """Return the total number of matches from a given tournament’s round."""
        round_r = self.tournaments[tournament_t].current_round_index
        return len(self.tournaments[tournament_t].get_round_matches(round_r))

    def get_total_all_matches(self, tournament_t: int) -> int:
        """Return the total number of matches from a given tournaments (all rounds)."""
        tournament = self.tournaments[tournament_t]
        return sum(len(tournament.get_round_matches(round_r)) for round_r in range(tournament.total_started_rounds))

    def get_all_matches_str(self, tournament_t: int) -> list[str]:
        """Return matches descriptions."""
        tournament = self.tournaments[tournament_t]
        matches = []
        for r, round in enumerate(tournament.rounds):
            matches.append(round.name)
            matches.extend(self.get_matches_str(tournament_t, r))
        return matches

    def start_tournament(self, tournament_t: int) -> tuple[Log, int]:
        """Start the given tournament (and generate the first round matches)."""
        matches = self.get_round_matches(tournament_t)
        return str(self.tournaments[tournament_t]), len(matches)

    def get_matches_str(self, tournament_t: int, round_r: Optional[int] = None) -> list[str]:
        """Return matches descriptions."""
        if round_r is None:
            round_r = self.tournaments[tournament_t].current_round_index
        return [str(match) for match in self.tournaments[tournament_t].get_round_matches(round_r)]

    # -- tournaments ----------------------------------------------------------

    @save_at_the_end(tournaments_file=True)
    def add_tournaments(self, *tournaments_data: dict[str, Any]) -> Log:
        """Create new tournaments and add them to the internal list."""
        for tournament_data in tournaments_data:
            tournament_data["name"] = tournament_data["name"].strip()
            tournament_data["location"] = tournament_data["location"].capitalize()
            tournament_data["total_rounds"] = int(tournament_data["total_rounds"])
            if isinstance(tournament_data["begin_date"], str):
                tournament_data["begin_date"] = date.fromisoformat(tournament_data["begin_date"])
            if isinstance(tournament_data["end_date"], str):
                tournament_data["end_date"] = date.fromisoformat(tournament_data["end_date"])
            if tournament_data["end_date"] < tournament_data["begin_date"]:
                raise InconsistentDates(
                    f"{tournament_data['name']} ending date ({tournament_data['end_date']})"
                    + f" is anterior to starting date ({tournament_data['begin_date']})"
                )
            tournament = Tournament(**tournament_data)
            self.tournaments.append(tournament)
        return str(tournament)  # Log only the last one (tournaments are added 1 by 1 from the interface)

    @save_at_the_end(tournaments_file=True)
    def start_round(self, tournament_t: int):
        """Start the next round of the given tournament."""
        self.tournaments[tournament_t].start_round()

    def get_ordered_tournaments_str(self) -> list[str]:
        """Return ordered tournaments descriptions."""
        sorted_tournaments = sorted(self.tournaments)
        return [str(tournament) for tournament in sorted_tournaments]

    def get_tournaments_states_statistics(self) -> dict[str, int]:
        """Return tournaments states statistics (number of ongoing/past/future/all)."""
        statistics = {}
        for filter_name, func_status_filter in self.status_filter.items():
            statistics[filter_name] = sum(1 for tournament in self.tournaments if func_status_filter(tournament))
        return statistics

    def get_total_tournaments(self) -> int:
        """Return the total number of tournaments."""
        return len(self.tournaments)

    def get_tournaments_str(self, status: str = "all") -> list[tuple[int, str, str]]:
        """Return tournaments descriptions."""
        return [
            (t_index, tournament.name, str(tournament))
            for t_index, tournament in enumerate(self.tournaments)
            if self.status_filter[status](tournament)
        ]

    def get_tournament_info(self, tournament_t: int) -> dict[str, Any]:
        """Return various tournament data as dictionary."""
        tournament = self.tournaments[tournament_t]
        return {
            "str": str(tournament),
            "name": tournament.name,
            "location": tournament.location,
            "begin_date": str(tournament.begin_date),
            "end_date": str(tournament.end_date),
            "total_rounds": tournament.total_rounds,
            "is_current_round_started": tournament.current_round.is_started if tournament.is_started else False,
            "current_round_name": tournament.current_round.name if tournament.is_started else None,
            "total_started_rounds": tournament.total_started_rounds,
            "total_finished_matches": sum(1 for match in tournament.current_round.matches if match.is_ended)
            if tournament.total_started_rounds > 0
            else 0,
            "total_matches": len(tournament.current_round.matches) if tournament.total_started_rounds > 0 else 0,
            "total_finished_rounds": tournament.total_finished_rounds,
            "total_participants": len(tournament.participants),
            "winners": self._get_winners(tournament_t) if tournament.is_ended else None,
        }
