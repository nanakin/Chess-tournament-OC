"""Define rounds related data structures."""

from dataclasses import dataclass
from datetime import datetime
from typing import Self, Any

from ..serialization import Serializable
from .match import Match
from .participant import Participant


@dataclass
class Round(Serializable):
    """Tournament's round data."""

    name: str
    matches: tuple[Match, ...]
    start_time: datetime | None = None
    end_time: datetime | None = None

    @property
    def is_ended(self) -> bool:
        """Return True if the round has an end time defined, False otherwise."""
        return self.end_time is not None

    @property
    def is_started(self) -> bool:
        """Return True if the round has a start time defined, False otherwise."""
        return self.start_time is not None

    def start_round(self, start_time: datetime = datetime.now()) -> None:
        """Register the starting time of the round."""
        self.start_time = start_time

    def end_round(self, end_time: datetime = datetime.now()) -> None:
        """Register the ending time of the round."""
        self.end_time = end_time

    def encode(self) -> dict[str, object]:
        """Transform the instance of the object into JSON compatible format."""
        return {
            "name": self.name,
            "start_time": str(self.start_time) if self.start_time is not None else "",
            "end_time": str(self.end_time) if self.end_time is not None else "",
            "matches": [match.encode() for match in self.matches],
        }

    @classmethod
    def decode(cls, encoded_data: dict[str, Any], participants_db: list[Participant]) -> Self:
        """Instantiate a new object from data in JSON format."""
        encoded_data["start_time"] = (
            datetime.fromisoformat(encoded_data["start_time"]) if encoded_data["start_time"] else None
        )
        encoded_data["end_time"] = (
            datetime.fromisoformat(encoded_data["end_time"]) if encoded_data["end_time"] else None
        )
        encoded_data["matches"] = tuple([Match.decode(encoded_match, participants_db) for encoded_match in encoded_data["matches"]])
        return cls(**encoded_data)
