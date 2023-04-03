from dataclasses import dataclass
from .player import Player
from ..serialization import Serializable

@dataclass
class Participant(Serializable):
    """Tournament's participant data."""
    player: Player
    score: float = 0

    def add_score(self, to_add: float):
        self.score += to_add

    def __le__(self, other):
        return self.score <= other.score

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        return f"{self.player.identifier} ({self.score} points)"

    def __hash__(self):
        return hash(self.player.identifier)

    def encode(self):
        return {
            "player": self.player.encode(),
            "score": self.score,
        }

    @classmethod
    def decode(cls, encoded_data):
        encoded_data["player"] = Player.decode(encoded_data["player"])
        encoded_data["score"] = float(encoded_data["score"])
        return cls(**encoded_data)
