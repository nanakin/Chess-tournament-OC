from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import List, Tuple, Self


@dataclass
class Player:
    """Player's data."""
    last_name: str
    first_name: str
    birth_date: date


@dataclass
class Participant:
    """Tournament's participant data."""
    player: Player
    score: float = 0

    def add_score(self: Self, to_add: float):
        self.score += to_add


@dataclass
class Match:
    """Round's match data."""
    class Points(Enum):
        WIN = 1.0
        LOSE = 0.0
        DRAW = 0.5

    participants_pair: Tuple[Participant, Participant]
    participants_scores: Tuple[Points] | None = None

    def register_score(self: Self, participants_status: Tuple[Points]):
        self.participants_scores = participants_status
        for p, participant in enumerate(self.participants_pair):
            self.participants_pair[p].add_score(self.participants_scores[p].value)


@dataclass
class Round:
    """Tournament's round data."""
    name: str
    matches: Tuple[Match]
    start_time: datetime | None = None
    end_time: datetime | None = None

    def start_round(self: Self, start_time: datetime = datetime.now()):
        self.start_time = start_time

    def end_round(self: Self, end_time: datetime = datetime.now()):
        self.end_time = end_time


@dataclass
class Tournament:
    """Tournament data."""
    name: str
    location: str
    begin_date: date
    end_date: date
    participants: Tuple[Participant]
    total_round: int = 4
    rounds: List[Round] = field(default_factory=list)
    current_round: int = 0

    def _generate_matches(self) -> Tuple[Match]:
        # sort participants by score and create pairs by order
        # to implement
        return tuple()  # temp

    def get_next_round(self):
        self.current_round += 1
        round = Round(name=f"Round {self.current_round}",
                      matches=self._generate_matches())
        self.rounds.append(round)
