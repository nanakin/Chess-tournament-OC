from dataclasses import dataclass
from datetime import datetime
from typing import Tuple
from .match import Match


@dataclass
class Round:
    """Tournament's round data."""
    name: str
    matches: Tuple[Match]
    start_time: datetime | None = None
    end_time: datetime | None = None

    @property
    def is_ended(self):
        return self.end_time is not None

    def start_round(self, start_time: datetime = datetime.now()):
        self.start_time = start_time

    def end_round(self, end_time: datetime = datetime.now()):
        self.end_time = end_time
