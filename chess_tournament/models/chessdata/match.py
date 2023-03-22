from dataclasses import dataclass
from enum import Enum
from typing import Tuple
from .participant import Participant


@dataclass
class Match:
    """Round's match data."""
    class Points(Enum):
        WIN = 1.0
        LOSE = 0.0
        DRAW = 0.5

    participants_pair: Tuple[Participant, Participant]
    participants_scores: Tuple[Points, Points] | None = None

    @classmethod
    def get_pairs_score_from_first(cls, first_result):
        if first_result == cls.Points.WIN:
            return cls.Points.WIN, cls.Points.LOSE
        if first_result == cls.Points.LOSE:
            return cls.Points.LOSE, cls.Points.WIN
        return cls.Points.DRAW, cls.Points.DRAW

    def register_score(self, participants_status: Tuple[Points, Points]):
        self.participants_scores = participants_status
        print(self.participants_pair)
        for participant, score in zip(self.participants_pair, self.participants_scores):
            participant.add_score(score.value)