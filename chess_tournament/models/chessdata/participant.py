"""Define tournament's participants related data structures."""

from dataclasses import dataclass
from typing import Any, Self

from ..serialization import Serializable
from .player import Player


@dataclass
class Participant(Serializable):
    """Tournament's participant data."""

    player: Player
    score: float = 0

    def add_score(self, to_add: float) -> None:
        """Add up the participant score."""
        self.score += to_add

    def __lt__(self, other: Self) -> bool:
        """Order participant by score."""
        return self.score > other.score

    def __str__(self) -> str:
        """Return string representation of a participant instance."""
        return f"{self.player} - {self.score} points"

    def __hash__(self) -> int:
        """Make participant instance hashable."""
        return hash(self.player.identifier)

    def encode(self) -> dict[str, Any]:
        """Transform the instance of the object into JSON compatible format."""
        return {
            "player": self.player.identifier,
            "score": self.score,
        }

    @classmethod
    def decode(cls, encoded_data: dict[str, Any], players_db: dict) -> Self:
        """Instantiate a new object from data in JSON format."""
        encoded_data["player"] = players_db[encoded_data["player"]]
        encoded_data["score"] = float(encoded_data["score"])
        return cls(**encoded_data)
