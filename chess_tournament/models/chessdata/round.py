from dataclasses import dataclass
from datetime import datetime
from typing import Tuple
from .match import Match
from ..serialization import Serializable


@dataclass
class Round(Serializable):
    """Tournament's round data."""
    name: str
    matches: Tuple[Match]
    start_time: datetime | None = None
    end_time: datetime | None = None

    @property
    def is_ended(self):
        return self.end_time is not None

    @property
    def is_started(self):
        return self.start_time is not None

    def start_round(self, start_time: datetime = datetime.now()):
        self.start_time = start_time

    def end_round(self, end_time: datetime = datetime.now()):
        self.end_time = end_time

    def encode(self):
        return {
            "name": self.name,
            "start_time": str(self.start_time) if self.start_time is not None else "",
            "end_time": str(self.end_time) if self.end_time is not None else "",
            "matches": [match.encode() for match in self.matches]
        }

    @classmethod
    def decode(cls, encoded_data):
        encoded_data["start_time"] = datetime.fromisoformat(encoded_data["start_time"]) if encoded_data["start_time"] else None
        encoded_data["end_time"] = datetime.fromisoformat(encoded_data["end_time"]) if encoded_data["end_time"] else None
        encoded_data["matches"] = tuple([Match.decode(encoded_match)
                                         for encoded_match in encoded_data["matches"]])
        return cls(**encoded_data)
