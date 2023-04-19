"""Define tournaments related data structures."""

import random
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Self

from ..serialization import Serializable
from .match import Match
from .participant import Participant
from .round import Round
from .player import Player
from .matchmaking import MatchMaking


@dataclass
class Tournament(Serializable, MatchMaking):
    """Tournament data."""

    name: str
    location: str
    begin_date: date
    end_date: date
    participants: list[Participant] = field(default_factory=list)
    total_rounds: int = 4
    rounds: list[Round] = field(default_factory=list)

    @property
    def total_finished_rounds(self) -> int:
        """Return the total number of finished rounds."""
        if not self.rounds:
            return 0
        else:
            return len(self.rounds) - 1 if self.rounds[-1].end_time is None else len(self.rounds)

    def __str__(self) -> str:
        """Return the string representation of the tournament instance."""
        return f'{self.name} in {self.location} ({str(self.begin_date)} > {str(self.end_date)})'

    def __lt__(self, other: Self) -> bool:
        """Order tournaments by starting date."""
        return self.begin_date < other.begin_date

    @property
    def current_round(self) -> Round:
        """Return the last started round."""
        return self.rounds[-1]

    @property
    def current_round_index(self) -> int:
        return max(0, len(self.rounds) - 1)

    @property
    def is_ended(self) -> bool:
        """Return True if all rounds are finished, False otherwise."""
        return self.total_finished_rounds == self.total_rounds

    @property
    def is_started(self) -> bool:
        """Return True if a least one round has been generated, False otherwise."""
        return self.total_started_rounds > 0

    @property
    def total_started_rounds(self) -> int:
        """Return the total number of rounds generated."""
        return len(self.rounds)

    def set_next_round(self) -> None:
        """Do the matchmaking and register the round internally."""
        matches_list = self.generate_pairs(self.total_started_rounds, self.participants)
        round = Round(name=f"Round {(len(self.rounds) + 1)}", matches=matches_list)
        self.rounds.append(round)

    def start_round(self) -> None:
        """Register the starting time of the current round."""
        self.current_round.start_round()

    def get_round_matches(self, round_r) -> tuple[Match, ...]:
        """Return matches of the given round index."""
        if not self.rounds or round_r >= len(self.rounds):
            return tuple()
        return self.rounds[round_r].matches

    def encode(self) -> dict[str, Any]:
        """Transform the instance of the object into JSON compatible format."""
        return {
            "name": self.name,
            "location": self.location,
            "begin_date": str(self.begin_date),
            "end_date": str(self.end_date),
            "total_rounds": int(self.total_rounds),
            "participants": [participant.encode() for participant in self.participants],
            "rounds": [round.encode() for round in self.rounds],
        }

    @classmethod
    def decode(cls, encoded_data: dict[str, Any], players_db: dict[str, Player]) -> Self:
        """Instantiate a new object from data in JSON format."""
        encoded_data["begin_date"] = date.fromisoformat(encoded_data["begin_date"])
        encoded_data["end_date"] = date.fromisoformat(encoded_data["end_date"])
        encoded_data["participants"] = [
            Participant.decode(encoded_participant, players_db) for encoded_participant in encoded_data["participants"]
        ]
        encoded_data["rounds"] = [Round.decode(encoded_round, encoded_data["participants"])
                                  for encoded_round in encoded_data["rounds"]]
        tournament = cls(**encoded_data)
        tournament.reconstruct_remaining_possibilities_from_past_matches(tournament.participants, tournament.rounds)
        return tournament
