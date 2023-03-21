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

    def register_score(self, participants_status: Tuple[Points, Points]):
        self.participants_scores = participants_status
        print(self.participants_pair)
        for participant, score in zip(self.participants_pair, self.participants_scores):
            participant.add_score(score.value)