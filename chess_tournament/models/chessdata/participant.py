from dataclasses import dataclass
from .player import Player


@dataclass
class Participant:
    """Tournament's participant data."""
    player: Player
    score: float = 0

    def add_score(self, to_add: float):
        self.score += to_add

    def __le__(self, other):
        return self.score <= other.score

    def __lt__(self, other):
        return self.score < other.score

